#!/usr/bin/python
import codecs
import re
import csv
import sys

from mysql import MysqlPython
from time import sleep
from datetime import datetime
from datetime import timedelta


def insert_into_db(query):
     res = mysql.custom_insert(query)
     if res > 0:
        print("Inserted row id:{}:query={}".format(res,query))
     else:
        print("Failed inserting {}:query={}".format(res,query))

def insert_record(data, url):
     query = ''
     for key, value in FIELDS.items():
         d = data[value]
         if type(d) == 'NoneType':
            pass
         elif type(d) == int or d == 'NoneType':
            pass
         elif type(d) == unicode:
            d = d.encode('utf-8', errors='replace')
         else:
            pass
            #d = d.decode('unicode_escape').encode('ascii','ignore')
         query = query + value + '="' + str(d) + '", '
     query = 'INSERT INTO ' + TABLE + ' SET ' + query + ' url="' + str(url) + '"'
     print(query)
     insert_into_db(query)


def update_record(data, url):

     query= 'UPDATE ' + TABLE + ' SET '
     i = 1
     for key, value in FIELDS.items():
         d = data[value]
         if type(d) == 'NoneType':
            pass
         elif type(d) == int or d == 'NoneType':
            pass
         elif type(d) == unicode:
            d = d.encode('utf-8', errors='replace')
         else:
            pass
         query = query + value + '="' + str(d) + '" '
         if i < len(FIELDS):
             query = query + ', '
         i = i + 1

     query = query + ' WHERE '
     if len(PRIMARY_KEYS) == 1:
         query = query + PRIMARY_KEYS['1'] + '="' + str(data[PRIMARY_KEYS['1']]) + '" LIMIT 1 '
     else:
         i = 1
         for key, value in PRIMARY_KEYS.items():
             if i < len(PRIMARY_KEYS):
               query = query + value + '="' + str(data[value]) + '" AND '
             else:
               query = query + value + '="' + str(data[value]) + '" LIMIT 1'
             i = i + 1

     print(query)
     return mysql.custom_query(query)


def get_next():
        query_select = 'SELECT ' + FIELDS['1'] + ', ' + TABLE + ' FROM ' + STATUS_TABLE + ' WHERE ' + TABLE + '=0 order by ' + FIELDS['1'] + ' ASC limit 1 FOR UPDATE'
        print(query_select)
        query_update = 'UPDATE ' + STATUS_TABLE + ' set ' + TABLE + '=' + str(100) + ' WHERE ' + FIELDS['1'] + '=%s limit 1'
        print(query_update)
        res = mysql.get_next(query_select, query_update)
        return res


id=1
css_file = 'cities.csv'

with open(csv_file, newline='\n') as csvfile:
     cityreader = csv.reader(csvfile, delimiter=',', quotechar='"')
     for row in cityreader:
         print((row))
         exit()
exit()
