#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socketserver
import sys
import serverhandler
import comlib
import dblib
import logger

CONFIG={}

class VideoagServer(socketserver.BaseRequestHandler):
    def setup(self):
        dbconf = CONFIG["dbconf"]
        self.db = dblib.DBmysql(dbconf["dbuser"], dbconf["dbpass"], dbconf["dbhost"], dbconf["db"])
        self.log = logger.logger(CONFIG["logconf"], self.db)
        
    def handle(self):
        #Authenticate User
        self.log.log(3, "Authentication User")
        try:
            if not comlib.checkauth(s=self.request, db=self.db, log=self.log, saltsize=128, rounds=100000):
                comlib.sendcom(self.request,{"status":"no permission"})
                self.log.log(1, "authentication failed")
                return
        except KeyError as err:
            comlib.sendcom(self.request,{"status":"no key '" + format(err) + "'"})
            self.log.log(1, "no key '" + format(err) + "' during authentication")
            return
        comlib.sendcom(self.request,{"status":"ok"})
        
        while True:
            com = comlib.recvcom(self.request)
            try:
                req = com["request"]
            except KeyError as err:
                comlib.sendcom(self.request,{"status":"no key '" + format(err) + "'"})
                self.log.log(1, "no key '" + format(err) + "' during main loop")
                return
            comlib.sendcom(self.request,{"status":"ok"})
            
            if req == "index":
                self.log.log(2, "doing index")
                serverhandler.indexhandle(self.request, self.db, self.log, CONFIG)
            elif req == "upload":
                self.log.log(2, "doing upload")
                serverhandler.uphandle(self.request, self.db, self.log, CONFIG)
            elif req == "end":
                self.log.log(2, "terminating connection")
                return
            else:
                comlib.sendcom(self.request,{"status":"do not understand request '"+req+"'"})
                self.log.log(1, "do not understand request '"+req+"'")
    
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
