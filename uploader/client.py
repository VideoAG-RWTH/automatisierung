#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import socket
import comlib
import filelib
import sys
import hashlib

def index(filename, config):
    fobj = open(filename, "rb")
    uuhash = filelib.uuhash(fobj)
    filesize = str(filelib.getfilesize(fobj))
    mtime = str(os.stat(filename).st_mtime)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((config["host"],config["port"]))
    comlib.sendcom(s,
        {
            "request"   :   "index", 
            "token"     :   config["token"]
        })
    ans = comlib.recvcom(s)
    if ans["status"] != "ok":
        raise Exception
    filearray = \
        [
            {
                "size"      :   filesize,
                "uuhash"    :   uuhash,
                "mtime"     :   mtime,
                "filename"  :   filename,
            }
        ]
    comlib.sendcom(s, {"files":filearray})
        
    ans = comlib.recvcom(s) #filearray
    if ans["status"] != "ok":
        raise Exception(ans["status"])
    return ans["files"]

def upload(filename, id, config):
    fobj = open(filename, "rb")
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((config["host"],config["port"]))
    comlib.sendcom(s,
        {
            "request"   :   "upload", 
            "token"     :   config["token"]
        })
    ans = comlib.recvcom(s)
    if ans["status"] != "ok":
        raise Exception
    
    comlib.sendcom(s, {"id": id})
    ans = comlib.recvcom(s)
    if ans["status"] != "ok":
        raise Exception    
    
    hasher = hashlib.md5()
    read = 1
    while read > 0:
        data = fobj.read(config["chunksize"])
        read = len(data)
        hasher.update(data)
        s.sendall(data)
    fobj.close()
    md5 = hasher.hexdigest()
    comlib.sendcom(s, {"status":"ok", "md5":md5})
    ans = comlib.recvcom(s)
    if ans["status"] != "ok":
        raise Exception

def readconfig(name):
    fobj = open(name, "r")
    conf = fobj.read()
    fobj.close()
    return eval(conf)
    
if __name__ == "__main__":
    config = readconfig(sys.argv[1])
    id = index(sys.argv[3], config)[0]["id"]
    upload(sys.argv[2], id, config)