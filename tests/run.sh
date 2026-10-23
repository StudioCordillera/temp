#!/bin/sh
# Build every program, check the round trip, run the static lint tests and
# a fixed-seed random-input sweep, then run all four suites in the TI-BASIC
# harness. Results go to tests/results.txt.
set -e
cd "$(dirname "$0")/.."
./build.sh
.venv/bin/python tests/test_static.py
for seed in 1 2 3; do .venv/bin/python tests/fuzz.py $seed 2000; done
.venv/bin/python tests/run_tests.py "$@"
