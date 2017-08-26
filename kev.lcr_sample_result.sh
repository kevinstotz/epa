#!/bin/sh

j=0
for i in `cat pwsids.txt`
do
./fetch.py -o lcr_sample_result.json  https://iaspub.epa.gov/enviro/efservice/LCR_SAMPLE_RESULT/PWSID/$i/JSON/
((j=j+1))
echo $j
date
done
