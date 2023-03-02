#!/bin/bash

if [ ! -d "env" ]; then
    echo "Creating virtual environment and installing dependencies..."
    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt
else
    source env/bin/activate
fi

python3 main.py $1 $2 $3