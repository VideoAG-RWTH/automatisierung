#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
import struct
import binascii
import base64
import os

def getfilesize(fobj):
    fobj.seek(0, os.SEEK_END)
    filesize = fobj.tell()
    fobj.seek(0, os.SEEK_SET)
    return filesize

def uuhash(fobj):
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