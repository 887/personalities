#!/usr/bin/env bash
# Thin shim around render-furry-skills.py so the entry point reads as a
# shell script and stays familiar in PATH-style invocations.
set -euo pipefail
cd "$(dirname "$0")/.."
exec python3 scripts/render-furry-skills.py "$@"
