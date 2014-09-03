#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import pwd
import hashlib
import dblib
import apilib
import identify

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