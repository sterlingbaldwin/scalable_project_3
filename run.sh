#!/bin/sh
ssh 10.35.70.30

python3 -m venv .venv
source ./venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cd ./src

python controller_manager.py > controller.log &

python entity_manager.py > entity.log &

python main.py