#!/bin/sh

for i in `cat pwsids.txt`; do ./fetch.py -o treatment.json  https://iaspub.epa.gov/enviro/efservice/TREATMENT/PWSID/$i/JSON/; done
