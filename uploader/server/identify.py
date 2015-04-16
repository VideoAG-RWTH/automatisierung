# -*- coding: utf-8 -*-

import urllib.request, urllib.parse, urllib.error
import json
import time

"""
def identify(filearray):
    #filearray: [{"filename": filename, "mtime": mtime, "size": size, ...}]
    for file in filearray:
        events = []
        for foundevent in [{"event":"foo", "date":"26082014", "id":1337},{"event":"bar", "date":"29082014", "id":4711}]:
            events.append(foundevent)
        file["events"] = events
    return filearray
"""

def getevents(timestamp, duration=86400):
    addr = "https://videoag.fsmpi.rwth-aachen.de/site/heute.php?start=" + str(timestamp) + "&timespan=" + str(duration) # maybe make this configurable
    response = urllib.request.urlopen(addr)
    raw = response.read()
    data = json.loads(str(raw, encoding='utf-8', errors='strict'))
    return data

def today():
    return dayify(time.time())

def dayify(timestamp):
    return int(timestamp - timestamp % 86400)

def confidence(): # maybe make this configurable
    return 15 * 60 # 15 minutes

def during(event, timestamp):
    return timestamp >= event["starting"] - confidence() and timestamp <= event["ending"] + confidence()

def findclusters(files):
    sort = sorted(files, key=lambda f: f["mtime"])
    cluster = []
    lasttime = 0
    for f in sort:
        if abs(f["mtime"] - lasttime) > confidence(): # maybe don't use confidence() here # and/or add or lasttime == 0
            cluster.append({"files": [f], "events": []}) # new cluster
        else:
            cluster[-1]["files"].append(f) # append to cluster
        lasttime = f["mtime"]
    return cluster

def possibleevents(events, timestamp):
    ret = []
    for e in events:
        if during(e, timestamp):
            ret.append(e)
    return ret

def clusterevents(events, cluster):
    ret = []
    for f in cluster["files"]:
        possible = possibleevents(events, f["mtime"])
        for p in possible:
            if not p in ret:
                ret.append(p)
    return ret

def filedates(files):
    start = today()
    end = today() + 86400
    for f in files:
        if f["mtime"] < start:
            start = f["mtime"]
        if f["mtime"] > end:
            end = f["mtime"]
    start = dayify(start)
    end = dayify(end) + 86400
    duration = end - start
    return start, duration

# returns list of clusters: [{"files": [,,,], "events": [,,]},...]
def identify(files):
    #files: [{"filename": filename, "mtime": mtime, "size": size, ...}]
    start, duration = filedates(files)
    events = getevents(start, duration)["response"]["lectures"]
    clusters = findclusters(files)
    for c in clusters:
        c["events"] = clusterevents(events, c)
    return clusters
    
#    #Covert to another format ;)
#    filearray = []
#    i=0
#    for c in clusters:
#        for f in c["files"]:
#            fevents = []
#            for e in c["events"]:
#                e["id"] = i
#                fevents.append(e)
#            f["events"] = fevents
#            filearray.append(f)
#        i+=1
#    
#    return filearray
