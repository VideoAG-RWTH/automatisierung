#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socketserver
import sys
import serverhandler
import comlib
import dblib

CONFIG={}

class VideoagServer(socketserver.BaseRequestHandler):
    def handle(self):
        com = comlib.recvcom(self.request)
        try:
            if not dblib.checkauth(com["token"], CONFIG):
                comlib.sendcom(self.request,{"status":"no permission"})
                return
        except KeyError as err:
            comlib.sendcom(self.request,{"status":"no key '" + format(err) + "'"})
            return
        if com["request"] == "index":
            serverhandler.indexhandle(self.request, CONFIG)
        elif com["request"] == "upload":
            serverhandler.uphandle(self.request, CONFIG)
 
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
