#!/usr/bin/env bash
# install.sh -- install wc-py's project-level dependencies, then EXIT.
#
# Runs as an unprivileged user: no sudo, no system package manager, no system
# services. It installs only into the active Python environment, is safe to
# re-run, and never starts a server (wc-py has none -- it is a CLI).
# System prerequisites (a Python 3.8+ interpreter) are listed in INSTALL.md.
set -euo pipefail
cd "$(dirname "$0")"

PYTHON="${PYTHON:-python3}"

echo "wc-py setup"
echo

echo "[1/4] Updating Python packaging tools"
"$PYTHON" -m pip install --upgrade pip setuptools wheel

echo
echo "[2/4] Installing declared dependencies from requirements.txt"
"$PYTHON" -m pip install -r requirements.txt

echo
echo "[3/4] Installing the wc-py console script (editable, local only)"
"$PYTHON" -m pip install --no-build-isolation -e .

echo
echo "[4/4] Verifying the tool imports and counts correctly"
"$PYTHON" -c "import wc; assert wc.count_words('examples/notes.txt') == 12; print('wc.py: import ok, examples/notes.txt -> 12 words')"

echo
echo "Setup complete."
echo "  Run the tool      : python3 wc.py examples/notes.txt"
echo "  Or the script     : wc-py examples/notes.txt"
echo "  Recordable demo   : bash demo.sh"
echo "  Test suite        : python3 -m pytest   (or python3 -m unittest)"
echo "  Help              : python3 wc.py --help"
