#!/usr/bin/env python3

from flask import Flask
from flask import render_template

import http.client
import json

import config

app = Flask(__name__)
app.config.from_object('config')

def reqapi(token, request, data={}):
	req = {}
	req["request"] = request
	req["token"] = token
	req["data"] = data
	conn = http.client.HTTPConnection("localhost", 8080)
	conn.request("POST", "/uploadapi/metaserver.py", json.dumps(req))

@app.route('/')
def index():
	events = reqapi("aab8d0dc34b59ee9e804f1261a2da9a82feafb64054cd40c4a62fa0767aed228096e558b13452623579208ed33904c6762c4ad625c4e7b25c2b2688e2e5ebb0c", "getunindexed")
	return render_template("index.html", events=events)

if __name__ == '__main__':
	app.run(debug=True)

