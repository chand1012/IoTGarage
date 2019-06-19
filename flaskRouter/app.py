from flask import Flask, Response, render_template, redirect, request
import json
import requests

app = Flask(__name__)

DEVICES = None
with open("devices.json") as f:
    rawjson = f.read()
    DEVICES = json.loads(rawjson)

def sendCommand(device, command, resp=0):
    d = DEVICES[device]
    host = d["host"]
    port = ""
    if int(d["port"])!=80 or d["port"]!=None:
        port = d["port"]
    url = "http://{}:{}/{}".format(host, port, command)
    recv = None
    try:
        recv = requests.get(url, timeout=3)
    except:
        if not resp:
            return 500
        else:
            return recv
    else:
        if not resp:
            return recv.status_code
        else:
            return recv

@app.route("/")
def index(): 
    return redirect("https://blog.chand1012.net/")

@app.route("/<string:device>/<string:command>", methods=["POST", "GET"])
def devicehandler(device, command):
    if request.method=="GET":
        d = DEVICES[device]
        if not command in d["commands"]:
            return Response(status=404)
        else:
            recv = sendCommand(device, command)
            return Response(status=recv)
    elif request.method=="POST":
        d = DEVICES[device]
        if not command in d["commands"]:
            return Response(status=404)
        else:
            recv = sendCommand(device, command, 1)
            Response(recv.text, status=200)


if __name__=='__main__':
    app.run(host='0.0.0.0', port=55555, debug=True)
