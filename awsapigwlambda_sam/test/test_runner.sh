#!/usr/bin/env bash
set -x
cd test
export PYTHONPATH=$(pwd)/../src
pytest .
