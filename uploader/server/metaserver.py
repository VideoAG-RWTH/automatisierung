#!/usr/bin/env python3

#import cgitb
import time
import datetime

from vidserver import *
from models import AlreadyExists

class VideoagMetaServer(VideoagServer):
	def index(self):
		files = self.data["data"]["files"]
		upload = self.db.indexupload()
		fileobjs = []
		for filedata in files:
			name = filedata["name"]
			try:
				fileobj = self.db.indexfile(filedata, upload)
			except AlreadyExists:
				continue
			fileobjs.append({"name": name, "fileobj": fileobj})
		#self.db.commit()
		
		self.db.identify(upload)
		self.db.commit()
		
		self.response["data"]["fileids"] = []
		for f in fileobjs:
			fileid = f["fileobj"].id
			self.response["data"]["fileids"].append({"fileid": fileid, "name": f["name"]})
	
	def getunindexed(self):
		try:
			starttime = datetime.datetime.fromtimestamp(self.data["data"]["starttime"])
		except KeyError:
			starttime = None
		try:
			endtime = datetime.datetime.fromtimestamp(self.data["data"]["endtime"])
		except KeyError:
			endtime = None
		
		clusters = self.db.getunindexed(starttime, endtime)
		
		self.response["data"]["clusters"] = []
		
		for cobj in clusters:
			c = {}
			files = []
			for fobj in cobj.files:
				files.append({
						"id": fobj.id,
						"mtime": fobj.mtime.timestamp(),
						"size": fobj.size,
						"name": fobj.name,
						"uploadid": fobj.upload.id,
						"uploadtime": fobj.upload.time.timestamp(),
						"uploaduser": fobj.upload.user.name
					})
			c['files'] = files
			events = []
			for eobj in cobj.events:
				events.append(eobj.event)
			c['events'] = events
			
			self.response["data"]["clusters"].append(c)
		
	def handle(self):
		if self.data["request"] == "index":
			self.index()
		elif self.data["request"] == "getunindexed":
			self.getunindexed()
		else:
			self.error("Unkown Request", "Unknown request " + self.data["request"], "400 Bad Request")
		
if __name__ == "__main__":
	srv = VideoagMetaServer("server.conf", getdata())
	srv.serve()
