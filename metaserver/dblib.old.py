#!/usr/bin/env python3

import mysql.connector

class DBConn(object):
	def __init__(self, conf):
		self.conn = mysql.connector.connect(
			user=conf["dbuser"],
			password=conf["dbpass"],
			host=conf["dbhost"],
			database=conf["db"]
			)
		self.csr = self.conn.cursor()
		self.uploadid = None
	
	def close(self):
		self.conn.close()
	
	def getuid(self, token):
		self.csr.execute("select id from auth where token=%(token)s", {"token":token})
		idrows = self.csr.fetchall()
		if len(idrows) > 1:
			raise ValueError("Not at most one row returned, at most one expected.")
		if len(idrows) < 1:
			return 0;
		else:
			return idrows[0][0]
	
	def indexupload(self):
		self.csr.execute("insert into uploads (id, date) values (id, NOW())")
		self.uploadid = self.csr.lastrowid
		return self.uploadid
	
	def indexfile(self, data):
		if self.uploadid == None:
			self.uploadid = self.indexupload()
		self.csr.execute("""insert into files
			(uuhash, origname, size, mtime, uploadid)
			values
			(%(uuhash)s, %(name)s, %(size)s, FROM_UNIXTIME(%(mtime)s), %(uploadid)s)""",
			{"uuhash": data["uuhash"], "name":data["filename"], "size":data["size"], "mtime":data["mtime"], "uploadid":self.uploadid})
		self.conn.commit()
		fileid = self.csr.lastrowid
		return fileid
	
