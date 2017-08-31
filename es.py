#!/usr/bin/python2.7
# encoding: utf-8
'''
@author:     Sid Probstein
@license:    MIT License (https://opensource.org/licenses/MIT)
@contact:    sidprobstein@gmail.com
'''

import argparse
import os
import glob
import sys
import json

from elasticsearch import Elasticsearch

#############################################

def main(argv):
    parser = argparse.ArgumentParser(description='Index json file(s) into elastic')
    parser.add_argument('-i', '--indexname', help="name of the index to use for this file")
    parser.add_argument('-t', '--type', help="type of item to index")
    parser.add_argument('-f', '--fid', help="use filename as id")
    parser.add_argument('-d', '--debug', help="produce additional diagnostic output")
    parser.add_argument('filespec', help="path or wildcard to the json file(s) you want to index")
    args = parser.parse_args()

    # initialize
    lstFiles = []
    nSent = 0

    if args.filespec:
        lstFiles = glob.glob(args.filespec)
    else:
        sys.exit()
    es = Elasticsearch('http://ec2-34-226-105-246.compute-1.amazonaws.com:9200/')
    print(args)
    for sFile in lstFiles:
        print(os.path.basename(sFile))
        if args.debug:
            print "index.py: reading:", sFile

        try:
            f = open(sFile, 'r')
        except Exception, e:
            print "index.py: error opening:", e
            continue

        # read the file
        try:
            jData = json.load(f)
        except Exception, e:
            print "index.py: error reading:", e
            f.close()
            continue

        # add the filename
        jData['filename'] = sFile

        print "index.py: indexing:", sFile,

        try:
            print(args)
            if args.fid:
                res = es.index(index=args.indexname, doc_type=args.type, id=sFile, body=jData)
            else:
                res = es.index(index=args.indexname, doc_type=args.type, id=os.path.splitext(os.path.basename(sFile))[0], body=jData)
            print(res['_id'], res['created'])
        except Exception, e:
            print "index.py: error:", e
            f.close()
            continue

        nSent = nSent + 1
        f.close()

    # end for
    if args.debug:
        print "index.py: indexed", nSent, "files"

# end main

#############################################

if __name__ == "__main__":
    main(sys.argv)

# end

