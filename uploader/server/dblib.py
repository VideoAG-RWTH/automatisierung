#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from models import *

import datetime
import identify

class DBConn(object):
	def __init__(self, uri):
		self.engine = create_engine(uri)
		self.DBSession = sessionmaker(bind=self.engine)
		self.session = self.DBSession()
		self.user = None
	
	def getuid(self, token):
		try:
			self.user = self.session.query(User).filter(User.token == token).one()
		except NoResultFound:
			return 0
		return self.user.id
	
	def indexupload(self):
		if self.user == None:
			raise Exception("Only autherized users can index uploads")
		upload = Upload(user=self.user)
		self.session.add(upload)
		return upload
	
	def indexfile(self, filedata, upload):
		if self.session.query(File).filter(File.uuhash==filedata["uuhash"]).count() >0:
			raise AlreadyExists()
		f = File(name=filedata["name"], uuhash=filedata["uuhash"], size=filedata["size"], mtime=datetime.datetime.fromtimestamp(filedata["mtime"]), upload=upload)
		self.session.add(f)
		return f
	
	def getuploadfiles(self, upload):
		return self.session.query(File).filter(File.upload == upload).all()
	
	def identify(self, upload):
		fileobjs = self.getuploadfiles(upload)
		files = []
		for fileobj in fileobjs:
			f = {}
			f["obj"] = fileobj
			f["name"] = fileobj.name
			f["mtime"] = fileobj.mtime.timestamp()
			f["size"] = fileobj.size
			files.append(f)
		clusters = identify.identify(files)
		for c in clusters:
			cobj = Cluster()
			self.session.add(cobj)
			for f in c["files"]:
				fobj = f["obj"]
				fobj.cluster = cobj
			for e in c["events"]:
				self.session.add(Eventconnector(cluster=cobj, event=e["lecture_id"]))
		
	
	def getfile(self, fileid):
		return self.session.query(Files).filter(File.id == fileid).one()
	
	def getunindexed(self, starttime, endtime):
		pass
	
	def getfilestocluster(self, cluster):
		return self.session.query(File).filter(File.cluster == cluster).all()
	
	def commit(self):
		self.session.commit()
	
	def close(self):
		self.commit()
