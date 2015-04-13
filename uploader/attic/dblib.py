#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
    
    def indexevent(self, fileid, events, delete=False):
        if delete:
            self.csr.execute("delete from fileevent where file=%(fileid)s", {"fileid": fileid})
            self.conn.commit()
        for event in events:
            eventid = event["lecture_id"]
            self.csr.execute("select id from fileevent where file=%(fileid)s and lecture=%(eventid)s", {"fileid":fileid, "eventid":eventid})
            rows = self.csr.fetchall()
            if len(rows) > 1:
                raise ValueError("Not at most one row returned, at most one expected.")
            elif len(rows) == 1:
                continue
            self.csr.execute("insert into fileevent (file, lecture) values (%(fileid)s, %(eventid)s)", {"fileid": fileid, "eventid":eventid})
            self.conn.commit()
    
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
                    "id":       eventrow[0],
                    "fileid":   eventrow[1],
                    "eventid":  eventrow[2],
                    }
            events.append(event)
        
        self.csr.execute("select filesubtest.data, filesubtest.good, subtest.name, tests.name from filesubtest join subtest on subtest.id=filesubtest.subtest join tests on tests.id=subtest.test where filesubtest.file=%(fileid)s", {"fileid":filerow[0]})
        subtestrows = self.csr.fetchall()
        subtests = []
        for row in subtestrows:
            subtest = {}
            subtest["testdata"] = row[0]
            subtest["good"] = row[1]
            subtest["subtestname"] = row[2]
            subtest["testname"] = row[3]
            subtests.append(subtest)
        
        self.csr.execute("select path from filepaths where fileid=%(fileid)s", {"fileid":filerow[0]})
        pathrows = self.csr.fetchall()
        
        paths = []
        for row in pathrows:
            paths.append(row[0])
        
        filedict = {
                    "id":       str(filerow[0]),
                    "filename": filerow[1],
                    "uuhash":   filerow[2],
                    "size":     filerow[3],
                    "mtime":    filerow[4],
                    "md5":      filerow[5],
                    "path":     filerow[6],
                    "events":   events,
                    "subtests": subtests,
                    "paths":    paths
                    }
        return filedict
        
    def adduser(self, user, token):
        self.csr.execute("update auth set valid=0 where user=%(user)s", {"user":user})
        self.csr.execute("insert into auth (user, token) values (%(user)s, %(token)s)", {"user": user, "token":token})
        self.conn.commit()
        
        return self.csr.lastrowid
    
    def newlogid(self):
        self.csr.execute("insert into logids (logid) VALUES (NULL)")
        return self.csr.lastrowid
    
    def log(self, id, level, msg):
        self.csr.execute("insert into log (level, logid, msg) values (%(level)s, %(logid)s, %(msg)s)", {"level": str(level), "logid":str(id), "msg":msg})
        self.conn.commit()
    
    def posstest(self, ending):
        self.csr.execute("select tests.name from endings join testending on endings.id=testending.ending join tests on testending.test=tests.id where endings.ending=%(ending)s", {"ending": ending})
        rows = self.csr.fetchall()
        tests = []
        for row in rows:
            tests.append(row[0])
        return tests
    
    def indextest(self, fileid, testname, data):
        self.csr.execute("select id from tests where name=%(name)s", {"name":testname})
        rows = self.csr.fetchall()
        if len(rows) != 1:
            raise ValueError("Not exactly one row returned, one expected.")
        testid = rows[0][0]
        self.csr.execute("select id, name from subtest where test=%(test)s", {"test":testid})
        rows = self.csr.fetchall()
        subtests = {}
        for row in rows:
            subtests[row[1]] = row[0]
        for key in data:
            self.csr.execute("insert into filesubtest (file, subtest, data, good) values (%(fileid)s, %(subtestid)s, %(data)s, %(good)s)", {"fileid":fileid, "subtestid":subtests[key], "good":data[key][0], "data":data[key][1]})
            self.conn.commit()
        
    def indexpath(self, fileid, path):
        self.csr.execute("insert into filepaths (fileid, path) values (%(fileid)s, %(path)s)", {"fileid":fileid, "path":path})
        self.conn.commit()
        
        
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


#class DBsqlite(DBconnsql):
#    """
#    This is the concrete class for a sqlite3 database backend.
#    BROKEN!
#    """
#    
#    def __init__(self, path):
#        super().__init__()
#        self.conn = sqlite3.connect(path)
#        self.csr = self.conn.cursor()
#        
#    def close(self):
#        self.conn.close()
