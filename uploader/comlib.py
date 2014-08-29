#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

def sendcom(socket, nojson):
    socket.sendall(bytes(json.dumps(nojson), encoding='utf-8', errors='strict')+b'\n')
    
def recvcom(socket):
    try:
        return json.loads(str(readline(socket).strip(), encoding='utf-8', errors='strict'))
    except ValueError:
        sendcom(socket, {"status":"no json"})
        raise ValueError

def readline(s):
    recv = b""
    data = b""
    
    while recv != b"\n":
        data += recv
        recv = s.recv(1)
        if recv == b"":
            raise Exception("Connection closed")
    return data
