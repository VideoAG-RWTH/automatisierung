#!/usr/bin/env python3

def auth(db, token):
	uid = db.getuid(token)
	return uid
