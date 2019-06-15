from flask import Flask, Response, request, render_template
import json
import requests

app = Flask(__name__)

DEVICES = None
with open("devices.json") as f:
    rawjson = f.read()
    DEVICES = json.loads(rawjson)

def sendCommand(device, command):
    d = DEVICES[device]
    host = d["host"]
    port = ""
    if int(d["port"])!=80 or d["port"]!=None:
        port = d["port"]
    url = "http://{}:{}/{}".format(host, port, command)
    recv = requests.get(url)
    return recv.status_code

@app.route("/", methods = ["GET"])
def index(): # this will be the remote page for if I cannot access the alexas
    return render_template("index.html", devices=DEVICES, rawdevices=json.dumps(DEVICES))

@app.route("/<string:device>/<string:command>")
def devicehandler(device, command):
    recv = sendCommand(device, command)
    return Response(status=recv)

if __name__=='__main__':
    app.run(host='0.0.0.0', port=55555, debug=True)
