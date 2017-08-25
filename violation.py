#!/usr/bin/python3
import re
import sys
import json
import requests

from mysql import MysqlPython
from time import sleep
from datetime import datetime
from datetime import timedelta

TABLES = ("VIOLATION_ENF_ASSOC","LCR_SAMPLE","TREATMENT","LCR_SAMPLE_RESULT","SERVICE_AREA","GEOGRAPHIC_AREA","ENFORCEMENT_ACTION","VIOLATION","WATER_SYSTEM_FACILITY","WATER_SYSTEM")
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

def let_user_pick(tables):
    print("Please choose:")
    for idx, table in enumerate(tables):
        print("{}) {}".format(idx+1,table))
    i = int(input("Enter number: "))
    try:
        if 0 < int(i) <= len(tables):
           pass
        else:
           exit()
    except :
        exit()

    table=''
    primary_keys=''
    fields=''

    if i == 1:
        table="VIOLATION_ENF_ASSOC"
        STATUS_TABLE=table + '_status'
        primary_keys = {'1': 'PWSID','2': 'VIOLATION_ID','3': 'ENFORCEMENT_ID'}
        fields = {'1': 'PWSID','2': 'VIOLATION_ID','3': 'ENFORCEMENT_ID'}

    if i == 2:
        table="LCR_SAMPLE"
        STATUS_TABLE=table + '_status'
        primary_keys  = {'1': 'PWSID', '2': 'SAMPLE_ID'}
        fields = {'1': 'PWSID','2': 'SAMPLE_ID','3': 'SAMPLING_END_DATE','4':'SAMPLING_START_DATE','5':'RECONCILIATION_ID','6':'PRIMACY_AGENCY_CODE','7':'EPA_REGION'}

    if i == 3:
        table="TREATMENT"
        STATUS_TABLE=table + '_status'
        primary_keys = {'1': 'PWSID', '2': 'TREATMENT_ID','3': 'FACILITY_ID'}
        fields = {'1': 'PWSID','2': 'TREATMENT_ID','3': 'FACILITY_ID','4':'TREATMENT_OBJECTIVE_CODE','5':'TREATMENT_PROCESS_CODE','6':'COMMENTS_TEXT'}

    if i == 4:
        table = "LCR_SAMPLE_RESULT"
        STATUS_TABLE=table + '_status'
        primary_keys = {'1': 'PWSID', '2': 'SAMPLE_ID'}
        fields = {'1': 'PWSID','2': 'SAMPLE_ID','3': 'EPA_REGION','4':'PRIMACY_AGENCY_CODE','5':'CONTAMINANT_CODE','6':'RESULT_SIGN_CODE','7':'SAMPLE_MEASURE','8':'SAR_ID','9':'UNIT_OF_MEASURE'}

    if i == 5:
        table = "SERVICE_AREA"
        STATUS_TABLE=table + '_status'
        primary_keys = {'1': 'PWSID'} 
        fields = {'1': 'PWSID','2': 'EPA_REGION','3': 'IS_PRIMARY_SERVICE_AREA_CODE','4':'PRIMACY_AGENCY_CODE','5':'PWS_ACTIVITY_CODE','6':'PWS_TYPE_CODE', '7':'SERVICE_AREA_TYPE_CODE'}

    if i == 6:
        table = "GEOGRAPHIC_AREA"
        STATUS_TABLE=table = '_status'
        primary_keys = {'1': 'PWSID','2': 'GEO_ID'} 
        fields = {'1': 'PWSID','2': 'GEO_ID','3': 'ANSI_ENTITY_CODE','4':'AREA_TYPE_CODE','5':'CITY_SERVED','6':'COUNTY_SERVED', '7':'EPA_REGION','8': 'PRIMACY_AGENCY_CODE','9': 'PWS_ACTIVITY_CODE','10': 'PWS_TYPE_CODE','11':'STATE_SERVED','12':'TRIBAL_CODE','13':'ZIP_CODE_SERVED'}

    if i == 7:
        table = "ENFORCEMENT_ACTION"
        STATUS_TABLE=table + '_status'
        primary_keys = {'1': 'PWSID', '2': 'ENFORCEMENT_ID'}
        fields = {'1': 'PWSID','2': 'ENFORCEMENT_ID','3': 'ORIGINATOR_CODE','4':'ENFORCEMENT_DATE','5':'ENFORCEMENT_ACTION_TYPE_CODE','6':'ENFORCEMENT_COMMENT_TEXT'}

    if i == 8:
        table = "VIOLATION"
        STATUS_TABLE=table + '_status'
        primary_keys = {'1': 'PWSID', '2': 'VIOLATION_ID'}
        fields = {'1':  'PWSID', '2':  'VIOLATION_ID', '3':  'COMPL_PER_END_DATE', '4':  'CONTAMINANT_CODE', '5':  'CORRECTIVE_ACTION_ID', '6':  'EPA_REGION', '7':  'FACILITY_ID', '8':  'IS_HEALTH_BASED_IND', '9':  'IS_MAJOR_VIOL_IND', '10':  'LATEST_ENFORCEMENT_ID', '11':  'ORIGINATOR_CODE', '12':  'POPULATION_SERVED_COUNT', '13':  'POP_CAT_5_CODE', '14':  'PRIMACY_AGENCY_CODE', '15':  'PRIMARY_SOURCE_CODE', '16':  'PUBLIC_NOTIFICATION_TIER', '17':  'COMPLIANCE_STATUS_CODE', '18':  'PWS_ACTIVITY_CODE', '19':  'PWS_DEACTIVATION_DATE', '20':  'PWS_TYPE_CODE', '21':  'RTC_DATE', '22':  'RTC_ENFORCEMENT_ID', '23':  'RULE_CODE', '24':  'RULE_FAMILY_CODE', '25':  'RULE_GROUP_CODE', '26':  'SAMPLE_RESULT_ID', '27':  'SEVERITY_IND_CNT', '28':  'STATE_MCL', '29':  'UNIT_OF_MEASURE', '30':  'VIOLATION_CATEGORY_CODE', '31':  'VIOLATION_CODE', '32':  'COMPL_PER_BEGIN_DATE', '33':  'VIOL_MEASURE'}

    if i == 9:
        table = "WATER_SYSTEM_FACILITY"
        STATUS_TABLE=table + '_status'
        primary_keys = {'1': 'PWSID', '2': 'FACILITY_ID'}
        fields = {'1': 'PWSID', '2': 'FACILITY_ID', '3': 'FACILITY_ACTIVITY_CODE', '4': 'FACILITY_DEACTIVATION_DATE', '5': 'EPA_REGION', '6': 'FACILITY_NAME', '7': 'FACILITY_TYPE_CODE', '8': 'FILTRATION_STATUS_CODE', '9': 'IS_SOURCE_IND', '10': 'IS_SOURCE_TREATED_IND', '11': 'PRIMACY_AGENCY_CODE', '12': 'AVAILABILITY_CODE', '13': 'PWS_ACTIVITY_CODE', '14': 'PWS_DEACTIVATION_DATE', '15': 'PWS_TYPE_CODE', '16': 'SELLER_PWSID', '17': 'SELLER_PWS_NAME', '18': 'SELLER_TREATMENT_CODE', '19': 'STATE_FACILITY_ID', '20': 'SUBMISSION_STATUS_CODE', '21': 'WATER_TYPE_CODE'}

    if i == 10:
        table = "WATER_SYSTEM"
        STATUS_TABLE="status." + table
        primary_keys = {'1': 'PWSID'}
        fields = {'1': 'PWSID', '2': 'ADDRESS_LINE1', '3': 'ADDRESS_LINE2', '4': 'ADMIN_NAME', '5': 'ALT_PHONE_NUMBER', '6': 'CDS_ID', '7': 'CITY_NAME', '8': 'COUNTRY_CODE', '9': 'DBPR_SCHEDULE_CAT_CODE', '10': 'EMAIL_ADDR', '11': 'EPA_REGION', '12': 'FAX_NUMBER', '13': 'GW_SW_CODE', '14': 'IS_GRANT_ELIGIBLE_IND', '15': 'IS_SCHOOL_OR_DAYCARE_IND', '16': 'IS_WHOLESALER_IND', '17': 'LT2_SCHEDULE_CAT_CODE', '18': 'ORG_NAME', '19': 'OUTSTANDING_PERFORMER', '20': 'OUTSTANDING_PERFORM_BEGIN_DATE', '21': 'OWNER_TYPE_CODE', '22': 'PHONE_EXT_NUMBER', '23': 'PHONE_NUMBER', '24': 'POPULATION_SERVED_COUNT', '25': 'POP_CAT_11_CODE', '26': 'POP_CAT_2_CODE', '27': 'POP_CAT_3_CODE', '28': 'POP_CAT_4_CODE', '29': 'POP_CAT_5_CODE', '30': 'PRIMACY_AGENCY_CODE', '31': 'PRIMACY_TYPE', '32': 'PRIMARY_SOURCE_CODE', '33': 'PWS_ACTIVITY_CODE', '34': 'PWS_DEACTIVATION_DATE', '35': 'PWS_NAME', '36': 'PWS_TYPE_CODE', '37': 'SEASON_BEGIN_DATE', '38': 'SEASON_END_DATE', '39': 'SERVICE_CONNECTIONS_COUNT', '40': 'SOURCE_PROTECTION_BEGIN_DATE', '41': 'SOURCE_WATER_PROTECTION_CODE', '42': 'STATE_CODE', '43': 'SUBMISSION_STATUS_CODE', '44': 'ZIP_CODE'}

    return (STATUS_TABLE, table, primary_keys, fields)


