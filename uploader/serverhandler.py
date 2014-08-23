#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import filelib
import comlib

def uphandle(socket, com, config):
    filename = com["filename"]
    date = com["date"]
    mtime = com["mtime"]
    event = com["event"]
    uuhash = com["uuhash"]
    size = int(com["size"])
    
    comlib.sendans(socket,{"status":"ok"})
    
    fs = comlib.readsock(socket)
    r = filelib.readmd5(fs)
    print(uuhash)
    realname = event+"-"+date+"-"+filename
    fobj = open(realname,"wb")
    
    while size > config["chunksize"]:
        fobj.write(r.read(config["chunksize"]))
        size-=config["chunksize"]
    fobj.write(r.read(size))
    fobj.close()
    os.utime(realname, times=(time.time(),float(mtime)))
    md5 = r.getmd5()
    #print(md5)
    com = comlib.recvcom(socket)
    if com["md5"] != md5:
        comlib.sendans(socket,{"status":"bad"})
        raise Exception
    else:
        comlib.sendans(socket,{"status":"ok"})
