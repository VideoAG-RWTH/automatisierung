#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
    reader = filelib.readmd5(fobj)
    read = CHUNKSIZE
    while read >= CHUNKSIZE:
        data = reader.read(CHUNKSIZE)
        read = len(data)
        s.sendall(data)
    fobj.close()
    md5 = reader.getmd5()
    #print(md5)
    comlib.sendans(s, {"status":"ok", "md5":md5})
    ans = comlib.recvcom(s)
    if ans["status"] != "ok":
        raise Exception
