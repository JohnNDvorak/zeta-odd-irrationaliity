#!/usr/bin/env bash
set -euo pipefail

ROOT="/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch"
STATE_DIR="${CODEX_STATE_DIR:-$HOME/.codex/self_drives/zeta5_autoresearch}"
RUN_DIR="$STATE_DIR/runs"
PID_FILE="$STATE_DIR/runner.pid"
SESSION_FILE="$STATE_DIR/session_id"
LATEST_MESSAGE="$STATE_DIR/latest_message.txt"
RUNNER_LOG="$STATE_DIR/runner.log"
BOOTSTRAP_PROMPT="$ROOT/tools/prompts/Z5_SELF_DRIVE_BOOTSTRAP_2026-04-02.txt"
CONTINUE_PROMPT="$ROOT/tools/prompts/Z5_SELF_DRIVE_CONTINUE_2026-04-02.txt"

MODEL="${CODEX_MODEL:-gpt-5.4}"
REASONING_EFFORT="${CODEX_REASONING_EFFORT:-high}"
SLEEP_SECS="${CODEX_LOOP_SLEEP_SECS:-5}"
MAX_RUNS="${CODEX_MAX_RUNS:-0}"

mkdir -p "$RUN_DIR"

log() {
  printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" | tee -a "$RUNNER_LOG" >&2
}

if [[ -f "$PID_FILE" ]]; then
  old_pid="$(cat "$PID_FILE" 2>/dev/null || true)"
  if [[ -n "${old_pid:-}" ]] && kill -0 "$old_pid" 2>/dev/null; then
    log "Loop already running with PID $old_pid"
    exit 1
  fi
fi

echo "$$" > "$PID_FILE"
trap 'rm -f "$PID_FILE"' EXIT

extract_thread_id() {
  local json_file="$1"
  sed -n 's/.*"thread_id":"\([^"]*\)".*/\1/p' "$json_file" | head -n 1
}

sync_latest_symlinks() {
  local json_file="$1"
  local msg_file="$2"
  ln -sfn "$json_file" "$RUN_DIR/latest.jsonl"
  ln -sfn "$msg_file" "$RUN_DIR/latest.txt"
}

run_bootstrap() {
  local stamp="$1"
  local json_file="$RUN_DIR/${stamp}_bootstrap.jsonl"
  local msg_file="$RUN_DIR/${stamp}_bootstrap.txt"

  log "Starting fresh Codex session"
  if codex --search exec \
      -C "$ROOT" \
      --dangerously-bypass-approvals-and-sandbox \
      -c "model_reasoning_effort=\"$REASONING_EFFORT\"" \
      -m "$MODEL" \
      --json \
      -o "$LATEST_MESSAGE" \
      - < "$BOOTSTRAP_PROMPT" > "$json_file" 2>&1; then
    :
  else
    local status=$?
    cp -f "$LATEST_MESSAGE" "$msg_file" 2>/dev/null || true
    sync_latest_symlinks "$json_file" "$msg_file"
    log "Bootstrap run failed with status $status"
    return "$status"
  fi

  cp -f "$LATEST_MESSAGE" "$msg_file" 2>/dev/null || true
  sync_latest_symlinks "$json_file" "$msg_file"

  local thread_id
  thread_id="$(extract_thread_id "$json_file")"
  if [[ -z "$thread_id" ]]; then
    log "Could not extract thread id from bootstrap output"
    return 1
  fi
  printf '%s\n' "$thread_id" > "$SESSION_FILE"
  log "Bootstrap completed; thread id $thread_id"
}

run_continue() {
  local stamp="$1"
  local json_file="$RUN_DIR/${stamp}_continue.jsonl"
  local msg_file="$RUN_DIR/${stamp}_continue.txt"
  local thread_id
  thread_id="$(cat "$SESSION_FILE")"

  log "Continuing Codex session $thread_id"
  if codex --search exec resume \
      "$thread_id" \
      --dangerously-bypass-approvals-and-sandbox \
      -c "model_reasoning_effort=\"$REASONING_EFFORT\"" \
      -m "$MODEL" \
      --json \
      -o "$LATEST_MESSAGE" \
      - < "$CONTINUE_PROMPT" > "$json_file" 2>&1; then
    :
  else
    local status=$?
    cp -f "$LATEST_MESSAGE" "$msg_file" 2>/dev/null || true
    sync_latest_symlinks "$json_file" "$msg_file"
    log "Continue run failed with status $status"
    return "$status"
  fi

  cp -f "$LATEST_MESSAGE" "$msg_file" 2>/dev/null || true
  sync_latest_symlinks "$json_file" "$msg_file"
  log "Continue completed"
}

should_stop() {
  if [[ ! -f "$LATEST_MESSAGE" ]]; then
    return 1
  fi

  local first_line
  first_line="$(head -n 1 "$LATEST_MESSAGE" | tr -d '\r')"

  case "$first_line" in
    "SELF-DRIVE STOP: PROVED")
      log "Received PROVED stop marker"
      return 0
      ;;
    "SELF-DRIVE STOP: BLOCKED")
      log "Received BLOCKED stop marker"
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

count=0
while :; do
  stamp="$(date '+%Y%m%d_%H%M%S')"

  if [[ -s "$SESSION_FILE" ]]; then
    if ! run_continue "$stamp"; then
      log "Resume failed; clearing saved session id and retrying from fresh bootstrap on next cycle"
      rm -f "$SESSION_FILE"
      sleep "$SLEEP_SECS"
      continue
    fi
  else
    run_bootstrap "$stamp"
  fi

  count=$((count + 1))
  if should_stop; then
    exit 0
  fi

  if [[ "$MAX_RUNS" -gt 0 && "$count" -ge "$MAX_RUNS" ]]; then
    log "Reached CODEX_MAX_RUNS=$MAX_RUNS; stopping loop"
    exit 0
  fi

  sleep "$SLEEP_SECS"
done
