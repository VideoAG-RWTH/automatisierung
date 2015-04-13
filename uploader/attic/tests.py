#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

class MP2T(object):
    NAME="mp2t"
    def __init__(self):
        self.left = 4
        self.read = 0
        self.good = True
    
    def update(self, data):
        read = len(data)
        ret = read
        if self.good:
            while read > self.left:
                read-=self.left
                self.read+=self.left
                if not data[-read] == 71: #b"G"[0]=71
#                    raise Exception(self.read)
                    self.good=False
                self.left = 192
            self.left-=read
        return ret
            
    def final(self):
        return {"mp2t": (self.good,"")}

if __name__ == "__main__":
    for i in range(2, len(sys.argv)):
        filename = sys.argv[i]
        print(filename + ":")
        try:
            if sys.argv[1] == "MP2T":
                file = open(filename, "rb")
                obj = MP2T()
                read=1
                while read>0:
                    read = obj.update(file.read(8192))
            print(" passed")
        except Exception as err:
            print(" failed with " + str(format(err)))
            

alltests = [MP2T]