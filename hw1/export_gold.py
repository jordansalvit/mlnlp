#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import MySQLdb as mdb
import sys
import collections
import argparse


def parse_args():
    p = argparse.ArgumentParser(description="Export Files for different algorithms")
    p.add_argument('-a', '--algo', dest='algorithm', help="Which document method are we exporting for? 0-3",
                   required=False)
    p.add_argument('-m', '--max', dest='maxRows', help="Max number of rows in data set", required=False, default=500)
    return p.parse_args()


def getBagOfWords(txt):
    bagofwords = collections.Counter(re.findall(r'\w+', txt))
#    print bagofwords
    return bagofwords


def getDataSet(start, limit, cursor):
    cursor.execute(
        """select * from (
            (SELECT r.review_id, r.review, 'CMU' as school
            FROM Reviews r inner join businesses b on b.businessid = r.businessid
            where b.schools = 'Carnegie Mellon University' and categories = 'Restaurants'
            order by review_id
            limit %s, %s)
            union
            (SELECT r.review_id, r.review, 'Columbia' as school
            FROM Reviews r inner join businesses b on b.businessid = r.businessid
            where b.schools = 'Columbia University' and categories = 'Restaurants'
            order by review_id
            limit %s, %s)
            union
            (SELECT r.review_id, r.review, 'Harvard' as school
            FROM Reviews r inner join businesses b on b.businessid = r.businessid
            where b.schools = 'Harvard University' and categories = 'Restaurants'
            order by review_id
            limit %s, %s)
            union
            (SELECT r.review_id, r.review, 'Princeton' as school
            FROM Reviews r inner join businesses b on b.businessid = r.businessid
            where b.schools = 'Princeton University' and categories = 'Restaurants'
            order by review_id
            limit %s, %s)
            union
            (SELECT r.review_id, r.review, 'Urbana' as school
            FROM Reviews r inner join businesses b on b.businessid = r.businessid
            where b.schools = 'University of Illinois - Urbana-Champaign' and categories = 'Restaurants'
            order by review_id
            limit %s, %s)
            ) d;""",
        (start, limit, start, limit, start, limit, start, limit, start, limit))
    reviews = cursor.fetchall()
    return reviews

args = parse_args()

con = None
cursor = None
con = mdb.connect('localhost', 'root', '', 'r_yelp', charset='utf8')
cursor = con.cursor()

f = open('complete_set.txt', 'w')

#Write the complete file with answers
reviews = getDataSet(0,args.maxRows,cursor)
for review in reviews:
    try:
        f.write("%s " % review[0])
        f.write("%s " % review[2])
        listOfWords = re.findall(r'\w+', review[1])
        for word in listOfWords:
            f.write("%s " % word)
        f.write("\n")
    except:
        print "Error with encode - first "
f.close()

train = open('train_gold.txt', 'w')
reviews = getDataSet(0,225,cursor)
for review in reviews:
    try:
        train.write("%s " % review[0])
        train.write("%s " % review[2])
        listOfWords = re.findall(r'\w+', review[1])
        for word in listOfWords:
            train.write("%s " % word)
        train.write("\n")
    except:
        print "Error with encode - second"
train.close()

test = open('test_gold.txt', 'w')
reviews = getDataSet(225,75,cursor)
for review in reviews:
    try:
        test.write("%s " % review[0])
        test.write("%s " % review[2])
        listOfWords = re.findall(r'\w+', review[1])
        for word in listOfWords:
            test.write("%s " % word)
        test.write("\n")
    except:
        print "Error with encode - third"
test.close()

bag_train = open('train_bagofwords.txt', 'w')
reviews = getDataSet(0,225,cursor)
for review in reviews:
    try:
        arrayOfWords = getBagOfWords(review[1])
        bag_train.write("%s " % review[0])
        for word in arrayOfWords:
            bag_train.write("%s " % word)
        bag_train.write("\n")
    except:
        print "Error with encode - fourth"
bag_train.close()

bag_test = open('test_bagofwords.txt', 'w')
reviews = getDataSet(225,75,cursor)
for review in reviews:
    try:
        arrayOfWords = getBagOfWords(review[1])
        bag_test.write("%s " % review[0])
        for word in arrayOfWords:
            bag_test.write("%s " % word)
        bag_test.write("\n")
    except:
        print "Error with encode - fifth"
bag_test.close()

if cursor:
    cursor.close()

if con:
    con.close()