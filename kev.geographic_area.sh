#!/bin/sh

for i in `cat pwsids.txt`; do ./fetch.py -o geographic_area.json  https://iaspub.epa.gov/enviro/efservice/GEOGRAPHIC_AREA/PWSID/$i/JSON/; done
