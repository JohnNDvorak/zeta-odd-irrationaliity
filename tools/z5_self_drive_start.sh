#!/usr/bin/env bash
set -euo pipefail

ROOT="/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch"
STATE_DIR="${CODEX_STATE_DIR:-$HOME/.codex/self_drives/zeta5_autoresearch}"
PID_FILE="$STATE_DIR/runner.pid"
LAUNCH_LOG="$STATE_DIR/launcher.log"
LOOP_SCRIPT="$ROOT/tools/z5_self_drive_loop.sh"

MODEL="${CODEX_MODEL:-gpt-5.4}"
REASONING_EFFORT="${CODEX_REASONING_EFFORT:-high}"
SLEEP_SECS="${CODEX_LOOP_SLEEP_SECS:-5}"
MAX_RUNS="${CODEX_MAX_RUNS:-0}"

mkdir -p "$STATE_DIR"

if [[ -f "$PID_FILE" ]]; then
  old_pid="$(cat "$PID_FILE" 2>/dev/null || true)"
  if [[ -n "${old_pid:-}" ]] && kill -0 "$old_pid" 2>/dev/null; then
    echo "Already running with PID $old_pid"
    exit 0
  fi
fi

rm -f "$PID_FILE"
launcher_pid="$(
  CODEX_STATE_DIR="$STATE_DIR" \
  CODEX_MODEL="$MODEL" \
  CODEX_REASONING_EFFORT="$REASONING_EFFORT" \
  CODEX_LOOP_SLEEP_SECS="$SLEEP_SECS" \
  CODEX_MAX_RUNS="$MAX_RUNS" \
  /opt/homebrew/opt/python@3.11/libexec/bin/python3 - "$LOOP_SCRIPT" "$LAUNCH_LOG" <<'PY'
import os
import subprocess
import sys

loop_script = sys.argv[1]
launch_log = sys.argv[2]

with open(launch_log, "ab", buffering=0) as log:
    proc = subprocess.Popen(
        [loop_script],
        stdin=subprocess.DEVNULL,
        stdout=log,
        stderr=log,
        start_new_session=True,
        close_fds=True,
        env=os.environ.copy(),
    )

print(proc.pid)
PY
)"

sleep 1

if [[ -f "$PID_FILE" ]]; then
  new_pid="$(cat "$PID_FILE" 2>/dev/null || true)"
else
  new_pid="$launcher_pid"
fi

if [[ -n "${new_pid:-}" ]] && kill -0 "$new_pid" 2>/dev/null; then
  echo "Started zeta5 self-drive loop"
  echo "PID: $new_pid"
  echo "State dir: $STATE_DIR"
else
  echo "Failed to start zeta5 self-drive loop" >&2
  exit 1
fi
