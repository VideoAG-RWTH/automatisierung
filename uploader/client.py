#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import socket
import comlib
import filelib
import sys
import hashlib

def index(filenames, config):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((config["host"],config["port"]))
        
    comlib.auth(s, config["auth"])
    
    comlib.sendcom(s,{"request":"index"})
    ans = comlib.recvcom(s)
    if ans["status"] != "ok":
        raise Exception
    
    filearray = []
    for filename in filenames:
        fobj = open(filename, "rb")
        uuhash = filelib.uuhash(fobj)
        filesize = str(filelib.getfilesize(fobj))
        mtime = os.stat(filename).st_mtime
        filedict = \
            {
                "size"      :   filesize,
                "uuhash"    :   uuhash,
                "mtime"     :   mtime,
                "filename"  :   filename,
            }
        filearray.append(filedict)
    
    comlib.sendcom(s, {"files":filearray})
        
    ans = comlib.recvcom(s) #filearray
    if ans["status"] != "ok":
        raise Exception(ans["status"])
    
    comlib.sendcom(s,{"request":"end"})
    
    return ans["files"]

def upload(filearray, config):
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((config["host"],config["port"]))
        
    comlib.auth(s, config["auth"])
    
    for file in filearray:
        filename = file["filename"]
        id = file["id"]
    
        comlib.sendcom(s,{"request":"upload"})
        ans = comlib.recvcom(s)
        if ans["status"] != "ok":
            raise Exception
        
        comlib.sendcom(s, {"id": id})
        ans = comlib.recvcom(s)
        if ans["status"] == "noupload":
            continue
        elif ans["status"] != "ok":
            raise Exception
                
        fobj = open(filename, "rb")
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
            raise Exception(ans["status"])
    
    comlib.sendcom(s,{"request":"end"})

def readconfig(name):
    fobj = open(name, "r")
    conf = fobj.read()
    fobj.close()
    return eval(conf)
    
if __name__ == "__main__":
    config = readconfig(sys.argv[1])
    files = []
    for i in range(2, len(sys.argv)):
        files.append(sys.argv[i])
    filearray = index(files, config)
    upload(filearray, config)