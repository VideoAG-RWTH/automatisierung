#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector
import os
import sys
import pwd
import hashlib

def adduser(user, dbconf):
    conn = mysql.connector.connect(user=dbconf["dbuser"], password=dbconf["dbpass"], host=dbconf["dbhost"], database=dbconf["db"])
    csr = conn.cursor()
    
    csr.execute("update auth set valid=0 where user=%(user)s", {"user":user})
    token = hashlib.sha512(os.urandom(8192)).hexdigest()
    csr.execute("insert into auth (user, token) values (%(user)s, %(token)s)", {"user": user, "token":token})
    conn.commit()
    
    return '"auth":{"id":"'+str(csr.lastrowid)+'", "token":"'+token+'"},'
    
def readconfig(name):
    fobj = open(name, "r")
    conf = fobj.read()
    fobj.close()
    return eval(conf)

if __name__ == "__main__":
    config = readconfig(sys.argv[1])
    if sys.argv[2] == "adduser":
        user = pwd.getpwuid(os.getuid())[0]
        print(adduser(user, config["dbconf"]))