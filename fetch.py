#!/usr/bin/python3
# encoding: utf-8
'''
@author:     Smartcurrent
@contact:    judah@smartcurrent.com
'''

#############################################
# fetch SDWIS data for a given state code, in json format, and write it out as json
# example usage: python jfetch_sdwis_json.py -o WS_MA_ALL.json https://iaspub.epa.gov/enviro/efservice/WATER_SYSTEM/STATE_CODE/MA/

# to do: make sure this produces valid JSON, e.g. [ {record1}, {record2], ... {recordN} ]

#############################################

from os.path import basename, splitext
#from SendEmail import SendEmail
import sys
import argparse
import json
import requests
import time
import xmltodict
from requests.exceptions import HTTPError
from requests.exceptions import ConnectionError
from requests.exceptions import InvalidSchema
#############################################

def main(argv):

    json_file = ''
    parser = argparse.ArgumentParser(description='Fetch json from EPA SDWIS, optionally retrieving all rows')
    parser.add_argument('-r', '--row', default=1, help="first row to retrieve")
    parser.add_argument('-o', '--outputfile', help="filename to write results to, in json format")
    parser.add_argument('-d', '--debug', help="provide debug information")
    parser.add_argument('uri', help="uri to the web service, without row specification")
    args = parser.parse_args()

    if args.outputfile:
        try:
            json_file = open(args.outputfile, 'a')
        except:
            msg = '{}: Cannot open {} for writing;'
            print(msg.format(basename(sys.argv[0]), args.outputfile))
            sys.exit(1)

    if args.debug:
        sendOutputTo = sys.stdout
    else:
        logfile = splitext(basename(sys.argv[0]))[0] + '.log'
        try:
            with open(logfile, 'w') as f:
                f.close()
        except:
            msg = '{}: Cannot open {} for writing.'
            print(msg.format(basename(sys.argv[0]), logfile), file=sendOutputTo, flush=True)
            sys.exit(1)

    # get row count
    nRecords = 0
    xSLEEP = 20
    nAttempts = 8
    j = 0

    while j < nAttempts:
        nRecords = 0
        #url = args.uri + 'COUNT/'
        url = args.uri

        try:
            response = requests.get(url)
            response.raise_for_status()
        except ConnectionError as err:
            msg = '{}: Error: {}'
            print(msg.format(basename(sys.argv[0]), err), file=sendOutputTo, flush=True)
            msg = '{}: Will Retry: {} of {}.'
            print(msg.format(basename(sys.argv[0]), j, nAttempts), file=sendOutputTo, flush=True)
            j+= 1
            time.sleep(xSLEEP * j)
            continue
        except HTTPError as err:
            msg = '{}: Error: {}'
            print(msg.format(basename(sys.argv[0]), err), file=sendOutputTo, flush=True)
            msg = '{}: Error: verify URL: {}'
            print(msg.format(basename(sys.argv[0]), url), file=sendOutputTo, flush=True)
            msg = '{}: Will Retry: {} of {}.'
            print(msg.format(basename(sys.argv[0]), j, nAttempts), file=sendOutputTo, flush=True)
            j+= 1
            time.sleep(xSLEEP * j)
            continue
        except InvalidSchema as err:
            msg = '{}: Error: {}'
            print(msg.format(basename(sys.argv[0]), err), file=sendOutputTo, flush=True)
            msg = '{}: Check Url: {}'
            print(msg.format(basename(sys.argv[0]), url), file=sendOutputTo, flush=True)
            SendEmail.SendEmail(msg.format(basename(sys.argv[0]), err))
            sys.exit(1)
        finally:
            pass

        if response.ok:
            # response is in xml format... ick...
            
            jData = json.loads(response.content.decode('utf-8'))
            json_file.write(str(jData)+'\n')

            #xDoc = xmltodict.parse(response.content)
            #nRecords = int(xDoc[u'Envirofacts'][u'RequestRecordCount'])
            #msg = '{}: Returned: {} records'
            #print(msg.format(basename(sys.argv[0]), nRecords), file=sendOutputTo, flush=True)
            #if nRecords == 0:
            #    msg = '{}: That is odd exiting, check {}.'
            #    print(msg.format(basename(sys.argv[0])), file=sendOutputTo, flush=True)
            #    SendEmail.SendEmail(msg.format(basename(sys.argv[0])))
            #    sys.exit(1)
            j = nAttempts
        else:
            msg = '{}: Failed getting url: {}'
            print(msg.format(basename(sys.argv[0])), file=sendOutputTo, flush=True)
            sys.exit(1)
        response.close()

        # initialize
        msg = '{}: done!'

        json_file.close()

# end main

#############################################

if __name__ == "__main__":
    main(sys.argv)

# end

