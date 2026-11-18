#!/usr/bin/env bash
# Installs requirements.txt into the repo's .venv (created if missing)
set -euo pipefail

cd "$(dirname "$0")"

if [ ! -d .venv ]; then
  python -m venv .venv
fi

# Windows (Git Bash) keeps the interpreter in Scripts/, Linux and macOS in bin/
if [ -f .venv/Scripts/python.exe ]; then
  PYTHON=.venv/Scripts/python.exe
else
  PYTHON=.venv/bin/python
fi

"$PYTHON" -m pip install -r requirements.txt
echo "Requirements installed in .venv"
