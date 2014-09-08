# -*- coding: utf-8 -*-

class logger(object):
    def __init__(self, logconf, db):
        self.db = db
        self.id = db.newlogid()
        self.level = logconf["loglevel"]
    
    def log(self, level, msg):
        if level <= self.level:
            self.db.log(self.id, level, msg)