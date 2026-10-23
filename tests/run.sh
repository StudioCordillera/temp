#!/bin/sh
# Build every program, check the round trip, then run all four suites in
# the TI-BASIC harness. Results go to tests/results.txt.
set -e
cd "$(dirname "$0")/.."
./build.sh
.venv/bin/python tests/run_tests.py "$@"