def exists_in_db(id):
    query = 'SELECT PWSID, last_updated FROM ' + TABLE + ' WHERE PWSID="' + str(id) + '"'
    res = mysql.custom_query(query)
    if len(res) == 0:
        print("not found in DB={}:query={}".format(res,query))
        return '0','0'
    else:
        print("found in DB={}:query={}".format(res[0],query))
        return res[0]


def insert_into_db(query):
     res = mysql.custom_insert(query)
     if res > 0:
        print("Inserted row id:{}:query={}".format(res,query))
     else:
        print("Failed inserting {}:query={}".format(res,query))


def parse_json(json_data, url):
    data = json.loads(json_data)

    for record in data:
       if find_record(record) == 0:
         print("inserting")
         insert_record(record,url)
       else:
         print("updating")
         update_record(record,url)


def insert_record(data, url):
     query = ''
     for key, value in FIELDS.items():
         cleaned = re.sub(r'[^\u0000-\uFFFF]+', '', str(data[value]), flags=re.IGNORECASE)
         query = query + value + '="' + cleaned + '", '
     query = 'INSERT INTO ' + TABLE + ' SET ' + query + ' url="' + str(url) + '"'
     print(query)
     insert_into_db(query)


def find_record(data):
     if len(PRIMARY_KEYS) == 1:
         query = 'SELECT count(*) FROM ' + TABLE + ' WHERE ' + PRIMARY_KEYS['1'] + '="' + str(data[PRIMARY_KEYS['1']]) + '"'
     else:
         query = 'SELECT count(*) FROM ' + TABLE + ' WHERE '
         i = 1
         for key, value in PRIMARY_KEYS.items():
             if i < len(PRIMARY_KEYS):
               query = query + value + '="' + str(data[value]) + '" AND '
             else:
               query = query + value + '="' + str(data[value]) + '"'
             i = i + 1     

     res = mysql.custom_query(query)
     if res[0][0] > 0:
        print("Record {}:Found: query={}".format(res[0],query))
        return len(res)
     else:
        print("Record {}:Not Found: query={}".format(res[0], query))
        return 0


