#!/bin/bash

cd -- "$(dirname "$BASH_SOURCE")"
python3 main.py
read -n 1 -s -r -p ""
