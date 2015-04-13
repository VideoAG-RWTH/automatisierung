#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import pwd
import hashlib
import dblib
import apilib
import identify
import random
import time
import filelib

def adduser(user, dbconf):
    db = dblib.DBmysql(dbconf["dbuser"], dbconf["dbpass"], dbconf["dbhost"], dbconf["db"])
    
    token = hashlib.sha512(os.urandom(8192)).hexdigest()
    rowid = db.adduser(user, token)
    
    db.close()
    
    return '"auth":{"id":"'+str(rowid)+'", "token":"'+token+'"},'
    
def listevents(fileid, config):
    dbconf = config["dbconf"]
    db = dblib.DBmysql(dbconf["dbuser"], dbconf["dbpass"], dbconf["dbhost"], dbconf["db"])
    
    prop = db.getfileprop(fileid)
    events = prop["events"]
    lectures = []
    for event in events:
        id = event["eventid"]
        lecture = apilib.lectures(id, config["apiurl"])
        lecture["course"] = apilib.courses(lecture["course_id"], config["apiurl"])
        
        lectures.append(lecture)
    
    db.close()
    
    return lectures
    
def reidentify(fileids, config):
    dbconf = config["dbconf"]
    db = dblib.DBmysql(dbconf["dbuser"], dbconf["dbpass"], dbconf["dbhost"], dbconf["db"])
    
    files = []
    for fileid in fileids:
        files.append(db.getfileprop(fileid))
    
    files = identify.identify(files)
    for file in files:
        db.indexfile(file)
    
    db.close()
    
def link(fileids, config):
    dbconf = config["dbconf"]
    db = dblib.DBmysql(dbconf["dbuser"], dbconf["dbpass"], dbconf["dbhost"], dbconf["db"])
    
    for id in fileids:
        filelib.linkall(id, db, config["dirconf"]["human"])
    
    db.close()

def maketestdata(dir, courseid, api="https://videoag.fsmpi.rwth-aachen.de/api.php/v1/"):
#    if (fileid==None) == (eventid==None):
#        raise Exception("Excectly one of fileid and eventid must be not None")
    lids = apilib.courselectures(courseid)
    for l in lids:
        lprops = apilib.lectures(l)
        start = lprops["time"]["timestamp"]
        stop = start + lprops["duration"]*60
        gap = random.randint(10*60, 15*60)
        for i in range(start-random.randint(0, 15*60), stop+random.randint(0, 15*60)):
            if gap == 0:
                gap = random.randint(10*60, 15*60)
                fname = os.path.join(dir, str(i)+".MTS")
                f = open(fname, "wb")
                f.write(os.urandom(1024*1024))
                f.close()
                os.utime(fname, times=(time.time(),float(i)))
            gap-=1

def readconfig(name):
    fobj = open(name, "r")
    conf = fobj.read()
    fobj.close()
    return eval(conf)

if __name__ == "__main__":
    config = readconfig(sys.argv[1])
    if sys.argv[2] == "adduser":
        user = pwd.getpwuid(os.getuid())[0]
        print(adduser(user, config["dbconf"]))
        
    elif sys.argv[2] == "listevents":
        print(listevents(sys.argv[3], config))
    
    elif sys.argv[2] == "reidentify":
        fileids = []
        for i in range(3, len(sys.argv)):
            fileids.append(sys.argv[i])
        reidentify(fileids, config)
    
    elif sys.argv[2] == "link":
        fileids = []
        for i in range(3, len(sys.argv)):
            fileids.append(sys.argv[i])
        link(fileids, config)
    
    elif sys.argv[2] == "maketestdata":
        maketestdata(sys.argv[3], sys.argv[4])