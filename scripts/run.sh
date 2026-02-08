#!/usr/bin/env bash
set -euo pipefail

if [[ ! -d ".venv" ]]; then
  echo "[INFO] .venv not found. Run scripts/bootstrap.sh first."
  exit 1
fi

source .venv/bin/activate
pig "$@"
