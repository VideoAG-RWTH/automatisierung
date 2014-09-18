#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
import struct
import binascii
import base64
import os
import apilib
import datetime
import time

def getfilesize(fobj):
    fobj.seek(0, os.SEEK_END)
    filesize = fobj.tell()
    fobj.seek(0, os.SEEK_SET)
    return filesize

def parseeventdates(eventdates):
    num = 0
    events = ""
    dates = ""
    for eventdate in eventdates:
        events += eventdate["event"] + " "
        dates += eventdate["date"] + " "
        num+=1
    events = events.strip()
    dates = dates.strip()
    return {"events":events, "dates":dates, "eventcount":num}
    
def getstorename(prop):
    filename = prop["id"]
    return filename
    
def getfilenames(prop):
    events = prop["events"]
    names = []
    for e in events:
        eid = e["eventid"]
        lecture = apilib.lectures(eid)
        course = apilib.courses(lecture["course_id"])
        date = datetime.datetime.utcfromtimestamp(lecture["time"]["timestamp"])
        y = str(date.year)
        m = str(date.month)
        if len(m) < 2:
            m = "0" + m
        d = str(date.day)
        if len(d) < 2:
            d = "0" + d
        H = str(date.hour)
        if len(H) < 2:
            H = "0" + H
        M = str(date.minute)
        if len(M) < 2:
            M = "0" + M
        shortdate = y + m + d + "-" + H + M
        name = os.path.join(os.path.join(course["handle"],course["handle"] + "-" + str(shortdate)), prop["filename"])
        names.append(name)
    return names

def linkall(id, db, humandir):
    prop = db.getfileprop(id)
    paths = getfilenames(prop)
    for path in paths:
        linkpath = os.path.join(humandir, path)
        try:
            os.makedirs(os.path.dirname(linkpath))
        except FileExistsError:
            pass
        try:
            os.link(prop["path"], linkpath)
        except FileExistsError:
            pass
        os.utime(linkpath, times=(time.time(),float(prop["mtime"])))
        db.indexpath(prop["id"], linkpath)

def uuhash(fobj):
    chunksize = 307200
    
    filesize = getfilesize(fobj)
    
    fobj.seek(0)
    chunk = fobj.read(chunksize)
    md5hash = hashlib.md5(chunk).digest()
    
    smallhash = 0
    
    if filesize > chunksize:
        lastpos = fobj.tell()
        offset = 0x100000
        
        while offset + 2*chunksize < filesize:
            fobj.seek(offset)
            chunk = fobj.read(chunksize)
            
            smallhash = binascii.crc32(chunk, smallhash)
            
            lastpos = offset + chunksize
            offset <<= 1
            
        endlen = filesize - lastpos
        if endlen > chunksize:
            endlen = chunksize
            
        fobj.seek(filesize-endlen)
        chunk = fobj.read(endlen)
        smallhash = binascii.crc32(chunk, smallhash)
        
    smallhash = ((~smallhash) ^ filesize) % 2**32
        
    fobj.seek(0, os.SEEK_SET)
        
    uuhash = md5hash + struct.pack("<I", smallhash)
    return str(base64.b64encode(uuhash), encoding='utf-8', errors='strict')