#!/bin/bash

DIR=/usr/local/aqua-etl
cd ${DIR}

export FLASK_APP=${DIR}/aqua-server.py

source ${DIR}/venv/bin/activate

flask run --port=8000  --host=0.0.0.0

