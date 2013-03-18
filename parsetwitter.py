#!/usr/bin/env/python

import sys
import json

def readjson(filename):
  json_data = open(filename, 'r')
  data = json.load(json_data)
  print data # LEFT OFF HERE
  json_data.close

def readcsv(filename):
  tweets = []

  with open(filename, 'r') as f:
    i=0
    for line in f:
      if line != "\n":
        if i < 6: print line != "\n", "*** LINE: %s" % line
        l = line.split(',')

        #if i < 6: print "tweet: %s" % (l[0])
        i += 1

      #tweets.append(l[7])

def main():
  if len(sys.argv) != 2:
    print 'usage: ./%s filename' % sys.argv[0]
    sys.exit(1)

  filename = sys.argv[1]
  readjson(filename)

if __name__ == '__main__':
  main()