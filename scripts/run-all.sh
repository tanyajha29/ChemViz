#!/usr/bin/env bash
set -euo pipefail

echo "== ChemViz run all =="

PY="backend/.venv/bin/python"
if [ -f "backend/.venv/Scripts/python" ]; then
  PY="backend/.venv/Scripts/python"
fi

cleanup() {
  if [ -n "${BACK_PID:-}" ]; then kill "$BACK_PID" 2>/dev/null || true; fi
  if [ -n "${WEB_PID:-}" ]; then kill "$WEB_PID" 2>/dev/null || true; fi
  if [ -n "${DESK_PID:-}" ]; then kill "$DESK_PID" 2>/dev/null || true; fi
}
trap cleanup EXIT

$PY backend/manage.py runserver &
BACK_PID=$!

(cd web-frontend/chemviz-web && npm run dev) &
WEB_PID=$!

$PY desktop-app/chemviz-desktop/main.py &
DESK_PID=$!

echo "Started backend (PID $BACK_PID), web (PID $WEB_PID), desktop (PID $DESK_PID)."
echo "Press Ctrl+C to stop."
wait
