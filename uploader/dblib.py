#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def checkauth(token, config):
    if token in ["moritz", "videoag"]:
        return True
    else:
        return False
        
def indexfile(uuhash, size, mtime, event, date):
    pass