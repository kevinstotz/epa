#!/bin/sh

for i in `cat pwsids.txt`
do 
./fetch.py -o service_area.json  https://iaspub.epa.gov/enviro/efservice/SERVICE_AREA/PWSID/$i/JSON/
done
