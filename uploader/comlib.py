#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

def sendans(socket, nojson):
    socket.sendall(bytes(json.dumps(nojson), encoding='utf-8', errors='strict')+b'\n')
    
def recvcom(socket):
    return json.loads(str(readline(socket).strip(), encoding='utf-8', errors='strict'))
    
def readline(s):
    recv = b""
    data = b""
    
    while recv != b"\n":
        data += recv
        recv = s.recv(1)
    return data

class readsock(object):
    def __init__(self, s):
        self.s = s
    def read(self, size):
        return self.s.recv(size)