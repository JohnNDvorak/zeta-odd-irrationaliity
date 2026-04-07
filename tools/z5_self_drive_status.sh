#!/usr/bin/env bash
set -euo pipefail

STATE_DIR="${CODEX_STATE_DIR:-$HOME/.codex/self_drives/zeta5_autoresearch}"
PID_FILE="$STATE_DIR/runner.pid"
SESSION_FILE="$STATE_DIR/session_id"
LATEST_MESSAGE="$STATE_DIR/latest_message.txt"
RUNNER_LOG="$STATE_DIR/runner.log"
RUN_DIR="$STATE_DIR/runs"

echo "State dir: $STATE_DIR"

if [[ -f "$PID_FILE" ]]; then
  pid="$(cat "$PID_FILE" 2>/dev/null || true)"
  if [[ -n "${pid:-}" ]] && kill -0 "$pid" 2>/dev/null; then
    echo "Status: running"
    echo "PID: $pid"
  else
    echo "Status: stale pid file"
    echo "PID file: $pid"
  fi
else
  echo "Status: stopped"
fi

if [[ -f "$SESSION_FILE" ]]; then
  echo "Thread: $(cat "$SESSION_FILE")"
elif compgen -G "$RUN_DIR/*.jsonl" > /dev/null; then
  latest_json="$(ls -1t "$RUN_DIR"/*.jsonl | head -n 1)"
  thread_id="$(sed -n 's/.*"thread_id":"\([^"]*\)".*/\1/p' "$latest_json" | head -n 1)"
  if [[ -n "${thread_id:-}" ]]; then
    echo "Bootstrap thread: $thread_id"
  fi
fi

if [[ -f "$LATEST_MESSAGE" ]]; then
  echo
  echo "Latest message:"
  sed -n '1,20p' "$LATEST_MESSAGE"
fi

if [[ -f "$RUNNER_LOG" ]]; then
  echo
  echo "Runner log tail:"
  tail -n 20 "$RUNNER_LOG"
fi
