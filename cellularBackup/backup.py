from json import loads
from Hologram.HologramCloud import HologramCloud
import requests

def getNumbers(filename="numberlist.txt"):
    returnlist = []
    with open(filename) as f:
        returnlist = f.readlines()
    return returnlist

print("Getting API key...")
key = ""
with open("key.json") as f:
    raw = loads(f.read())
    key = raw["key"]

creds = {'devicekey' : key}

print("Logging into Hologram Cloud Network....")
cloud = HologramCloud(creds, network='cellular')

cloud.enableSMS()

while True:
    sms = cloud.popRecievedSMS()
    print("Waiting for SMS message...")
    while sms==None:
       pass
    print("Message {} from {}".format(sms.message, sms.sender))
    if sms.sender + "\n" in getNumbers():
        if "garage" in sms.message.lower():
            requests.get("http://localhost:55555/garageDoor/toggleGarage")
        elif "lamp" in sms.message.lower():
            requests.get("http://localhost:55555/chandlerLamp/lampSwitch")
    