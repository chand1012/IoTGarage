#!/bin/bash
export HOST=localhost
export PORT=55555
export FLASK_APP=AskAlexa.py
export FLASK_DEBUG=1
flask run --cert=cert.pem --key=key.pem
