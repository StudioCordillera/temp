#!/bin/sh
# Rebuild every MATHKIT program and check it. Creates .venv on first run.
set -e
cd "$(dirname "$0")"
if [ ! -x .venv/bin/python ]; then
  python3 -m venv .venv
  .venv/bin/pip install -q "tivars==1.1.1"
fi
.venv/bin/python tools/build.py
