# Modified by Nisa

from __future__ import print_function

from pprint import pprint
from time import time
import logging

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn import metrics

import numpy as np

###############################################################################
train_file = 'train_gold.txt'
train_data = []
train_cats = []
with open(train_file, 'r') as f:
    for line in f:
        l = line.split()
        train_cats.append(l[1])
        train_data.append(" ".join(l[2:]))


test_file = 'test_gold.txt'
test_data = []
test_cats = []
with open(test_file, 'r') as f:
    for line in f:
        l = line.split()
        test_cats.append(l[1])
        test_data.append(" ".join(l[2:]))

###############################################################################
# define a pipeline combining a text feature extractor with a simple
# classifier
pipeline = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', SGDClassifier()),
])

# uncommenting more parameters will give better exploring power but will
# increase processing time in a combinatorial way
parameters = {
    'vect__max_df': (0.5, 0.75, 1.0),
    'vect__max_features': (None, 5000, 10000, 50000),
    'vect__ngram_range': ((1, 1), (1, 2)),  # unigrams or bigrams
    'tfidf__use_idf': (True, False),
    'tfidf__norm': ('l1', 'l2'),
    'clf__alpha': (0.00001, 0.000001),
    'clf__penalty': ('l2', 'elasticnet'),
    'clf__n_iter': (10, 50, 80),
}

if __name__ == "__main__":
    # multiprocessing requires the fork to happen in a __main__ protected
    # block

    # find the best parameters for both the feature extraction and the
    # classifier
    grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1, verbose=1)

    #print("Performing grid search...")
    #print("pipeline:", [name for name, _ in pipeline.steps])
    #print("parameters:")
    #pprint(parameters)
    t0 = time()
    label_map = dict((k, i) for i, k in enumerate(set(train_cats)))
    train_labels = np.array([label_map[cat] for cat in train_cats])

    test_label_map = dict((k, i) for i, k in enumerate(set(test_cats)))
    test_labels = np.array([test_label_map[cat] for cat in test_cats])

    #grid_search.fit(train_data, train_cats)
    grid_search.fit(train_data, train_labels)
    #print("done in %0.3fs" % (time() - t0))
    #print()
    print("Best score: %0.3f" % grid_search.best_score_)

    pred = grid_search.best_estimator_.predict(test_data)
    print(metrics.accuracy_score(test_labels, pred))

    print("Best parameters set:")
    best_parameters = grid_search.best_estimator_.get_params()
    for param_name in sorted(parameters.keys()):
        print("\t%s: %r" % (param_name, best_parameters[param_name]))
