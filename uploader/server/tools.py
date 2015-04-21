#!/usr/bin/env python3

import json
import apilib
import random
import os
import base64
from urllib.request import HTTPError

def genfile(name, mtime, size, uuhash):
	f = {
		"name": name,
		"mtime": mtime,
		"size": size,
		"uuhash": uuhash
	}
	return f

def genfiles(starttime, stoptime, namepref):
	files = []
	namesuf = "1"
	while starttime < stoptime:
		dur = 60*20 + random.randint(-5*60,5*60)
		endtime = starttime + dur
		if endtime > stoptime:
			endtime = stoptime
		size = 2*1024*1024*1024+random.randint(-5,5)*192
		size = int(size - (((starttime + dur)-endtime)/(starttime + dur))*size)
		uuhash = base64.b64encode(os.urandom(16)).decode('ascii')
		
		files.append(genfile(namepref + "/" + namesuf + ".MTS", endtime, size, uuhash))
		
		namesuf = str(int(namesuf)+1)
		starttime = endtime
	return files

def genlec(lid, namepref = ""):
	files = []
	try:
		lec = apilib.lectures(lid)
	except HTTPError as err:
		print("Error at id " + str(lid) + ", Response: " + str(err))
		return []
	starttime = lec["time"]["timestamp"] - random.randint(5*60, 15*60)
	stoptime = lec["time"]["timestamp"] + lec["duration"]*60 + random.randint(5*60, 5*60)
	files = files + genfiles(starttime, stoptime, namepref)
	return files

def genlecs(lids):
	files = []
	namesuf = "1"
	for lid in lids:
		files = files + genlec(lid, namesuf)
		namesuf = str(int(namesuf)+1)
	return files

def genreq(request, data):
	req = {}
	req["request"] = request
	req["token"] = "aab8d0dc34b59ee9e804f1261a2da9a82feafb64054cd40c4a62fa0767aed228096e558b13452623579208ed33904c6762c4ad625c4e7b25c2b2688e2e5ebb0c"
	
	req["data"] = data
	return req

def genjreq(request, data):
	return json.dumps(genreq(request, data), indent=2)

def genlecsreq(lids):
	return genjreq('index', {"files": genlecs(lids)})

def genunindexed(starttime=None, endtime=None):
	data = {}
	if starttime != None:
		data['starttime'] = starttime
	if endtime != None:
		data['endtime'] = endtime
	return genjreq('getunindexed', data)
