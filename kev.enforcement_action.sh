#!/bin/sh
j=0
for i in `cat pwsids.txt`
do 
/usr/bin/python3 ./fetch.py -o enforcement_action.json  https://iaspub.epa.gov/enviro/efservice/ENFORCEMENT_ACTION/PWSID/$i/JSON/
echo $i
date
j=$((j+1))
echo $j
done
