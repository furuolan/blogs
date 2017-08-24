#!/bin/bash
virtualenv project_env
source project_env/bin/activate;
pip install -r requirements.txt;
zappa deploy dev;