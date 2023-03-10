#!/bin/bash

virtualenv -p $(which python) venv \
&& source venv/bin/activate \
&& pip3 install -r requirements.txt