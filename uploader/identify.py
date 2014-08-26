# -*- coding: utf-8 -*-

def identify(filearray):
    #filearray: [{"filename": filename, "mtime": mtime, "size": size, ...}]
    for file in filearray:
        dates = []
        events = []
        events.append("foo")
        dates.append("26082014")
        file["events"] = events
        file["dates"] = dates
    return filearray