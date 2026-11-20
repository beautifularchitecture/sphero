#!/usr/bin/env bash
# Start the U3 SPA dev server. Run ./backend.sh in another terminal first.
set -euo pipefail

cd "$(dirname "$0")"

if ! command -v npm >/dev/null 2>&1; then
  echo "npm is required." >&2
  exit 1
fi

if [[ ! -d node_modules ]]; then
  echo "Installing frontend dependencies..."
  npm install
fi

echo "Opening http://localhost:5173"
echo "Proxies: /ws/chat -> 8000, /ws/robot-state -> 8001"
exec npm run dev
