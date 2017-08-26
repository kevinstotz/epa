#!/bin/sh
j=0

for i in `cat pwsids.txt`
do ./fetch.py -o violation_assoc_enf.json  https://iaspub.epa.gov/enviro/efservice/VIOLATION_ENF_ASSOC/PWSID/$i/JSON/
((j=j+1))
echo $j
date
done

