#!/usr/bin/python
import argparse
import glob
from elasticsearch import Elasticsearch
import codecs
import re
import sys
import json
import requests
import subprocess
import os
from mysql2Json import MysqlPython
from time import sleep
from datetime import datetime
from datetime import timedelta


MAX_ATTEMPTS=5
table=''
STATUS_TABLE=''
UPDATE_TIME_DELTA=10
SLEEP_TIME=5
TABLE=''
PRIMARY_KEYS=''
FIELDS=''
mysql = MysqlPython()
pwsid = -1


def es(data):
        args = {}
        args = {'fid':'','type': 'ws', 'id': '', 'indexname': 'kyw2'}
        args['fid'] = None
        args['type'] = 'ws'
        args['id'] = data.name
        args['indexname'] = 'kyw2'

        es = Elasticsearch('http://ec2-34-226-105-246.compute-1.amazonaws.com:9200/')
        jData = {}
        try:
            with open(data.name,'r') as json_file:
                jData = json.load(json_file)
        except Exception, e:
            print "index.py: error reading:", e

        # add the filename
        jData['filename'] = data.name
        print "index.py: indexing:", data.name,

        try:
            print(args)
            res = es.index(index=args['indexname'], doc_type=args['type'],  id=args['id'], body=jData)
        except Exception, e:
            print(e)

def get_water_system(pwsid, TABLE):
     query = 'SELECT * FROM ' + TABLE  + ' WHERE PWSID="' + str(pwsid) + '"'
     print(query)
     res = mysql.custom_query(query)
     if len(res) > 0:
        return res
     else:
        print("Record {}:Not Found: query={}".format(res, query))
        return res


def get_aggregates(pwsid, TABLE):
     if pwsid.isdigit():
        pwsid = str(pwsid[:1]);
        query = 'SELECT * FROM ' + TABLE  + ' WHERE STATE LIKE "' + str(pwsid) + '%"'
     else:
        pwsid = str(pwsid[:2]);
        query = 'SELECT * FROM ' + TABLE  + ' WHERE STATE="' + str(pwsid) + '"'
     print(query)
     res = mysql.custom_query(query)
     if len(res) > 0:
        return res
     else:
        print("Record {}:Not Found: query={}".format(res, query))
        return res



def get_city_names(pwsid, TABLE):
     query = 'call get_city_names("' + str(pwsid) + '")'
     print(query)
     res = mysql.custom_procedure(query)
     if len(res) > 0:
        return res
     else:
        print("Record {}:Not Found: query={}".format(res, query))
        return res


def get_county_names(pwsid, TABLE):
     query = 'SELECT COUNTY_SERVED FROM ' + TABLE  + ' WHERE PWSID="' + str(pwsid) + '"'
     print(query)
     res = mysql.custom_query(query)
     if len(res) > 0:
        return res
     else:
        print("Record {}:Not Found: query={}".format(res, query))
        return res


def get_contaminants(pwsid, TABLE):
     query = 'SELECT CONTAMINANT, DATE, LEVEL, SIGN, UNITS FROM ' + TABLE  + ' WHERE PWSID="' + str(pwsid) + '"'
     print(query)
     res = mysql.custom_query(query)
     if len(res) > 0:
        return res
     else:
        print("Record {}:Not Found: query={}".format(res, query))
        return res


def get_source_reservoir_info(pwsid, TABLE):
     query = 'SELECT FACILITY_ID,FACILITY_NAME,SDWIS_URI FROM ' + TABLE  + ' WHERE PWSID="' + str(pwsid) + '"'
     print(query)
     res = mysql.custom_query(query)
     if len(res) > 0:
        return res
     else:
        print("Record {}:Not Found: query={}".format(res, query))
        return res


def get_source_treatment_info(pwsid, TABLE):
     query = 'SELECT FACILITY_ID,FACILITY_NAME,SDWIS_URI FROM ' + TABLE  + ' WHERE PWSID="' + str(pwsid) + '"'
     print(query)
     res = mysql.custom_query(query)
     if len(res) > 0:
        return res
     else:
        print("Record {}:Not Found: query={}".format(res, query))
        return res


def get_violations(pwsid, TABLE):
     query = 'SELECT * FROM ' + TABLE  + ' WHERE PWSID="' + str(pwsid) + '"'
     print(query)
     res = mysql.custom_query(query)
     if len(res) > 0:
        return res
     else:
        print("Record {}:Not Found: query={}".format(res, query))
        return res


