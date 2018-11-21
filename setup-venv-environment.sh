#!/bin/bash

python3 -m venv ${PWD}/venv

source venv/bin/activate

# This will install all the packages required by dynasimpy into your venv
pip install dynasimpy

pip install -r development-packages-list.txt
