#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib
import json

def reqapi(url, api="https://videoag.fsmpi.rwth-aachen.de/api.php/v1/"):
    request = urllib.request.urlopen(urllib.parse.urljoin(api,url))
    answer = request.read()
    jdata = json.loads(str(answer, encoding='utf-8', errors='strict'))
    response = jdata["response"]
    return response
    
def courses(id=None, api="https://videoag.fsmpi.rwth-aachen.de/api.php/v1/"):
    if id != None:
        idurl = str(id)
        key = "course"
    else:
        idurl = ""
        key = "courses"
    return reqapi("courses/"+idurl, api)[key]

def courselectures(id, api="https://videoag.fsmpi.rwth-aachen.de/api.php/v1/"):
    return reqapi("courses/"+str(id)+"/lectures/", api)["lectures"]

def lectures(id=None, api="https://videoag.fsmpi.rwth-aachen.de/api.php/v1/"):
    if id != None:
        idurl = str(id)
        key = "lecture"
    else:
        idurl = ""
        key = "lectures"
    return reqapi("lectures/"+idurl, api)[key]

def lecturecourse(id, api="https://videoag.fsmpi.rwth-aachen.de/api.php/v1/"):
    return lectures(id, api)["course_id"]