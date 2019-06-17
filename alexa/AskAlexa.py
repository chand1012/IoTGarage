import logging
import os

import requests
from flask import Flask, render_template

from flask_ask import Ask, question, request, session, statement

HOST = os.environ["HOST"]
PORT = os.environ["PORT"]
URL = "http://{}:{}".format(HOST, PORT)

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.launch
def launch():
    return open_garage_door()

@ask.intent("OpenGarageDoor")
def open_garage_door():
    recv = requests.get(URL + "/garageDoor/toggleGarage")
    if recv.status_code==200:
        output = render_template("garagesuccess")
        title = render_template("title")
        return statement(output).simple_card(title, output)
    else:
        output = render_template("failure")
        title = render_template("title")
        return statement(output).simple_card(title, output)

@ask.intent("toggleLamp")
def toggle_lamp():
    recv = requests.get(URL + "/chandlerLamp/lampSwitch")
    if recv.status==200:
        output = render_template("lampsuccess")
        title = render_template("title")
        return statement(output).simple_card(title, output)
    else:
        output = render_template("failure")
        title = render_template("title")
        return statement(output).simple_card(title, output)

@ask.intent("doAThing")
def do_a_thing():
    recv = requests.get(URL + "/chandlerLamp/lampSwitch")
    if recv.status==200:
        output = render_template("testdevice")
        title = render_template("title")
        return statement(output).simple_card(title, output)
    else:
        output = render_template("failure")
        title = render_template("title")
        return statement(output).simple_card(title, output)

@ask.session_ended
def session_ended():
    return "{}", 200

if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(host="0.0.0.0", port=12420,debug=True)