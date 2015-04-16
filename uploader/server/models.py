#!/usr/bin/env python3

from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

class AlreadyExists(Exception):
	pass

Base = declarative_base()

class User(Base):
	__tablename__ = 'user'
	id = Column(Integer, primary_key=True)
	token = Column(String(128), nullable=False, unique=True)
	name = Column(String(20), nullable=False)
	created = Column(DateTime, default=func.now())
	active = Column(Boolean, default=True)

class Upload(Base):
	__tablename__ = 'upload'
	id = Column(Integer, primary_key=True)
	time = Column(DateTime, default=func.now())
	user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
	user = relationship(User)

class Cluster(Base):
	__tablename__ = 'clusters'
	id = Column(Integer, primary_key=True)

class File(Base):
	__tablename__ = 'files'
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	uuhash = Column(String(250), nullable=False, unique=True)
	path = Column(String(250), nullable=True)
	size = Column(Integer, nullable=False)
	mtime = Column(DateTime, default=func.now())
	md5 = Column(String(32), nullable=True, unique=True)
	upload_id = Column(Integer, ForeignKey('upload.id'), nullable=False)
	upload = relationship(Upload)
	cluster_id = Column(Integer, ForeignKey('clusters.id'), nullable=True)
	cluster = relationship(Cluster)

class Eventconnector(Base):
	__tablename__ = 'fileevents'
	id = Column(Integer, primary_key=True)
	cluster = relationship(Cluster)
	cluster_id = Column(Integer, ForeignKey('clusters.id'), nullable=False)
	event = Column(Integer, nullable=False)
	confirmed = Column(Boolean, default=False)
	
	relunique = UniqueConstraint('cluster_id', 'event')
	relunique = UniqueConstraint('cluster_id', 'confirmed')

