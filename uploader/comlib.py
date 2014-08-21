#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

def sendans(fobj, nojson):
    fobj.write(bytes(json.dumps(nojson), encoding='utf-8', errors='strict')+b'\n')
    
def recvcom(fobj):
    return json.loads(str(fobj.readline().strip(), encoding='utf-8', errors='strict'))
    
def readline(s):
    recv = b""
    data = b""
    
    while recv != b"\n":
        data += recv
        recv = s.recv(1)
    return data