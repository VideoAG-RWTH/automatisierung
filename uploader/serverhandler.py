#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import comlib
import hashlib
import identify
import filelib
#import checker

def uphandle(socket, db, log, config):
    log.log(3, "starting indexhandle")
    com = comlib.recvcom(socket)
    try:
        id = com["id"]
    except KeyError as err:
            comlib.sendcom(socket,{"status":"missing key '" + format(err) + "'"})
            log.log(1, "no key '" + format(err) + "' indexhandle.recive_filearray")
            return
    
    prop = db.getfileprop(id)
    realname = config["datadir"] + "/" + filelib.getfilename(prop)
    if prop["path"] != None:
        log.log(2, "id '" + str(id) + "' already present")
        realname = prop["path"]
        if prop["md5"] != None:
            comlib.sendcom(socket,{"status":"noupload"})
            log.log(2, "no upload for id '" + str(id) + "'")
            return
    db.updatefile(id, "path", realname)
    
    log.log(2, "uploading id '" + str(id) + "' as file '" + realname + "'")
    
    size = prop["size"]
    mtime = prop["mtime"]
    
    comlib.sendcom(socket,{"status":"ok"})
    log.log(3, "receiving " + str(size) + " bytes")
    
    fobj = open(realname,"wb")
    hasher = hashlib.md5()
    #cmts = checker.MP2T()
    read = 1
    while size > 0:
        if size < config["chunksize"]:
            toread = size
        else:
            toread = config["chunksize"]
        data = socket.recv(toread)
        read = len(data)
        hasher.update(data)
        #cmts.update(data)
        fobj.write(data)
        size-=read
    fobj.close()
    os.utime(realname, times=(time.time(),float(mtime)))
    md5 = hasher.hexdigest()
    com = comlib.recvcom(socket)
    if com["md5"] != md5:
        comlib.sendcom(socket,{"status":"bad"})
        log.log(1, "md5 mismatch on file'" + realname + "', id: '" + str(id) + "'")
        raise Exception
    else:
        comlib.sendcom(socket,{"status":"ok"})
        log.log(3, "file'" + realname + "', id: '" + str(id) + "' received sucessfully")
    db.updatefile(id, "md5", md5)    
    log.log(2, "finished uphandle")

def indexhandle(socket, db, log, config):
    log.log(3, "starting indexhandle")
    com = comlib.recvcom(socket)
    try:
        filearray = com["files"]
    except KeyError as err:
        comlib.sendcom(socket,{"status":"missing key '" + format(err) + "'"})
        log.log(1, "no key '" + format(err) + "' indexhandle.recive_filearray")
        return
    
    filearray = identify.identify(filearray)
    
    for file in filearray:
        try:
            file["id"] = db.indexfile(file)
        except KeyError as err:
            comlib.sendcom(socket,{"status":"missing key '" + format(err) + "'"})
            log.log(1, "no key '" + format(err) + "' during indexhandle.indexfile")
            return
        except Exception as err:
            comlib.sendcom(socket,{"status":"error: '" + format(err) + "'"})
            log.log(1, "error '" + format(err) + "' during indexhandle.indexfile")
            return
    
    comlib.sendcom(socket, {"status": "ok", "files": filearray})
    log.log(2, "finished indexhandle")