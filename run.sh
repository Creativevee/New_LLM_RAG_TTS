#!/usr/bin/env bash
# One-shot launcher: sets up the venv, installs deps, starts the FastAPI
# backend on :8000 and serves the frontend on :5173.
#
# Usage:   ./run.sh
# Stop:    Ctrl+C  (both servers are torn down together)

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$ROOT/backend"
FRONTEND_DIR="$ROOT/frontend"
VENV_DIR="$BACKEND_DIR/.venv"
BACKEND_PORT="${BACKEND_PORT:-8000}"
FRONTEND_PORT="${FRONTEND_PORT:-5173}"

PY="${PYTHON:-python3}"
if ! command -v "$PY" >/dev/null 2>&1; then
  echo "error: $PY not found on PATH" >&2
  exit 1
fi

echo "==> Project root: $ROOT"

if [ ! -d "$VENV_DIR" ]; then
  echo "==> Creating virtualenv at $VENV_DIR"
  "$PY" -m venv "$VENV_DIR"
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

echo "==> Upgrading pip"
python -m pip install --upgrade pip >/dev/null

echo "==> Installing backend dependencies"
pip install -r "$BACKEND_DIR/requirements.txt"

cleanup() {
  echo
  echo "==> Shutting down"
  if [ -n "${BACKEND_PID:-}" ] && kill -0 "$BACKEND_PID" 2>/dev/null; then
    kill "$BACKEND_PID" 2>/dev/null || true
    wait "$BACKEND_PID" 2>/dev/null || true
  fi
  if [ -n "${FRONTEND_PID:-}" ] && kill -0 "$FRONTEND_PID" 2>/dev/null; then
    kill "$FRONTEND_PID" 2>/dev/null || true
    wait "$FRONTEND_PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT INT TERM

echo "==> Starting backend on http://127.0.0.1:$BACKEND_PORT"
(
  cd "$BACKEND_DIR"
  exec uvicorn main:app --reload --port "$BACKEND_PORT"
) &
BACKEND_PID=$!

echo "==> Starting frontend on http://127.0.0.1:$FRONTEND_PORT"
(
  exec python -m http.server "$FRONTEND_PORT" --directory "$FRONTEND_DIR"
) &
FRONTEND_PID=$!

echo
echo "Backend  PID $BACKEND_PID  →  http://127.0.0.1:$BACKEND_PORT"
echo "Frontend PID $FRONTEND_PID  →  http://127.0.0.1:$FRONTEND_PORT"
echo "Press Ctrl+C to stop."

# Poll until either server exits (portable: avoids `wait -n`, which needs bash >= 4.3).
while kill -0 "$BACKEND_PID" 2>/dev/null && kill -0 "$FRONTEND_PID" 2>/dev/null; do
  sleep 1
done
