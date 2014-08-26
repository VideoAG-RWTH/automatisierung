#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def checkauth(token, config):
    if token in ["moritz", "videoag"]:
        return True
    else:
        return False
        
def indexfile(filename, uuhash, size, mtime, event, date, md5=None):
    pass

def updatefile(id, key, value):
    pass

def getfileprop(id, config):
    pass

def getfilename(id, config):
    prop = getfileprop(id, config)
    prop["event"]+"-"+prop["date"]+"-"+prop["filename"]