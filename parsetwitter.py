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
  ''' Crawls data dir and returns list of tweet files '''

  if not os.path.isdir(path):
    print "Path '%s' not found." % path

  for (_, _, files) in os.walk(path):

    # index the files & ignore non-.js files
    for filename in files: 
      if not re.search('\d{4}_\d{2}.js', filename):
        print "Ignoring %s." % filename
        files.remove(filename) # remove from index, doesn't touch file
    print "Found %s months of tweets." % len(files)

  return files 

def parseFiles(files, path):
  ''' Writes all tweets to text file '''
  
  w = open('justTheTweets.txt', 'a')
  for filename in files:
    with open(path + '/' + filename, 'r') as f:
      f.readline() # ignore the first line
       # parse the rest
      w.write(parseTweets(f))
  w.close()

def parseTweets(f):
  ''' Returns text of all tweets in a given file object'''
  tweets = []
  json_data = json.load(f)
  for tweet in json_data: 
    tweets.append(tweet['text'].encode('ascii', 'ignore'))
  if DEBUG: print tweets[0]
  return "\n".join(tweets)

''' TODO pull in the markov script to output x number of headlines to a file '''

def main():
  if len(sys.argv) != 1:
    print 'usage: $ python %s' % sys.argv[0]
    sys.exit(1)

  fileList = processArchive(PATH)
  parseFiles(fileList, PATH)

if __name__ == '__main__':
  main()