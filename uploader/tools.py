#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import pwd
import hashlib
import dblib
import apilib

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
    
    return lectures
    

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