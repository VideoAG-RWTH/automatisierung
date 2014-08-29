#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import mysql.connector

#A clean class hierarchy

class DBconn(object):
    """
    The base Class. This should apply to all DB-Types.
    Some base functions and getfilename are defiend here.
    You should not create objects of this Class!
    """
    
    def __init__(self):
        super().__init__()
    
    def __enter__(self):
        return self
        
    def close(self):
        pass
    
    def __exit__(self):
        self.close()
    
    def checkauth(token):
        pass
    
    def indexfile(self, filedict):
        pass
    
    def updatefile(self, id, key, value):
        pass
    
    def getfileprop(self, id):
        pass

class DBconnsql(DBconn):
    """
    The DBconn class, which should be usable for all SQL-based databases.
    You should not create objects of this Class!
    """
    
    def __init__(self):
        super().__init__()
        
    def close(self):
        pass
    
    def checkauth(self, id):
        self.csr.execute("select id, token, user, date from auth where id=%(id)s and valid=1", {"id":id})
        idrows = self.csr.fetchall()
        if len(idrows) > 1:
            raise ValueError("Not at most one row returned, at most one expected.")
        if len(idrows) < 1:
            return None
        else:
            return idrows[0][1]
    
    def indexfile(self, filedict):
        filename = filedict["filename"]
        uuhash = filedict["uuhash"]
        size = filedict["size"]
        mtime = filedict["mtime"]
        eventid = int(filedict["events"][0]["id"])
        
        self.csr.execute("select id, uuhash, size, UNIX_TIMESTAMP(mtime) from files where uuhash=%(uuhash)s", {"uuhash":uuhash})
        rows = self.csr.fetchall()
        if len(rows) > 1:
            raise ValueError("Not at most one row returned, at most one expected.")
        elif len(rows) == 1:
            if rows[0][2] == int(size):
                return rows[0][0]
            raise Exception("File with same uuhash, but other size found")
        
        self.csr.execute("insert into files (uuhash, origname, size, mtime, event) values (%(uuhash)s, %(name)s, %(size)s, FROM_UNIXTIME(%(mtime)s), %(eventid)s)", {"uuhash": uuhash, "name":filename, "size":size, "mtime":mtime, "eventid":eventid})
        self.conn.commit() 
        
        return self.csr.lastrowid
    
    def updatefile(self, id, key, value):
        self.csr.execute("update files set "+key+"=%(value)s where id=%(id)s", {"value":value, "id":id})
        self.conn.commit()
    
    def getfileprop(self, id):
        self.csr.execute("select id, origname, uuhash, size, UNIX_TIMESTAMP(mtime), event, md5, path from files where id=%(id)s", {"id":id})
        idrows = self.csr.fetchall()
        if len(idrows) != 1:
            raise ValueError("Not exactly one row returned, one expected.")
        idrow = idrows[0]
        return {"id":       str(idrow[0]),
                "filename": idrow[1],
                "uuhash":   idrow[2],
                "size":     idrow[3],
                "mtime":    idrow[4],
                "event":   idrow[5],
                "md5":      idrow[6],
                "path":     idrow[7]}
        
class DBmysql(DBconnsql):
    """
    This is the concrete class for a mysql database backend.
    """
    def __init__(self, user, password, host="localhost", database="videoag"):
        self.conn = mysql.connector.connect(user=user,
                                            password=password,
                                            host=host,
                                            database=database)
        self.csr = self.conn.cursor()
    
    def close(self):
        self.conn.close()


class DBsqlite(DBconnsql):
    """
    This is the concrete class for a sqlite3 database backend.
    """
    
    def __init__(self, path):
        super().__init__()
        self.conn = sqlite3.connect(path)
        self.csr = self.conn.cursor()
        
    def close(self):
        self.conn.close()
    