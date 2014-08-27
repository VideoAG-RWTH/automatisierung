#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import filelib

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
    
    def getfilename(self, id):
        prop = self.getfileprop(id)
        #filename = prop["events"].split(" ")[0]+"-"+prop["dates"].split(" ")[0]+"-"+prop["filename"]
        filename = prop["id"]
        return filename
        

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
    
    def indexfile(self, filedict):
        filename = filedict["filename"]
        uuhash = filedict["uuhash"]
        size = filedict["size"]
        mtime = filedict["mtime"]
        eventdates = filedict["events"]
        
        eventdatedict = filelib.parseeventdates(eventdates)
        events = eventdatedict["events"]
        dates = eventdatedict["dates"]
        eventcount = eventdatedict["eventcount"]
        
        self.csr.execute("insert into files (uuhash, origname, size, mtime, events, dates, eventcount) values (:uuhash, :name, :size, :mtime, :events, :dates, :eventcount)", {"uuhash": uuhash, "name":filename, "size":size, "mtime":mtime, "events":events, "dates":dates, "eventcount":eventcount})
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
        self.csr.execute("select id, origname, uuhash, size, mtime, events, dates, md5, path from files where id=:id", {"id":id})
        self.conn.commit()
        idrows = self.csr.fetchall()
        if len(idrows) != 1:
            raise ValueError("Not exactly one row returned, one expected.")
        idrow = idrows[0]
        return {"id":       str(idrow[0]),
                "filename": idrow[1],
                "uuhash":   idrow[2],
                "size":     idrow[3],
                "mtime":    idrow[4],
                "events":   idrow[5],
                "dates":    idrow[6],
                "md5":      idrow[7],
                "path":     idrow[8]}
        
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
    