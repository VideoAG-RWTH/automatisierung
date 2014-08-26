#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import comlib
import hashlib
import dblib

def uphandle(socket, config):
    com = comlib.recvcom(socket)
    try:
        id = com["id"]
    except KeyError as err:
            comlib.sendcom(socket,{"status":"missing key '" + format(err) + "'"})
            return
    
    comlib.sendcom(socket,{"status":"ok"})
    
    realname = dblib.getfilename(id, config)
    prop = dblib.getfileprop(id, config)
    size = prop["size"]
    mtime = prop["mtime"]
    
    fobj = open(realname,"wb")
    hasher = hashlib.md5()
    read = 1
    while size > 0:
        if size < config["chunksize"]:
            toread = size
        else:
            toread = config["chunksize"]
        data = socket.recv(toread)
        read = len(data)
        hasher.update(data)
        fobj.write(data)
        size-=read
    fobj.close()
    os.utime(realname, times=(time.time(),float(mtime)))
    md5 = hasher.hexdigest()
    com = comlib.recvcom(socket)
    if com["md5"] != md5:
        comlib.sendcom(socket,{"status":"bad"})
        raise Exception
    else:
        comlib.sendcom(socket,{"status":"ok"})
    dblib.updatefile(id, "md5", md5)

def indexhandle(socket, config):
    com = comlib.recvcom(socket)
    try:
        filename = com["filename"]
        date = com["date"]
        mtime = com["mtime"]
        event = com["event"]
        uuhash = com["uuhash"]
        size = int(com["size"])
    except KeyError as err:
        comlib.sendcom(socket,{"status":"missing key '" + format(err) + "'"})
        return
    
    status = "ok"
    try:
        dblib.indexfile(filename, uuhash, size, mtime, event, date)
    except Exception:
        status = "bad"
    comlib.sendcom(socket, {"status": status})