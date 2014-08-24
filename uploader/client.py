#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import socket
import comlib
import filelib
import sys
import hashlib


CONFIG={}


def upload(filename, event, date, host, port, token):
    fobj = open(filename, "rb")
    uuhash = filelib.uuhash(fobj)
    filesize = str(filelib.getfilesize(fobj))
    mtime = str(os.stat(filename).st_mtime)

    
    #print(jsonobj)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
    comlib.sendans(s,
        {
            "size"      :   filesize, 
            "uuhash"    :   uuhash, 
            "event"     :   event, 
            "mtime"     :   mtime, 
            "date"      :   date, 
            "request"   :   "upload", 
            "filename"  :   filename, 
            "token"     :   token
        })
    ans = comlib.recvcom(s)
    if ans["status"] != "ok":
        raise Exception
    hasher = hashlib.md5()
    read = 1
    while read > 0:
        data = fobj.read(CONFIG["chunksize"])
        read = len(data)
        hasher.update(data)
        s.sendall(data)
    fobj.close()
    md5 = hasher.hexdigest()
    comlib.sendans(s, {"status":"ok", "md5":md5})
    ans = comlib.recvcom(s)
    if ans["status"] != "ok":
        raise Exception

def readconfig(name):
    global CONFIG
    fobj = open(name, "r")
    conf = fobj.read()
    fobj.close()
    CONFIG=eval(conf)
    
if __name__ == "__main__":
    readconfig(sys.argv[1])
    upload(sys.argv[2], sys.argv[3], sys.argv[4], CONFIG["host"], CONFIG["port"], CONFIG["token"])