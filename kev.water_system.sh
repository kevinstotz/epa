#!/bin/sh

for i in `cat pwsids.txt`; do ./fetch.py -o water_system.json  https://iaspub.epa.gov/enviro/efservice/WATER_SYSTEM/PWSID/$i/JSON/; done
