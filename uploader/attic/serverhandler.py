#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import comlib
import hashlib
import identify
import filelib
import tests

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
    realname = config["dirconf"]["data"] + "/" + filelib.getstorename(prop)
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
    
    comlib.sendcom(socket,{"status":"ok"})
    log.log(3, "receiving " + str(size) + " bytes")
    
    fobj = open(realname,"wb")
    hasher = hashlib.md5()
    
    ending = prop["filename"].split(".")[-1].lower()
    availtest = db.posstest(ending)
    testobjs = []
    for test in tests.alltests:
        if test.NAME in availtest:
            testobjs.append(test())
    
    read = 1
    while size > 0:
        if size < config["chunksize"]:
            toread = size
        else:
            toread = config["chunksize"]
        data = socket.recv(toread)
        read = len(data)
        hasher.update(data)
        for obj in testobjs:
            obj.update(data)
        fobj.write(data)
        size-=read
    fobj.close()
    md5 = hasher.hexdigest()
    for obj in testobjs:
        res = obj.final()
        db.indextest(id, obj.NAME, res)
    com = comlib.recvcom(socket)
    if com["md5"] != md5:
        comlib.sendcom(socket,{"status":"bad"})
        log.log(1, "md5 mismatch on file'" + realname + "', id: '" + str(id) + "'")
        raise Exception
    else:
        comlib.sendcom(socket,{"status":"ok"})
        log.log(2, "file'" + realname + "', id: '" + str(id) + "' received sucessfully")
    db.updatefile(id, "md5", md5)    
    log.log(3, "finished uphandle")

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
    log.log(3, "finished indexhandle")

def correcthandle(socket, db, log, config):
    log.log(3, "starting correcthandle")
    com = comlib.recvcom(socket)
    try:
        fileid = com["id"]
        eventids = com["eventids"]
    except KeyError as err:
            comlib.sendcom(socket,{"status":"missing key '" + format(err) + "'"})
            log.log(1, "no key '" + format(err) + "' indexhandle.recive_filearray")
            return
    
    db.setevents(fileid, eventids)
    log.log(3, "finished correcthandle")