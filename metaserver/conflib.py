#!/usr/bin/env python3

import json

def loadconfig(filename):
	conffile = open(filename, "r")
	config = json.load(conffile)
	conffile.close()
	return config