def update_record(data, url):
     query= 'UPDATE ' + TABLE + ' SET '

     i = 1
     for key, value in FIELDS.items():
         query = query + value + '="' + str(data[value]) + '" '
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

     return mysql.custom_query(query)  

def get_stats():
        sql = 'SELECT count(id) FROM ' + STATUS_TABLE + '  WHERE ' + TABLE + '=0'
        print(sql)
        records_remaining = mysql.custom_query(sql)
        sql = 'SELECT count(id) FROM ' + STATUS_TABLE + '  WHERE ' + TABLE + '=1'
        records_completed = mysql.custom_query(sql)
        sql = 'SELECT count(id) FROM ' + STATUS_TABLE
        records_total = mysql.custom_query(sql)

        return records_total,records_completed,records_remaining


def get_next():
        query_select = 'SELECT ' + FIELDS['1'] + ', ' + TABLE + ' FROM ' + STATUS_TABLE + ' WHERE ' + TABLE + '=0 order by ' + FIELDS['1'] + ' ASC limit 1 FOR UPDATE'
        query_update = 'UPDATE ' + STATUS_TABLE + ' set ' + TABLE + '=' + str(100) + ' WHERE ' + FIELDS['1'] + '=%s limit 1'
        res = mysql.get_next(query_select, query_update)
        return res


