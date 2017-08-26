#!/bin/sh

j=0
for i in `cat pwsids.txt`
do ./fetch.py -o violation.json  https://iaspub.epa.gov/enviro/efservice/VIOLATION/PWSID/$i/JSON/
((j=j+1))
echo $j
date
done
