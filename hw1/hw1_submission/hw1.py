from __future__ import division
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7

@author: Team TORIAS!
"""

"""
This is the code to execute our hw1
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn import svm
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.lancaster import LancasterStemmer
from sklearn.externals import joblib
import argparse
import numpy as np
from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline
from time import time
from cat_entropy import *


"""
This is the Lemma Tokenizer class that uses wordnet and the nltk library
"""
class LemmaTokenizer(object):
	def __init__(self):
		self.wnl = WordNetLemmatizer()
	def __call__(self, doc):
		return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]

"""
This is the Stem Tokenizer class from the nltk library
"""
class StemTokenizer(object):
	def __init__(self):
		self.st = LancasterStemmer()
	def __call__(self, doc):
		return [self.st.stem(t) for t in word_tokenize(doc)]


"""
This is the code to parse the arguments for the file
"""
def parse_args():
    p = argparse.ArgumentParser(description="Runs the classification algorithm")
    p.add_argument('-te', '--testlabel', dest='testFile', help="This is the label file", required=False, default='test_gold.txt')
    p.add_argument('-tr', '--trainlabel', dest='trainFile', help="This is the train file", required=False, default='train_gold.txt')
    p.add_argument('-d', '--data', dest='dataFile', help="This is the data file with one line per review in the single file", required=False, default='complete_set.txt')
    p.add_argument('-o', '--output', dest='outputFile', help="This is the data file that will output the results", required=False, default='results.txt')
    p.add_argument('-r', '--represent', dest='representation', type=int, help="This is a number, which representation are you testing against, valid numbers are 0-3", required=False, default='0')
    p.add_argument('-ci', '--inputclassifier', dest='inputClassifierFile', help="This is the classifier to use based off the train data", required=False, default='classifierFile.pkl')
    p.add_argument('-co', '--outputclassifier', dest='outputClassifierFile', help="This is the classifier file to output based off the train data", required=False, default='classifierFile.pkl')
    p.add_argument('-p', '--pipeline', dest='isPipelineRun', help="Is True if we should run the pipeline tests", required=False, default=False)
    p.add_argument('-it', '--train', dest='isTrain', help="Is training done or just run on testing", required=False, default=True)
    #p.add_argument('-a', '--alpha', dest='alphaVar', help="Alpha Variable", required=False, default=0.1, type=float)
    return p.parse_args()


# Parse arguments
args = parse_args()

#Parse the train file
train_file = args.trainFile
train_data = []
train_cats = []
train_subcats = []
with open(train_file, 'r') as f:
    for line in f:
        l = line.split()
        train_cats.append(l[1])
        train_subcats.append(l[2])
        train_data.append(" ".join(l[3:]))

#Parse the test file
test_file = args.testFile
test_data = []
test_cats = []
test_subcats = []
test_ids = []
with open(test_file, 'r') as f:
    for line in f:
        l = line.split()
        test_ids.append(l[0])
        test_cats.append(l[1])
        test_subcats.append(l[2])
        test_data.append(" ".join(l[3:]))

#Condition to run pipeline tests, if false, only testing/training will run
if args.isPipelineRun:
    if args.representation == 0:
        pipeline = Pipeline([
            ('tfidf', TfidfVectorizer()),
            ('clf', MultinomialNB()),
            ])
        #different parameters to test
        parameters = {
            'tfidf__min_df': (0.5,0.75,1, ),
            'tfidf__max_features': (None, 5000,10000,30000,),
            'tfidf__ngram_range': ((1,1), (1,2),),
            'tfidf__use_idf': (True, False),
            'tfidf__norm': ('l1', 'l2'),
            'clf__alpha': (.01,0.1),
            'clf__fit_prior': (True, ),
        }
    elif args.representation == 1:
        ###############################################################################
        # define a pipeline combining a text feature extractor with a simple
        # classifier
        pipeline = Pipeline([
            ('vect', CountVectorizer()),
            ('catent', InvCatEntTransformer(train_subcats)),
            ('clf', MultinomialNB()),
        ])

        #different parameters to test
        parameters = {
#            'vect__max_df': (0.5,),
            'vect__max_features': (None, 5000,10000,30000,),
            'vect__ngram_range': ((1, 1),(1,2),),
            'catent__norm': ('l1','l2'),
            'clf__alpha': (.01,0.1),
            'clf__fit_prior': (True, ),
        }
    elif args.representation == 2:
        ###############################################################################
        # define a pipeline combining the third feature extractor with the best parameters
        # for a svm classifier.
        pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', MultinomialNB()),
        ])

        #different parameters to test
        parameters = {
            'tfidf__min_df': (1, ),
            'tfidf__max_features': (None, 5000,10000,30000,),
            'tfidf__ngram_range': ((1,2),),
            'tfidf__tokenizer': (LemmaTokenizer(), ),
            'tfidf__use_idf': (True,False),
            'tfidf__norm': ('l1','l2'),
            'tfidf__stop_words': ('english',),
            'clf__alpha': (.01,0.1),
            'clf__fit_prior': (True, ),
        }
    elif args.representation == 3:
        ###############################################################################
        # define a pipeline combining the third feature extractor with the best parameters
        # for a svm classifier.
        pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', MultinomialNB()),
        ])

        #different parameters to test
        parameters = {
            'tfidf__min_df': (0.5,0.75,1, ),
            'tfidf__max_features': (None, 5000,10000,30000,),
            'tfidf__ngram_range': ((4,4), (5,5)),
            'tfidf__tokenizer': (StemTokenizer(), ),
            'tfidf__use_idf': (True,False),
            'tfidf__norm': ('l1','l2'),
            'tfidf__stop_words': ('english', None),
            'tfidf__analyzer':('char_wb',),
            'clf__alpha': (.01,0.1),
            'clf__fit_prior': (True, ),
        }

    # multiprocessing requires the fork to happen in a __main__ protected
    # block

    # find the best parameters for both the feature extraction and the
    # classifier
    grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1, verbose=1)

    t0 = time()
    label_map = dict((k, i) for i, k in enumerate(set(train_cats)))
    train_labels = np.array([label_map[cat] for cat in train_cats])

    test_label_map = dict((k, i) for i, k in enumerate(set(test_cats)))
    test_labels = np.array([test_label_map[cat] for cat in test_cats])

    grid_search.fit(train_data, train_labels)

    print("Cross Validation Score: %0.3f" % grid_search.best_score_)

    pred = grid_search.best_estimator_.predict(test_data)
    print("Score on Test Data: %0.3f" %  metrics.accuracy_score(test_labels, pred))


    print("Best parameters set:")
    best_parameters = grid_search.best_estimator_.get_params()
    for param_name in sorted(parameters.keys()):
        print("\t%s: %r" % (param_name, best_parameters[param_name]))


