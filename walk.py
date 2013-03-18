#!/usr/bin/env/python

import os

path = "/Users/sasha/code/markovtwitter/tweets"

for (path, dirs, files) in os.walk(path):
	print files