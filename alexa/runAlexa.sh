#!/bin/bash
export HOST=localhost
export PORT=55555
export FLASK_APP=AskAlexa.py
export FLASK_RUN_PORT=12420
export FLASK_RUN_HOST=127.0.0.1
export FLASK_DEBUG=1
flask run
