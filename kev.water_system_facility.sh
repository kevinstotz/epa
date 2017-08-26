#!/bin/sh

j=0
for i in `cat pwsids.txt`
do ./fetch.py -o water_system_facility.json  https://iaspub.epa.gov/enviro/efservice/WATER_SYSTEM_FACILITY/PWSID/$i/JSON/
((j=j+1))
echo $j
date
done
