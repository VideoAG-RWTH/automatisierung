#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socketserver
import sys
import serverhandler
import comlib
import dblib

CONFIG={}

class VideoagServer(socketserver.BaseRequestHandler):
    def setup(self):
        self.db = dblib.DBmysql(CONFIG["dbuser"], CONFIG["dbpass"], CONFIG["dbhost"], CONFIG["db"])
        
    def handle(self):
        com = comlib.recvcom(self.request)
        try:
            req = com["request"]
        except KeyError as err:
            comlib.sendcom(self.request,{"status":"no key '" + format(err) + "'"})
            return
        comlib.sendcom(self.request,{"status":"ok"})
        
        try:
            if not comlib.checkauth(s=self.request, db=self.db, saltsize=8192, rounds=100000):
                comlib.sendcom(self.request,{"status":"no permission"})
                return
        except KeyError as err:
            comlib.sendcom(self.request,{"status":"no key '" + format(err) + "'"})
            return
        
        comlib.sendcom(self.request,{"status":"ok"})
        
        if req == "index":
            serverhandler.indexhandle(self.request, self.db, CONFIG)
        elif req == "upload":
            serverhandler.uphandle(self.request, self.db, CONFIG)
    
    def finish(self):
        self.db.close()
 
def readconfig(name):
    global CONFIG
    fobj = open(name, "r")
    conf = fobj.read()
    fobj.close()
    CONFIG=eval(conf)
 
if __name__ == "__main__":
    readconfig(sys.argv[1])
    server = socketserver.TCPServer((CONFIG["host"], CONFIG["port"]), VideoagServer)
    server.serve_forever()
#    server.handle_request()