def update_status_in_db(pwsid, code):
   sql = 'UPDATE ' + STATUS_TABLE + ' set ' + TABLE + '=' + str(code) + ' WHERE ' + FIELDS['1'] + '="'+pwsid+'" limit 1'
   print(sql)
   res = mysql.custom_query(sql)
   return res


def get_contents(url):
        i = 0
        response = ''
        while (i < MAX_ATTEMPTS):
          i = i + 1
          try:
               response = requests.get(url)
               print("attempt->{}".format(i))
          except:
               print("Unexpected error:", sys.exc_info()[0])
               sleep(SLEEP_TIME)
               continue
          if len(response.text) > MAX_ATTEMPTS and response.status_code == 200:
               return i, response.text
          if response.text == '[]' and response.status_code == 200:
               print("good url, no results trying to get {}".format(url))
               update_status_in_db(pwsid, 3)
               return 0, "" 
          if i == MAX_ATTEMPTS:
               print("failed ({}) trying to get {}".format(response.status_code, url))
               print(response.text)
               update_status_in_db(pwsid, 2)
               return 0, "" 
          sleep(SLEEP_TIME)
        return 10, "" 


(STATUS_TABLE, TABLE, PRIMARY_KEYS, FIELDS) = let_user_pick(TABLES)

id=1
while (pwsid != 0):
        total, complete, remaining = get_stats()
        pwsid = get_next()
        print('ID={}: (record {} of {}) PWSID={}'.format(id, remaining, total, pwsid))
        id = id + 1
        if pwsid == None:
            print("done")
            break
        sid, last_updated = exists_in_db(pwsid)
        #if len(last_updated) < 7:
        #    delta = datetime.now() -  timedelta(seconds=UPDATE_TIME_DELTA+1)
        #else:
        #    delta = datetime.now() - last_updated
        #if sid != '0':
        #    if delta.seconds < UPDATE_TIME_DELTA:
        #       print("already updated:{}".format(delta.seconds))
        #       continue
        #    else:
        #       print("Will Update:  seconds since last update={}".format(delta.seconds))
        #else:
        url = 'https://iaspub.epa.gov/enviro/efservice/'+TABLE+'/PWSID/' + pwsid + '/JSON/'
        results, contents = get_contents(url)
        print("results=",results)
        if results > 0:
            parse_json(str(contents), url)
            update_status_in_db(pwsid, 1)
        if results == 10:
            update_status_in_db(pwsid, 10)
exit()
