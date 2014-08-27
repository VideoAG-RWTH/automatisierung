# -*- coding: utf-8 -*-
import urllib2, json, datetime

def getevents(date):
    # date: datetime object
    addr = date # conversion must appear here
    response = urllib2.urlopen(addr)
    raw = reponse.read()
    data = json.loads(raw)
    return data

def identify(filearray):
    #filearray: [{"filename": filename, "mtime": mtime, "size": size, ...}]
    for file in filearray:
        events = []
        for foundevent in [{"event":"foo", "date":"26082014"}]:
            event = {}
            event["event"] = foundevent["event"]
            event["date"] = foundevent["date"]
            events.append(event)
        file["events"] = events
    return filearray
