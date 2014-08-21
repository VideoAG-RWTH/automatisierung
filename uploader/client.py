#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import struct
import binascii
import hashlib
import base64
import socket


CHUNKSIZE = 8192


def upload(filename, event, date, host, port, token):
    fobj = open(filename, "rb")
    uuhash = UUHash(fobj)
    filesize = str(getfilesize(fobj))
    mtime = str(os.stat(filename).st_mtime)
    
    jsonobj = json.dumps({"size":filesize, "uuhash":uuhash, "event":event, "mtime":mtime, "date":date, "request":"upload", "filename": filename, "token":token})
    
    #print(jsonobj)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
    s.sendall(bytes(jsonobj, encoding='utf-8', errors='strict')+b'\n')
    ans = json.loads(str(readline(s), encoding='utf-8', errors='strict'))
    if ans["status"] != "ok":
        raise Exception
    reader = readmd5(fobj)
    read = CHUNKSIZE
    while read >= CHUNKSIZE:
        data = reader.read(CHUNKSIZE)
        read = len(data)
        s.sendall(data)
    fobj.close()
    md5 = reader.getmd5()
    #print(md5)
    ans = json.loads(str(readline(s), encoding='utf-8', errors='strict'))
    if ans["status"] != "ok":
        raise Exception
    if ans["md5"] != md5:
        jsonobj = json.dumps({"status":"bad"})
    else:
        jsonobj = json.dumps({"status":"ok"})
    s.sendall(bytes(jsonobj, encoding='utf-8', errors='strict')+b'\n')

def readline(s):
    recv = b""
    data = b""
    
    while recv != b"\n":
        data += recv
        recv = s.recv(1)
    return data

def getfilesize(fobj):
    fobj.seek(0, os.SEEK_END)
    filesize = fobj.tell()
    fobj.seek(0, os.SEEK_SET)
    return filesize

class readmd5(object):
	def __init__(self,fobj):
		self.fobj = fobj
		self.md5 = hashlib.md5()
	
	def read(self,size):
		data = self.fobj.read(size)
		self.md5.update(data)
		return data

	def getmd5(self):
		return self.md5.hexdigest()

def UUHash(fobj):
    chunksize = 307200
    
    filesize = getfilesize(fobj)
    
    fobj.seek(0)
    chunk = fobj.read(chunksize)
    md5hash = hashlib.md5(chunk).digest()
    
    smallhash = 0
    
    if filesize > chunksize:
        lastpos = fobj.tell()
        offset = 0x100000
        
        while offset + 2*chunksize < filesize:
            fobj.seek(offset)
            chunk = fobj.read(chunksize)
            
            smallhash = binascii.crc32(chunk, smallhash)
            
            lastpos = offset + chunksize
            offset <<= 1
            
        endlen = filesize - lastpos
        if endlen > chunksize:
            endlen = chunksize
            
        fobj.seek(filesize-endlen)
        chunk = fobj.read(endlen)
        smallhash = binascii.crc32(chunk, smallhash)
        
    smallhash = ((~smallhash) ^ filesize) % 2**32
        
    fobj.seek(0, os.SEEK_SET)
        
    uuhash = md5hash + struct.pack("<I", smallhash)
    return str(base64.b64encode(uuhash), encoding='utf-8', errors='strict')
