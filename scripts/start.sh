#!/usr/bin/env sh
set -eu

export PATH="/opt/debug-gym/bin:$PATH"
export PYTHONPATH=/opt/debug-gym

python -m app.server &

exec code-server \
  --auth none \
  --bind-addr 0.0.0.0:8080 \
  --disable-telemetry \
  --extensions-dir /opt/debug-gym/extensions \
  /home/coder/project
