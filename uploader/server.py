#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socketserver
import sys
import serverhandler
import comlib

CHUNKSIZE = 8192
DB = ""
HOST = "localhost"
PORT = 9999

class VideoagServer(socketserver.StreamRequestHandler):
    def handle(self):
        try:
            com = comlib.recvcom(self.rfile)
        except ValueError:
            comlib.sendans(self.wfile,{"status":"no json"})
            return
        try:
            if com["token"] not in ["moritz", "videoag"]:
                comlib.sendans(self.wfile,{"status":"no permission"})
                return
        except KeyError:
            comlib.sendans(self.wfile,{"status":"no token"})
            return
        if com["request"] == "upload":
            serverhandler.uphandle(self.rfile, self.wfile, com, CHUNKSIZE)
 
def readconfig(name):
    global CHUNKSIZE, DB, HOST, PORT
    fobj = open(name, "r")
    conf = fobj.read()
    fobj.close()
    exec(conf)
 
if __name__ == "__main__":
    readconfig(sys.argv[1])
    server = socketserver.TCPServer((HOST, PORT), VideoagServer)
    server.serve_forever()
#    server.handle_request()
