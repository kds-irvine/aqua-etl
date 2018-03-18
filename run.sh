#!/bin/bash

export FLASK_APP=aqua-server.py

nohup flask run --port=8000 > /tmp/run.log 2>&1 &

