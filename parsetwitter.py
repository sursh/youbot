#! /usr/bin/python

import os
import sys
import json
import re
from pprint import pprint

DEBUG = True
path = "data"

def createPath(path):
  if not os.path.isdir(path):
    os.mkdir(path)

def crawlPath(path):

  for (_, _, files) in os.walk(path):
    del _

    # index the files & ignore non-.js files
    for filename in files: 
      if not re.search('\S\.js', filename): 
        print "Ignoring %s." % filename
        files.remove(filename) # remove from index, doesn't touch file
    if DEBUG: print files

    # write out the processed .js tweets to the /processedtweets directory
    createPath('processedtweets')
    for filename in files:
      w = open('processedtweets/' + filename, 'w')
      with open(path + '/' + filename, 'r') as f:
        f.readline() # ignore first line
        theRest = f.read()
        if DEBUG: 
          if filename == "2008_01.js": pprint.pprint(theRest)
        w.write(json.dumps(theRest))
    w.close()

def readjson(filename):
  json_data = open(filename, 'r')
  data = json.load(json_data)
  print data # LEFT OFF HERE
  json_data.close

def main():
  if len(sys.argv) != 2:
    print 'usage: $ python %s filename' % sys.argv[0]
    sys.exit(1)

  filename = sys.argv[1]
  crawlPath(path)
  readjson(filename)

if __name__ == '__main__':
  main()