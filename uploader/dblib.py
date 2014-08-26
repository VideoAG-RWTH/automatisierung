#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

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
    
    def indexfile(self, filename, uuhash, size, mtime, event, date):
        pass
    
    def updatefile(self, id, key, value):
        pass
    
    def getfileprop(self, id):
        pass
    
    def getfilename(self, id):
        prop = self.getfileprop(id)
        return prop["event"]+"-"+prop["date"]+"-"+prop["filename"]

class DBconnsql(DBconn):
    """
    The DBconn class, which should be usable for all SQL-based databases.
    You should not create objects of this Class!
    """
    
    def __init__(self):
        super().__init__()
        
    def close(self):
        pass
    
    def checkauth(self, token):
        self.csr.execute("select user from auth where token=:token", {"token":token})
        self.conn.commit()
        idrows = self.csr.fetchall()
        if len(idrows) > 1:
            raise ValueError("Not at most one row returned, at most one expected.")
        if len(idrows) < 1:
            return False
        else:
            return True
    
    def indexfile(self, filename, uuhash, size, mtime, event, date):
        self.csr.execute("insert into files (uuhash, origname, size, mtime, event, date) values (:uuhash, :name, :size, :mtime, :event, :date)", {"uuhash": uuhash, "name":filename, "size":size, "mtime":mtime, "event":event, "date":date})
        self.conn.commit()        
        self.csr.execute("select id from files order by id desc limit 1")
        idrows = self.csr.fetchall()
        if len(idrows) != 1:
            raise ValueError("Not exactly one row returned, one expected.")
        return idrows[0][0]
    
    def updatefile(self, id, key, value):
        self.csr.execute("update files set "+key+"=:value where id=:id", {"key":key, "value":value, "id":id})
        self.conn.commit()
    
    def getfileprop(self, id):
        self.csr.execute("select origname, uuhash, size, mtime, event, date, md5, path from files where id=:id", {"id":id})
        self.conn.commit()
        idrows = self.csr.fetchall()
        if len(idrows) != 1:
            raise ValueError("Not exactly one row returned, one expected.")
        idrow = idrows[0]
        return {"filename": idrow[0],
                "uuhash":   idrow[1],
                "size":     idrow[2],
                "mtime":    idrow[3],
                "event":    idrow[4],
                "date":     idrow[5],
                "md5":      idrow[6],
                "path":     idrow[7]}
        
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
    