#! /usr/bin/python

import os
import sys
import json
import re
from pprint import pprint

DEBUG = True
PATH = "data/js/tweets"

def createPath(path):
  if not os.path.isdir(path):
    os.mkdir(path)

def processArchive(path):

  if not os.path.isdir(path):
    print "Path '%s' not found." % path

  for (_, _, files) in os.walk(path):

    # index the files & ignore non-.js files
    for filename in files: 
      if not re.search('\d{4}_\d{2}.js', filename):
        print "Ignoring %s." % filename
        files.remove(filename) # remove from index, doesn't touch file
    print "Found %s months of tweets." % len(files)

    ''' TODO: fix this bit so that instead of writing out to 
        a new directory, it just adds the tweets to a file.
        basically merge in readjson() 
        make sure to filter out any mentions '''
    # write out the processed .js tweets to the /processedtweets directory
    createPath('processedtweets')
    for filename in files:
      w = open('processedtweets/' + filename, 'w')
      with open(path + '/' + filename, 'r') as f:
        f.readline() # ignore first line
        ''' TODO: check contents of first line '''
        theRest = f.read()
        if not DEBUG: 
          if filename == "2008_01.js": pprint.pprint(theRest)
        w.write(json.dumps(theRest))
      w.close()


def readjson(filename):
  json_data = open(filename, 'r')
  data = json.load(json_data)
  print data # LEFT OFF HERE
  json_data.close

''' TODO pull in the markov script to output x number of headlines to a file '''

def main():
  if len(sys.argv) != 1:
    print 'usage: $ python %s' % sys.argv[0]
    sys.exit(1)

  processArchive(PATH)

if __name__ == '__main__':
  main()