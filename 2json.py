#!/usr/bin/python
import codecs
import re
import sys
import json
import requests

from mysql2Json import MysqlPython
from time import sleep
from datetime import datetime
from datetime import timedelta


TABLES = ("VIOLATION_ENF_ASSOC","LCR_SAMPLE","TREATMENT","LCR_SAMPLE_RESULT","SERVICE_AREA","GEOGRAPHIC_AREA","ENFORCEMENT_ACTION","VIOLATION","WATER_SYSTEM_FACILITY","WATER_SYSTEM","ENFORCEMENT")
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



def get_water_system(pwsid, TABLE):
     query = 'SELECT * FROM ' + TABLE  + ' WHERE PWSID="' + str(pwsid) + '"'
     print(query)
     res = mysql.custom_query(query)
     if len(res) > 0:
        return res
     else:
        print("Record {}:Not Found: query={}".format(res, query))
        return res


def get_aggregates(pwsid,AGGREGATES):
     query = "SELECT AGGREGATE, CONTAMINANT, DATE, UNITS, LEVEL FROM AGGREGATES WHERE PWSID='" + str(pwsid) + "'"
     print(query)
     res = mysql.custom_query(query)
     if len(res) > 0:
        return res
     else:
        print("Record {}:Not Found: query={}".format(res, query))
        return res


def get_city_names(pwsid, TABLE):
     query = 'SELECT CITY_SERVED FROM ' + TABLE  + ' WHERE PWSID="' + str(pwsid) + '"'
     print(query)
     res = mysql.custom_query(query)
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


def get_treatments(pwsid, TABLE):
     query = 'SELECT COMMENTS, FACILITY_ID, OBJECTIVE, OBJECTIVE_EXPLAINE,TREATMENT,TREATMENT_EXPLAIN FROM ' + TABLE  + ' WHERE PWSID="' + str(pwsid) + '"'
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
        query_select = 'SELECT PWSID  FROM kyw0817.GAP WHERE id='+str(id)
        print(query_select)
        res = mysql.get_next(query_select)
        return res


AGGREGATES = ('AGGREGATE', 'CONTAMINANT', 'DATE', 'UNITS', 'LEVEL')
id = 4995
id = 1
TABLES = ('AGGREGATES','TREATMENTS','ZIP_CODES','CITY_NAMES','CONTAMINANTS','SOURCE_TREATMENTPLANT_INFO','SOURCE_RESERVOIR_INFO','COUNTY_NAMES')

while (pwsid != 0):
        pwsid = get_next(id)
        outfile = open('json/'+pwsid[0]['PWSID'] + ".json", "w")
        print('id={}: PWSID={}'.format(id, pwsid))

        water_system = get_water_system(pwsid[0]['PWSID'], 'WATER_SYSTEMS')

        if not water_system:
            id=id + 1
            continue
        outfile.write('{')

        aggregates = get_aggregates(pwsid[0]['PWSID'], AGGREGATES)
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
        json.dump(county_names,outfile) 
        outfile.write(',')

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
        id = id + 1
exit()
