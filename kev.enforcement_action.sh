#!/bin/sh
j=0
for i in `cat pwsids.txt`
do ./fetch.py -o enforcement_action.json  https://iaspub.epa.gov/enviro/efservice/ENFORCEMENT_ACTION/PWSID/$i/JSON/
((j=j+1))
echo $j
date
done
