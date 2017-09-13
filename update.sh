#!/bin/sh -xv
PYTHON=`which python`
MYSQL=`which mysql`
#$MYSQL -u kazrootuser -h kaz16mysqlmedium.ckh7idnurzxi.us-west-2.rds.amazonaws.com -pGAS23ips < KYW_Build_Tables.sql
$MYSQL -u kazrootuser -h kaz16mysqlmedium.ckh7idnurzxi.us-west-2.rds.amazonaws.com -pGAS23ips < KYW_Fill_Tables.sql
$PYTHON ./2json.py
$PYTHON ./es.py  -i kyw2 -d debug -t ws  "json/MA6000000.json"
