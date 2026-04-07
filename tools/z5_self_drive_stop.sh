#!/usr/bin/env bash
set -euo pipefail

STATE_DIR="${CODEX_STATE_DIR:-$HOME/.codex/self_drives/zeta5_autoresearch}"
PID_FILE="$STATE_DIR/runner.pid"

if [[ ! -f "$PID_FILE" ]]; then
  echo "No PID file found; loop already stopped"
  exit 0
fi

pid="$(cat "$PID_FILE" 2>/dev/null || true)"
if [[ -z "${pid:-}" ]]; then
  echo "PID file is empty; removing it"
  rm -f "$PID_FILE"
  exit 0
fi

if ! kill -0 "$pid" 2>/dev/null; then
  echo "Process $pid is not running; removing stale PID file"
  rm -f "$PID_FILE"
  exit 0
fi

kill "$pid"
for _ in 1 2 3 4 5; do
  if ! kill -0 "$pid" 2>/dev/null; then
    echo "Stopped PID $pid"
    rm -f "$PID_FILE"
    exit 0
  fi
  sleep 1
done

kill -9 "$pid" 2>/dev/null || true
rm -f "$PID_FILE"
echo "Force-stopped PID $pid"
