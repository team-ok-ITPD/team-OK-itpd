#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/.."
python3 "$SCRIPT_DIR/run_debug_gym.py"
if [ $? -ne 0 ]; then
  echo
  read -r -p "Press Enter to close..." _ || true
fi