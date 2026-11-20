#!/usr/bin/env bash
# Start the Sphero chat-control backends from the workspace root.
#   U1: FastAPI chat + SPA on 8000
#   U2: BLE telemetry /ws/robot-state on 8001 (only with U2_BLE_ADDRESS set)
set -euo pipefail

cd "$(dirname "$0")"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required." >&2
  exit 1
fi

if [[ ! -f .env ]]; then
  echo "Warning: no .env found. The SPA and /health work without it, but chat" >&2
  echo "         needs OPENROUTER_API_KEY in .env or the environment." >&2
fi

echo "Starting U1 chat backend on http://127.0.0.1:8000"
python3 -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 &
U1_PID=$!

U2_PID=""
if [[ -n "${U2_BLE_ADDRESS:-}" ]]; then
  echo "Starting U2 telemetry on ws://127.0.0.1:8001/ws/robot-state"
  U2_WS_PORT=8001 python3 -m u2_telemetry &
  U2_PID=$!
else
  echo "U2 telemetry not started (set U2_BLE_ADDRESS to your Sphero Mini's address)."
fi

cleanup() {
  kill "$U1_PID" 2>/dev/null || true
  if [[ -n "$U2_PID" ]]; then
    kill "$U2_PID" 2>/dev/null || true
  fi
  wait 2>/dev/null || true
}
trap cleanup EXIT

echo "Now run ./frontend.sh in another terminal and open http://localhost:5173"
if [[ -n "$U2_PID" ]]; then
  wait "$U1_PID" "$U2_PID"
else
  wait "$U1_PID"
fi
