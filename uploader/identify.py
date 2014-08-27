# -*- coding: utf-8 -*-
import urllib2, json, time

def getevents(timestamp):
    addr = "https://videoag.fsmpi.rwth-aachen.de/site/heute.php?start=" + str(timestamp) # maybe make this configurable
    response = urllib2.urlopen(addr)
    raw = response.read()
    data = json.loads(raw)
    return data

def today():
    now = time.time()
    now = int(now - now % 86400)
    return now

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
            cluster.append({"files": [f], "events": []) # new cluster
        else:
            cluster[-1]["files"].append(f) # append to cluster
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

# returns list of clusters: [{"files": [,,,], "events": [,,]},...]
def identify(files):
    #files: [{"filename": filename, "mtime": mtime, "size": size, ...}]
    events = getevents(today())
    clusters = findclusters(files)
    for c in clusters:
        c["events"] = clusterevents(events, c)
    return clusters
