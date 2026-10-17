#!/usr/bin/env sh
set -eu

PYTHONPATH=/opt/debug-gym /opt/debug-gym/bin/python -m app.server &

exec code-server \
  --auth none \
  --bind-addr 0.0.0.0:8080 \
  --disable-telemetry \
  --extensions-dir /opt/debug-gym/extensions \
  /home/coder/project
