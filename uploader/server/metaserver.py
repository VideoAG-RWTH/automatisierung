#!/usr/bin/env python3

#import cgitb
import time

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
			fileid = fobj.id
			self.response["data"]["fileids"].append({"fileid": fileid, "name": f["name"]})
	
	def getunindexed(self):
		try:
			starttime = self.data["data"]["starttime"]
		except KeyError:
			starttime = time.time()-14400
		try:
			endtime = self.data["data"]["endtime"]
		except KeyError:
			endtime = time.time()
		
		self.response["data"]["clusters"] = []
		clusters = db.unindexed(starttime, endtime)
		for cobj in clusters:
			c = []
			for fobj in db.getfilestocluster(cobj):
				c.append({
					"id:" fobj.id,
					"mtime": fobj.mtime.timestamp(),
					"size": fobj.size
					"uploadid": fobj.upload.id
					"uploadtime": fobj.upload.time.timestamp()
					"uploaduser": fobj.upload.user.name
					})
			
				
			
	
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
