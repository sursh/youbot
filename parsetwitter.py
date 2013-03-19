#!/usr/bin/env/python

import sys
import json

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
  readjson(filename)

if __name__ == '__main__':
  main()