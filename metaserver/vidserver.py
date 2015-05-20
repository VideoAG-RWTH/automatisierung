#!/usr/bin/env python3

#import cgitb
import json
import sys
import os

import conflib
import dblib
import authlib

def getdata():
#	form = cgi.FieldStorage()
#	return json.loads(form[key])
#	return json.loads(sys.argv[1])
	return json.loads(sys.stdin.read(int(os.environ["CONTENT_LENGTH"])))

class VideoagServer(object):
	def __init__(self, conffile, data):
		self.response = {"result":"", "data":{}}
		
		conf = conflib.loadconfig(conffile)
		self.db = dblib.DBConn(conf["db"])
		
		#cgitb.enable()
		#self.data = getdata(conf["meta"]["httpfield"])
		self.data = data
	
	def authuser(self):
		token = self.data["token"]
		self.uid = authlib.auth(self.db, token)
		if self.uid == 0:
			return False
		else:
			return True
	
	def serve(self):
#		try:
			if not self.authuser():
				self.error("user auth failed", rescode="403 Forbidden")
			self.handle()
			self.end("ok")
#		except KeyError as err:
#			self.error("KeyError", "KeyError: {0}".format(err), "400 Bad Request")
#		except Exception as err:
#			self.error("Exception", "Generell Exception: {0}".format(err), "500 Internal Server Error")
		
	def error(self, desc, moredesc=None, rescode=None):
		self.response["data"]["errordesc"] = desc
		self.response["data"]["moredesc"] = moredesc
		self.end("error", rescode)
	
	def end(self, result, rescode=None):
		self.response["result"] = result
		if rescode != None:
			print("Status:"+rescode)
		print("Content-Type: text/json")
		print()
		print(json.dumps(self.response, indent=2))
		sys.exit(0)
