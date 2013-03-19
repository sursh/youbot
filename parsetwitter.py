#! /usr/bin/python

import os
import sys
import json
import re
from pprint import pprint
import markovgenerator

DEBUG = True
PATH = "data/js/tweets"
TWEETLIST = "justTheTweets.txt"

def createPath(path):
  if not os.path.isdir(path):
    os.mkdir(path)

def processArchive(path):
  ''' Crawls data dir and returns list of tweet files '''

  if not os.path.isdir(path):
    print "Path '%s' not found." % path
    sys.exit(1)

  for (_, _, files) in os.walk(path):

    # index the files & ignore non-.js files
    for filename in files: 
      if not re.search('\d{4}_\d{2}.js', filename):
        print "* Ignoring %s." % filename
        files.remove(filename) # remove from index, doesn't touch file
    print "* Found %s months of tweets." % len(files)

  return files 

def parseFiles(files, path):
  ''' Writes all tweets to text file '''
  
  w = open(TWEETLIST, 'a')
  for filename in files:
    with open(path + '/' + filename, 'r') as f:
      f.readline() # ignore the first line
      w.write(parseTweets(f))
  print "* Wrote tweets to %s." % TWEETLIST
  w.close()

def removeMentions(line):
  print line[0]

  #  if it's @, remove it and the rest of the chars until you hit a space

  return line

def parseTweets(f):
  ''' Returns text of all tweets in a given file object'''
  tweets = []
  json_data = json.load(f)
  for tweet in json_data: 
    payload = tweet['text'].encode('ascii', 'ignore')
    removeMentions(payload)
    tweets.append(payload)
  #if DEBUG: print "%d: %s" % (len(tweets[0]), tweets[0])
  return "\n".join(tweets)

def main():
  if len(sys.argv) != 1:
    print 'usage: $ python %s' % sys.argv[0]
    sys.exit(1)

  fileList = processArchive(PATH)
  parseFiles(fileList, PATH)
  markovgenerator.markovIt(TWEETLIST)

if __name__ == '__main__':
  main()