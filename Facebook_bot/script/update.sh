#!/bin/bash
source project_env/bin/activate;
pip install -r requirements.txt;
zappa update dev;