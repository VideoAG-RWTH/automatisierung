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
        dbconf = CONFIG["dbconf"]
        self.db = dblib.DBmysql(dbconf["dbuser"], dbconf["dbpass"], dbconf["dbhost"], dbconf["db"])
        
    def handle(self):
        #Authenticate User
        try:
            if not comlib.checkauth(s=self.request, db=self.db, saltsize=128, rounds=100000):
                comlib.sendcom(self.request,{"status":"no permission"})
                return
        except KeyError as err:
            comlib.sendcom(self.request,{"status":"no key '" + format(err) + "'"})
            return
        comlib.sendcom(self.request,{"status":"ok"})
        
        while True:
            com = comlib.recvcom(self.request)
            try:
                req = com["request"]
            except KeyError as err:
                comlib.sendcom(self.request,{"status":"no key '" + format(err) + "'"})
                return
            comlib.sendcom(self.request,{"status":"ok"})
            
            if req == "index":
                serverhandler.indexhandle(self.request, self.db, CONFIG)
            elif req == "upload":
                serverhandler.uphandle(self.request, self.db, CONFIG)
            elif req == "end":
                break
            else:
                comlib.sendcom(self.request,{"status":"do not understand request '"+req+"'"})
    
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
    serverconf = CONFIG["serverconf"]
    server = socketserver.TCPServer((serverconf["host"], serverconf["port"]), VideoagServer)
    server.serve_forever()
#    server.handle_request()
