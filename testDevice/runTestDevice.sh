#!/bin/bash
export FLASK_APP=testDevice.py
export FLASK_DEBUG=1
export FLASK_RUN_PORT=5000
export FLASK_RUN_HOST=127.0.0.1
flask run
