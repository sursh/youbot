#!/usr/bin/env/python

import os
import re

path = "tweets"

for (path, dirs, files) in os.walk(path):

	print "before: %s" % files

	for eachfile in files: 
		if not re.search('\S\.js', eachfile): 
			print "removing %s" % eachfile
			files.remove(eachfile)

	print "after %s" % files
