#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socketserver
import sys
import serverhandler
import comlib

CONFIG={}

class VideoagServer(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            com = comlib.recvcom(self.request)
        except ValueError:
            comlib.sendans(self.request,{"status":"no json"})
            return
        try:
            if com["token"] not in ["moritz", "videoag"]:
                comlib.sendans(self.request,{"status":"no permission"})
                return
        except KeyError:
            comlib.sendans(self.request,{"status":"no token"})
            return
        if com["request"] == "upload":
            serverhandler.uphandle(self.request, com, CONFIG)
 
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
