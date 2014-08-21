#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import socket
import comlib
import filelib


CHUNKSIZE = 8192


def upload(filename, event, date, host, port, token):
    fobj = open(filename, "rb")
    uuhash = filelib.uuhash(fobj)
    filesize = str(filelib.getfilesize(fobj))
    mtime = str(os.stat(filename).st_mtime)
    
    jsonobj = json.dumps({"size":filesize, "uuhash":uuhash, "event":event, "mtime":mtime, "date":date, "request":"upload", "filename": filename, "token":token})
    
    #print(jsonobj)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
    s.sendall(bytes(jsonobj, encoding='utf-8', errors='strict')+b'\n')
    ans = json.loads(str(comlib.readline(s), encoding='utf-8', errors='strict'))
    if ans["status"] != "ok":
        raise Exception
    reader = filelib.readmd5(fobj)
    read = CHUNKSIZE
    while read >= CHUNKSIZE:
        data = reader.read(CHUNKSIZE)
        read = len(data)
        s.sendall(data)
    fobj.close()
    md5 = reader.getmd5()
    #print(md5)
    ans = json.loads(str(comlib.readline(s), encoding='utf-8', errors='strict'))
    if ans["status"] != "ok":
        raise Exception
    if ans["md5"] != md5:
        jsonobj = json.dumps({"status":"bad"})
    else:
        jsonobj = json.dumps({"status":"ok"})
    s.sendall(bytes(jsonobj, encoding='utf-8', errors='strict')+b'\n')
