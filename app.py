from flask import Flask, Response, request
import json
import socket

def getDigitalPins(device):
    s = socket.socket()
    host = device["host"]
    port = device["port"]
    s.connect((host, port))
    s.send("outputs")
    data = s.recv(len(device["outputPins"]))
    rdata = {}
    count = 0
    for k in device["outputPins"]:
        rdata[str(k)] = int(list(data)[count])
        

app = Flask(__name__)

DEVICES = None
with open("devices.json") as f:
    rawjson = f.read()
    DEVICES = json.loads(rawjson)

@app.route("/", methods = ["GET"])
def index():
    return "Main Page"

@app.route("<string:device>", methods = ["POST", "GET"])
def devicehandler(deviceName):
    if request.method == "GET":
        
