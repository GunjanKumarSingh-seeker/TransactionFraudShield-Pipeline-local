#!/usr/bin/env bash
set -euo pipefail

python -m compileall fraud_shield scripts
pytest -q
