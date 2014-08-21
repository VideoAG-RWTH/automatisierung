#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import socketserver
import hashlib
import os
import time
import sys

CHUNKSIZE = 8192
DB = ""
HOST = "localhost"
PORT = 9999

class VideoagServer(socketserver.StreamRequestHandler):
    def handle(self):
        try:
            com = recvcom(self.rfile)
        except ValueError:
            sendans(self.wfile,{"status":"no json"})
            return
        try:
            if com["token"] not in ["moritz", "videoag"]:
                sendans(self.wfile,{"status":"no permission"})
                return
        except KeyError:
            sendans(self.wfile,{"status":"no token"})
            return
        if com["request"] == "upload":
            filename = com["filename"]
            date = com["date"]
            mtime = com["mtime"]
            event = com["event"]
            uuhash = com["uuhash"]
            size = int(com["size"])
            
            sendans(self.wfile,{"status":"ok"})
            
            r = readmd5(self.rfile)            
            print(uuhash)
            realname = event+"-"+date+"-"+filename
            fobj = open(realname,"wb")
            
            while size > CHUNKSIZE:
                fobj.write(r.read(CHUNKSIZE))
                size-=CHUNKSIZE
            fobj.write(r.read(size))
            fobj.close()
            os.utime(realname, times=(time.time(),float(mtime)))
            md5 = r.getmd5()
            sendans(self.wfile,{"status":"ok", "md5":md5})
            com = recvcom(self.rfile)
            if com["status"] != "ok":
                raise Exception

def sendans(fobj, nojson):
    fobj.write(bytes(json.dumps(nojson), encoding='utf-8', errors='strict')+b'\n')
    
def recvcom(fobj):
    return json.loads(str(fobj.readline().strip(), encoding='utf-8', errors='strict'))

class readmd5(object):
	def __init__(self,fobj):
		self.fobj = fobj
		self.md5 = hashlib.md5()
	
	def read(self,size):
		data = self.fobj.read(size)
		self.md5.update(data)
		return data

	def getmd5(self):
		return self.md5.hexdigest()
 
def readconfig(name):
    global CHUNKSIZE, DB, HOST, PORT
    fobj = open(name, "r")
    conf = fobj.readall()
    fobj.close()
    exec(conf)
 
if __name__ == "__main__":
    readconfig(sys.argv[1])
    server = socketserver.TCPServer((HOST, PORT), VideoagServer)
    server.serve_forever()
#    server.handle_request()
