#! /usr/bin/python

import os
import sys
import json
import re
from pprint import pprint
import markovgenerator

DEBUG = True
PATH = "."
TWEETLIST = "justTheTweets.txt"


def processArchive(path):
  ''' Crawls /data from twitter and returns list of files 
      containing tweets '''

  if not os.path.isdir(path):
    print "Path '%s' not found." % path
    sys.exit(1)

  tweetfiles = []

  for (root, _, files) in os.walk(path):
    # index the files & ignore non-.js files
    for filename in files[:]: 
      if re.search('\d{4}_\d{2}.js', filename):
        tweetfiles.append(os.path.join(root, filename))
  
  print "* Found %s months of tweets." % len(files)
  return tweetfiles 


def parseFiles(files, path):
  ''' Writes text of tweets to a single file '''

  if os.path.isfile(TWEETLIST):
    print "* Using existing file %s." % TWEETLIST
  
  else:
    w = open(TWEETLIST, 'w')
    print "* Writing tweets to %s." % TWEETLIST

    for filename in files:
      with open(filename, 'r') as f:
        f.readline() # ignore the first line; it's gibberish
        w.write(parseTweets(f))

    w.close()


def cleanTweets(line):
  ''' Removes mentions, replies, and links '''

  line = line.split(' ')

  for token in line[:]:
    if token and (token[0] == '@' or re.search(".*https*://", token)):
        line.remove(token)

  return ' '.join(line)


def parseTweets(f):
  ''' Returns text of all tweets in a given file object'''

  tweets = []
  json_data = json.load(f)
  
  for tweet in json_data: 
    payload = tweet['text'].encode('ascii', 'ignore')
    payload = cleanTweets(payload)
    tweets.append(payload)
  
  return "\n".join(tweets)


def main():

  if len(sys.argv) != 2:
    print 'usage: $ python %s <number_of_tweets>' % sys.argv[0]
    sys.exit(1)

  fileList = processArchive(PATH)
  parseFiles(fileList, PATH)
  markovgenerator.markovIt(TWEETLIST, int(sys.argv[1]))

if __name__ == '__main__':
  main()