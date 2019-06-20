import discord
import requests
from bs4 import BeautifulSoup

from json_extract import json_extract

HOST = json_extract("host")
PORT = json_extract("port")
URL = "http://{}:{}".format(HOST, PORT)
token = json_extract("token")
me = json_extract("admin")
client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if not me in str(message.author):
        print(message.author)
        return
    if message.content.lower().startswith("!opengaragedoor") or message.content.lower().startswith("!closegaragedoor"):
        req = requests.get(URL + "/garageDoor/toggleGarage")
        if req.status_code==200:
            msg = ""
            if "open" in message.content.lower():
                msg = "Garage Door opened successfully!"
            else:
                msg = "Garage Door closed successfully!"
            await message.channel.send(content=msg)
            return
        else:
            msg = "There was an error with your request: server returned code {}.".format(req.status_code)
            await message.channel.send(content=msg)
            return
    
    if message.content.lower().startswith("!turnonlamp") or message.content.lower().startswith("!turnofflamp"):
        req = requests.get(URL + "/chandlerLamp/lampSwitch")
        if req.status_code==200:
            msg = ""
            if "on" in message.content.lower():
                msg = "Lamp turned on successfully!"
            else:
                msg = "Lamp turned off successfully!"
            await message.channel.send(content=msg)
            return
        else:
            msg = "There was an error with your request: server returned code {}.".format(req.status_code)
            await message.channel.send(content=msg)
            return
    
    if message.content.lower().startswith("!doathing"):
        req = requests.get(URL + "/testDevice/doAThing")
        if req.status_code==200:
            await message.channel.send(content="Did nothing successfully!")
        else:
            await message.channel.send(content="Failed to do nothing! Error code {}.".format(req.status_code))
        return

    if message.content.lower().startswith("!getathing"):
        req = requests.post(URL + "/testDevice/getAThing")
        if req.status_code==200:
            page = BeautifulSoup(req.content, "html.parser")
            await message.channel.send(content=page.p.text)
        else:
            await message.channel.send(content="Failed to get nothing! Error code {}.".format(req.status_code))

    if message.content.lower().startswith("!garagestatus"):
        req = requests.post(URL + "/garageDoor/getGarage")
        if req.status_code == 200:
            page = BeautifulSoup(req.content, "html.parser")
            msg = page.h1.text + "\n" + page.p.text
            await message.channel.send(content=msg)
            return
        else:
            msg = "There was an error with your request: server returned code {}.".format(req.status_code)
            await message.channel.send(content=msg)
            return

@client.event # the on_ready event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(token)
