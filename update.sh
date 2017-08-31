#!/bin/sh
PYTHON=`which python`
PYTHON ./2json.py
PYTHON ./es.py  -i kyw1 -d debug -t ws  "json/*.json"
