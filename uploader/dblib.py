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
    
    def indexevent(self, fileid, events):
        for event in events:
            eventid = event["lecture_id"]
            self.csr.execute("select id from fileevent where file=%(fileid)s and lecture=%(eventid)s", {"fileid":fileid, "eventid":eventid})
            rows = self.csr.fetchall()
            if len(rows) > 1:
                raise ValueError("Not at most one row returned, at most one expected.")
            elif len(rows) == 1:
                continue
            self.csr.execute("insert into fileevent (file, lecture) values (%(fileid)s, %(eventid)s)", {"fileid": fileid, "eventid":eventid})
    
    def indexfile(self, filedict):
        filename = filedict["filename"]
        uuhash = filedict["uuhash"]
        size = filedict["size"]
        mtime = filedict["mtime"]
        events = filedict["events"]
        
        self.csr.execute("select id, uuhash, size, UNIX_TIMESTAMP(mtime) from files where uuhash=%(uuhash)s", {"uuhash":uuhash})
        rows = self.csr.fetchall()
        if len(rows) > 1:
            raise ValueError("Not at most one row returned, at most one expected.")
        elif len(rows) == 1:
            if rows[0][2] == int(size):
                fileid = rows[0][0]
                self.indexevent(fileid, events)
                return fileid
            raise Exception("File with same uuhash, but other size found")
        
        self.csr.execute("insert into files (uuhash, origname, size, mtime) values (%(uuhash)s, %(name)s, %(size)s, FROM_UNIXTIME(%(mtime)s))", {"uuhash": uuhash, "name":filename, "size":size, "mtime":mtime})
        self.conn.commit() 
        
        fileid = self.csr.lastrowid
        self.indexevent(fileid, events)
        return fileid
    
    def updatefile(self, id, key, value):
        self.csr.execute("update files set "+key+"=%(value)s where id=%(id)s", {"value":value, "id":id})
        self.conn.commit()
    
    def getfileprop(self, id):
        self.csr.execute("select id, origname, uuhash, size, UNIX_TIMESTAMP(mtime), md5, path from files where id=%(id)s", {"id":id})
        rows = self.csr.fetchall()
        if len(rows) != 1:
            raise ValueError("Not exactly one row returned, one expected.")
        filerow = rows[0]
        self.csr.execute("select id, file, lecture from fileevent where file=%(fileid)s", {"fileid":filerow[0]})
        eventrows = self.csr.fetchall()
        
        events = []
        for eventrow in eventrows:
            event = {
                    "lecture_id":   eventrow[0],
                    "fileid":       eventrow[1],
                    "eventid":      eventrow[2],
                    }
            events.append(event)
        
        filedict = {
                    "id":       str(filerow[0]),
                    "filename": filerow[1],
                    "uuhash":   filerow[2],
                    "size":     filerow[3],
                    "mtime":    filerow[4],
                    "md5":      filerow[5],
                    "path":     filerow[6],
                    "events":   events,
                    }
        return filedict
        
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
    