#!/bin/bash
set -e

fuser -k 8888/tcp 2>/dev/null || true

python3 src/main.py "/" || exit 1

cd docs
python3 -m http.server 8888 &

sleep 1
xdg-open 'http://localhost:8888'
