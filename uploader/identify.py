# -*- coding: utf-8 -*-

def identify(filearray):
    #filearray: [{"filename": filename, "mtime": mtime, "size": size, ...}]
    for file in filearray:
        events = []
        for foundevent in [{"event":"foo", "date":"26082014"}]:
            events.append(foundevent)
        file["events"] = events
    return filearray