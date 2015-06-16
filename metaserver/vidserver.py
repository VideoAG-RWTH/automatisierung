#!/usr/bin/env python3

import json
import sys
import os

import conflib
import dblib
import authlib

def getdata(environ):
	try:
		length = int(environ.get('CONTENT_LENGTH', '0'))
	except ValueError:
		length = 0

	return json.loads(environ['wsgi.input'].read(length))

class VideoagServer(object):
	def __init__(self, conffile, data):
		self.response = {"result":"", "data":{}}
		self.responseheaders = []
		
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
			self.end("ok", "200 OK")
#		except KeyError as err:
#			self.error("KeyError", "KeyError: {0}".format(err), "400 Bad Request")
#		except Exception as err:
#			self.error("Exception", "Generell Exception: {0}".format(err), "500 Internal Server Error")
		
	def error(self, desc, moredesc=None, rescode="500 Internal Server Error"):
		self.response["data"]["errordesc"] = desc
		self.response["data"]["moredesc"] = moredesc
		self.end("error", rescode)
	
	def end(self, result, rescode):
		self.response["result"] = result
		resdata = json.dumps(self.response, indent=2)
		
		self.responseheaders.append("Content-Type: text/json")
		self.responseheaders.append("Content-Length: " + str(len(resdata)))
		
		start_response(rescode, self.responseheaders)
		
		return [resdata]

def application_template(environ, start_response, ServerClass, conf):
	srv = ServerClass(conf, getdata(environ))
	srv.serve()

