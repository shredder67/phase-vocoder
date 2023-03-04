#!/bin/bash

if [ ! -d "env" ]; then
    echo "Creating virtual environment and installing dependencies..."
    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt
else
    echo "Env located, installing missing deps..."
    source env/bin/activate
    pip install -q -r requirements.txt
fi

echo "Env ready, executing script!"
python3 main.py $1 $2 $3
