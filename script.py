#! /usr/bin/python

import os
import sys
import json
import re
import markovgenerator

DEBUG = True
PATH = "."
TWEETLIST = "justTheTweets.txt"


def process_archive(path):
    ''' Crawls /data from twitter and returns list of files
            containing tweets '''

    if not os.path.isdir(path):
        print "Path '%s' not found." % path
        sys.exit(1)

    tweetfiles = []

    # index the files & ignore non-.js files
    for (root, _, files) in os.walk(path):
        for filename in files[:]:
            if re.search('\d{4}_\d{2}.js', filename):
                print "joining ", root, filename
                tweetfiles.append(os.path.join(root, filename))


    print "* Found %s months of tweets." % len(files)
    return tweetfiles


def parse_files(files):
    ''' Writes text of tweets to a single file '''

    if os.path.isfile(TWEETLIST):
        print "* Using existing file %s." % TWEETLIST

    else:
        for filename in files:
            with open(TWEETLIST, 'w') as w:
                print "* Writing tweets to %s." % TWEETLIST
                with open(filename, 'r') as f:
                    f.readline() # ignore the first line; it's gibberish
                    w.write(parse_tweets(f))

def clean_tweets(line):
    ''' Removes mentions, replies, RTs, and links '''

    line = line.split(' ')

    for token in line[:]:
        if token and (token[0] == '@' or token == 'RT'  \
                      or re.search(".*https*:", token)):
            line.remove(token)

    return ' '.join(line)


def parse_tweets(f):
    ''' Returns text of all tweets in a given file object'''

    tweets = []
    json_data = json.load(f)

    for tweet in json_data:
        payload = tweet['text'].encode('ascii', 'ignore')
        payload = clean_tweets(payload)
        tweets.append(payload)

    return "\n".join(tweets)


def main():

    if len(sys.argv) != 2:
        print 'usage: $ python %s <number_of_tweets>' % sys.argv[0]
        sys.exit(1)

    filelist = process_archive(PATH)
    parse_files(filelist)
    markovgenerator.markov_it(TWEETLIST, int(sys.argv[1]))

if __name__ == '__main__':
    main()