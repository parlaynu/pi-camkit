#!/usr/bin/env bash

RUN_DIR="$( dirname "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" )"
cd ${RUN_DIR}

export PYTHONPATH=${RUN_DIR}
pytest-3 -v tests
# pytest -s -v .
