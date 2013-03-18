#!/usr/bin/env/python

import os
import re

DEBUG = True
path = "tweets"

def createPath(path):
  if not os.path.isdir(path):
    os.mkdir(path)

for (_, _, files) in os.walk(path):

	del _

	# index files & ignore non-.js files
	for filename in files: 
		if not re.search('\S\.js', filename): 
			print "Removing %s." % filename
			files.remove(filename)

	if DEBUG: print files

	# write out the processed .js tweets to the /processedtweets directory
	createPath('processedtweets')

	for filename in files:
		w = open('processedtweets/' + filename, 'w')
		with open(path + '/' + filename, 'r') as f:
			f.readline() # ignore first line
			theRest = f.readlines() 
			w.write(str(theRest)) # write everything else

	w.close()
	# Write the processed files to /processedtweets