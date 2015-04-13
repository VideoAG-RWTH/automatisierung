#!/usr/bin/env python3

#import cgitb
import json
import sys

import conflib
import dblib
import authlib

from vidserver import *

class VideoagMetaServer(VideoagServer):
	def index(self):
		files = self.data["data"]["files"]
		self.response["data"]["fileids"] = []
		for filedata in files:
			filename = filedata["filename"]
			fileid = self.db.indexfile(filedata)
			self.response["data"]["fileids"].append({"fileid": fileid, "filename": filename})
	
	def handle(self):
		if self.data["request"] == "index":
			self.index()
		
if __name__ == "__main__":
	srv = VideoagMetaServer("server.conf", getdata())
	srv.serve()
