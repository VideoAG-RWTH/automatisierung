#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import hashlib
import base64

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

def auth(s, auth):
    sendcom(s, {"authid":auth["id"]})
    ans = recvcom(s)
    if ans["status"] != "ok":
        raise Exception
        
    salt = base64.b64decode(ans["salt"])
    rounds = ans["rounds"]
    
    authtoken = hashlib.pbkdf2_hmac('sha512', auth["token"].encode('utf-8'), salt, rounds)
    
    sendcom(s, {"authtoken":base64.b64encode(authtoken).decode('utf-8')})
    
    ans = recvcom(s)
    if ans["status"] != "ok":
        raise Exception
        
def checkauth(s, db, saltsize, rounds):
    ans = recvcom(s)
    id = ans["authid"]
    
    token = db.checkauth(id)
    
    if token == None:
        return False
    
    salt = os.urandom(saltsize)
    
    sendcom(s, {"status":"ok", "salt":base64.b64encode(salt).decode('utf-8'), "rounds":rounds})
    
    authtoken = hashlib.pbkdf2_hmac('sha512', token.encode('utf-8'), salt, rounds)
    
    ans = recvcom(s)
    c_authtoken = base64.b64decode(ans["authtoken"])
    
    return authtoken == c_authtoken
    
    