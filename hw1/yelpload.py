#!/usr/bin/python
# -*- coding: utf-8 -*-

import _mysql
import MySQLdb as mdb
import sys
import json


con = None
cursor = None
f = open('../../../../research/Yelp_Academic/yelp_academic_dataset.json', 'r')
x, y, z = 1, 1, 1
con = mdb.connect('localhost', 'root', '', 'r_yelp')
cursor = con.cursor()
#cursor.execute("truncate table reviews;")
cursor.execute("truncate table businesses;")
con.commit()
for line in f:
    jsline = json.loads(line)
#		if (x < 100) & (jsline["type"] == 'user'):
#			cursor.execute("insert into Users (userid, name, review_count, average_stars, useful, funny, cool) values (%s,%s,%s,%s,%s,%s,%s)",(jsline["user_id"],jsline["name"],jsline["review_count"],jsline["average_stars"],jsline["votes"]["useful"],jsline["votes"]["funny"],jsline["votes"]["cool"]))
#			con.commit()
#			x=x+1
    if (jsline["type"] == 'review') & (y<0):
        reviewText = None
        try:
            reviewText = unicode(jsline["text"])
            cursor.execute(
                "insert into Reviews (review_id, businessid, userid, stars, review, review_date, useful, funny, cool) values (%s, %s,%s,%s,%s,%s,%s,%s,%s)",
                (jsline["review_id"], jsline["business_id"], jsline["user_id"], jsline["stars"], reviewText, jsline["date"],
                 jsline["votes"]["useful"], jsline["votes"]["funny"], jsline["votes"]["cool"]))
            con.commit()
        except:
            pass
        y = y + 1
    elif (jsline["type"] == 'business'):
        neighborhood = ""
        for n in jsline["neighborhoods"]:
            neighborhood = n
        category = ""
        for c in jsline["categories"]:
            category = c
        school = ""
        for s in jsline["schools"]:
            school = s
        try:
            cursor.execute(
                "insert into Businesses (businessid, name, neighborhoods, full_address, city, state, latitude, longitude, stars, review_count, photo_url, categories, open, schools, url) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (jsline["business_id"], jsline["name"], neighborhood, jsline["full_address"], jsline["city"],
                 jsline["state"], jsline["latitude"], jsline["longitude"], jsline["stars"], jsline["review_count"],
                 jsline["photo_url"], category, jsline["open"], school, jsline["url"]))
            con.commit()
        except:
            pass
        z = z + 1

if cursor:
    cursor.close()

if con:
    con.close()