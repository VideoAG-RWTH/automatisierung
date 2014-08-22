#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import filelib
import comlib

def uphandle(rfile, wfile, com, chunksize):
    filename = com["filename"]
    date = com["date"]
    mtime = com["mtime"]
    event = com["event"]
    uuhash = com["uuhash"]
    size = int(com["size"])
    
    comlib.sendans(wfile,{"status":"ok"})
    
    r = filelib.readmd5(rfile)
    print(uuhash)
    realname = event+"-"+date+"-"+filename
    fobj = open(realname,"wb")
    
    while size > chunksize:
        fobj.write(r.read(chunksize))
        size-=chunksize
    fobj.write(r.read(size))
    fobj.close()
    os.utime(realname, times=(time.time(),float(mtime)))
    md5 = r.getmd5()
    #print(md5)
    com = comlib.recvcom(rfile)
    if com["md5"] != md5:
        comlib.sendans(wfile,{"status":"bad"})
        raise Exception
    else:
        comlib.sendans(wfile,{"status":"ok"})
