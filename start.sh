#!/bin/sh

mkdir -p server
python3 -m http.server -d server &
python3 anti-spam.py