def get_enforcements(pwsid, violation_id, enforcement_id, TABLE):
     query = 'SELECT ENFORCEMENT_ACTION_TYPE_CODE, ENFORCEMENT_ACTION_TYPE_CODE_EXPLAIN, DATE_FORMAT(ENFORCEMENT_DATE, \'%Y-%m-%d)\'), ORIGINATOR_CODE, ENFORCEMENT_ID, SDWIS_URI, ENFORCEMENT_COMMENT_TEXT FROM ' + TABLE  + ' WHERE PWSID="' + str(pwsid) + '" AND VIOLATION_ID="'+violation_id+'" AND ENFORCEMENT_ID="'+enforcement_id+'"'
     print(query)
     res = mysql.custom_query(query)
     if len(res) > 0:
        return res
     else:
        print("Record {}:Not Found: query={}".format(res, query))
        return res


def get_treatments(pwsid, TABLE):
     query = 'SELECT COMMENTS, FACILITY_ID, OBJECTIVE, TREATMENT,TREATMENT_EXPLAIN FROM ' + TABLE  + ' WHERE PWSID="' + str(pwsid) + '"'
     print(query)
     res = mysql.custom_query(query)
     if len(res) > 0:
        return res
     else:
        print("Record {}:Not Found: query={}".format(res, query))
        return res


def get_zip_codes(pwsid, TABLE):
     query = 'SELECT ZIP_CODE FROM ' + TABLE  + ' WHERE PWSID="' + str(pwsid) + '"'
     print(query)
     res = mysql.custom_query(query)
     if len(res) > 0:
        return res
     else:
        print("Record {}:Not Found: query={}".format(res, query))
        return res


def get_next(id):
        query_select = 'SELECT PWSID FROM WATER_SYSTEMS WHERE id='+str(id)
        print(query_select)
        res = mysql.get_next(query_select)
        return res


id = 1