else:
    # This is the train/test data.  We create the feature vectors here based on the ideal
    # parameters found during the pipeline runs.
    if args.representation == 0:
        vectorizer = TfidfVectorizer(ngram_range=(1, 1), norm='l2', min_df=1, max_features=5000, use_idf=True)
        vectorizer = TfidfVectorizer(ngram_range=(1, 1), norm='l2', min_df=1, max_features=None, use_idf=True)
        alphaVar = 0.1
        fitPriorValue = True
    elif args.representation == 1:
        featureset = CountVectorizer(max_df=0.5, max_features=5000,ngram_range=(1,1))
        featureset = CountVectorizer(max_df=0.5, max_features=None,ngram_range=(1,1))
        train_data = featureset.fit_transform(train_data)
        test_data = featureset.transform(test_data)
        vectorizer = InvCatEntTransformer(train_subcats,norm='l2')
        alphaVar = 0.1
        fitPriorValue = True
    elif args.representation == 2:
        vectorizer = TfidfVectorizer(ngram_range=(1, 2), norm='l2', tokenizer=LemmaTokenizer(), min_df=1, stop_words='english', max_features=5000,use_idf=True)
        vectorizer = TfidfVectorizer(ngram_range=(1, 2), norm='l2', tokenizer=LemmaTokenizer(), min_df=1, stop_words='english', max_features=None,use_idf=True)
        alphaVar = 0.1
        fitPriorValue = True
    else:
        vectorizer = TfidfVectorizer(analyzer='char_wb', ngram_range=(4, 4), tokenizer=StemTokenizer(), min_df=1, stop_words='english', max_features=5000,use_idf=True)
        vectorizer = TfidfVectorizer(analyzer='char_wb', ngram_range=(4, 4), tokenizer=StemTokenizer(), min_df=1, stop_words='english', max_features=None,use_idf=True)
        alphaVar = 0.01
        fitPriorValue = True

    train_vectors = vectorizer.fit_transform(train_data)
    test_vectors =  vectorizer.transform(test_data)

    # Use the inputted classifier or create a new one.
    if args.isTrain:
        clf = MultinomialNB(alpha=alphaVar,fit_prior=fitPriorValue)
        clf.fit(train_vectors, train_cats)
        _ = joblib.dump(clf, args.outputClassifierFile, compress=9)
    else:
        clf = joblib.load(args.inputClassifierFile)

    #output the results to the screen after predicting on test data.
    pred = clf.predict(test_vectors)
    print 'F1 score:', metrics.f1_score(test_cats, pred)
    print 'Accuracy:', metrics.accuracy_score(test_cats, pred)

    ## Create output file ReviewID, Real, Prediction, + if same, - if different
    f = open(args.outputFile, 'w')
    for t,c,p in zip(test_ids,test_cats,pred):
        if (c == p) :
            s = ", ".join([t,c,p,"+\n"])
            f.write(s)
        else:
            s = ", ".join([t,c,p,"-\n"])
            f.write(s)
    f.close()
"""
    print '--------------------------------------------------------------------------'
    print train_vectors.shape, test_vectors.shape
    print '--------------------------------------------------------------------------'
    print train_vectors.nnz / float(train_vectors.shape[0])
    try:
        print '--------------------------------------------------------------------------'
        print vectorizer.get_stop_words()
        print '--------------------------------------------------------------------------'
        print vectorizer.get_feature_names()
    except:
        pass

"""