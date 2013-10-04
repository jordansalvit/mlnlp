#!/usr/bin/python
from __future__ import division
import numpy as np 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics

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

# extract TF-IDF vectors of unigram tokens
vectorizer = TfidfVectorizer()
train_vectors = vectorizer.fit_transform(train_data)
test_vectors =  vectorizer.transform(test_data)
print train_vectors.shape, test_vectors.shape
# non-zero components
print train_vectors.nnz / float(train_vectors.shape[0])

clf = MultinomialNB(alpha=.01)
clf.fit(train_vectors, train_cats)
pred = clf.predict(test_vectors)
print 'F1 score:', metrics.f1_score(test_cats, pred)
print 'Accuracy:', metrics.accuracy_score(test_cats, pred)
print pred