while (pwsid != 0):
        pwsid = get_next(id)
        #pwsid[0]['PWSID'] = 'MA6000000'
        outfile = open('json/'+pwsid[0]['PWSID'] + ".json", "w")
        print('id={}: PWSID={}'.format(id, pwsid))

        water_system = get_water_system(pwsid[0]['PWSID'], 'WATER_SYSTEMS')

        if not water_system:
            id=id + 1
            continue
        outfile.write('{')

        aggregates = get_aggregates(pwsid[0]['PWSID'], 'AGGREGATES')
        outfile.write('"AGGREGATES": ')
        json.dump(aggregates,outfile)
        outfile.write(',')
        
        outfile.write('"CITY_NAME": ')
        json.dump(water_system[0]['CITY_NAME'],outfile)
        outfile.write(',')
        
        outfile.write('"CITY_NAMES": ')
        city_names = get_city_names(pwsid[0]['PWSID'], 'CITY_NAMES')
        outfile.write('[')
        idx = 0
        
        for city in city_names:
           json.dump(city['CITY_SERVED'],outfile)
           idx = idx + 1
           if idx < len(city_names):
               outfile.write(',')
        outfile.write('],')

        outfile.write('"CONTAMINANTS": ')
        contaminants = get_contaminants(pwsid[0]['PWSID'], 'CONTAMINANTS')
        json.dump(contaminants,outfile)
        outfile.write(',')
        
        outfile.write('"COUNTY_NAME": ')
        json.dump(water_system[0]['COUNTY_NAME'],outfile)
        outfile.write(',')

        outfile.write('"COUNTY_NAMES": ')
        county_names = get_county_names(pwsid[0]['PWSID'], 'COUNTY_NAMES')
        outfile.write('[')
        idx=0
        for county in county_names:
           json.dump(county['COUNTY_SERVED'],outfile)
           idx = idx + 1
           if idx < len(county_names):
               outfile.write(',')
        outfile.write('],')

        outfile.write('"IS_SCHOOL": ')
        json.dump(water_system[0]['IS_SCHOOL'],outfile)
        outfile.write(',')

        outfile.write('"ORG_ADDRESS_LINE1": ')
        stri = water_system[0]['ORG_ADDRESS_LINE1']
        stri = stri.decode('cp1252', errors='ignore')
        json.dump(stri,outfile)
        outfile.write(',')

        outfile.write('"ORG_ADDRESS_LINE2": ')
        stri = water_system[0]['ORG_ADDRESS_LINE2']
        stri = stri.decode('cp1252', errors='ignore')
        json.dump(stri,outfile)
        outfile.write(',')

        outfile.write('"ORG_CCR_REPORT_URI": ')
        json.dump(water_system[0]['ORG_CCR_REPORT_URI'],outfile)
        outfile.write(',')

        outfile.write('"ORG_NAME": ')
        json.dump(water_system[0]['ORG_NAME'],outfile)
        outfile.write(',')

        outfile.write('"ORG_PHONE_NUMBER": ')
        json.dump(water_system[0]['ORG_PHONE_NUMBER'],outfile)
        outfile.write(',')

        outfile.write('"ORG_URI": ')
        json.dump(water_system[0]['ORG_URI'],outfile)
        outfile.write(',')

        outfile.write('"OUTSTANDING_PERFORMER": ')
        json.dump(water_system[0]['OUTSTANDING_PERFORMER'],outfile)
        outfile.write(',')

        outfile.write('"POPULATION_SERVED": ')
        json.dump(water_system[0]['POPULATION_SERVED'],outfile)
        outfile.write(',')

        outfile.write('"PWSID": ')
        json.dump(water_system[0]['PWSID'],outfile)
        outfile.write(',')

        outfile.write('"PWS_NAME": ')
        stri = water_system[0]['PWS_NAME']
        stri = stri.decode('cp1252', errors='ignore')
        json.dump(stri,outfile)
        outfile.write(',')

        outfile.write('"SDWIS_PULLDATE": ')
        json.dump("2017-08-17",outfile)
        outfile.write(',')

        outfile.write('"SDWIS_URI": ')
        json.dump(water_system[0]['SDWIS_URI'],outfile)
        outfile.write(',')
        
        outfile.write('"SOURCE_PURCHASED_PWSID": ')
        json.dump(water_system[0]['SOURCE_PURCHASED_PWSID'],outfile)
        outfile.write(',')

        outfile.write('"SOURCE_RESERVOIR_INFO": ')
        source_reservoir = get_source_reservoir_info(pwsid[0]['PWSID'], 'SOURCE_RESERVOIR')
        json.dump(source_reservoir,outfile)
        outfile.write(',')

        outfile.write('"SOURCE_TREATMENTPLANT_INFO": ')
        source_treatment = get_source_treatment_info(pwsid[0]['PWSID'], 'SOURCE_TREATMENTPLANT')
        json.dump(source_treatment,outfile)
        outfile.write(',')

        outfile.write('"STATE_CODE": ')
        json.dump(water_system[0]['STATE_CODE'],outfile)
        outfile.write(',')

        outfile.write('"TREATMENTS": ')
        treatments = get_treatments(pwsid[0]['PWSID'], 'TREATMENTS')
        json.dump(treatments,outfile)
        outfile.write(',')

        outfile.write('"VIOLATIONS": ')
        violations = get_violations(pwsid[0]['PWSID'], 'VIOLATIONS')
        for idx,violation in enumerate(violations):
            violations[idx]['ENFORCEMENTS'] = get_enforcements(violation['PWSID'],violation['VIOLATION_ID'],violation['RTC_ENFORCEMENT_ID'],'ENFORCEMENTS')
        json.dump(violations,outfile)
        outfile.write(',')

        outfile.write('"WATER_SOURCE_TYPE": ')
        json.dump(water_system[0]['WATER_SOURCE_TYPE'],outfile)
        outfile.write(',')

        outfile.write('"ZIP_CODE": ')
        json.dump(water_system[0]['ZIP_CODE'],outfile)
        outfile.write(',')

        outfile.write('"ZIP_CODES": ')
        zip_codes = get_zip_codes(pwsid[0]['PWSID'], 'ZIP_CODES')
        outfile.write('[')
        idx = 0
        for zip_code in zip_codes:
           json.dump(zip_code['ZIP_CODE'],outfile)
           idx = idx + 1
           if idx < len(zip_codes):
               outfile.write(',')
        outfile.write(']')

        outfile.write('}')
        outfile.close()
        es(outfile)
        id = id + 1
exit()
