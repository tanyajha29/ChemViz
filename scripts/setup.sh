#!/usr/bin/env bash
set -euo pipefail

echo "== ChemViz setup =="

if [ ! -d "backend/.venv" ]; then
  echo "Creating virtual environment..."
  python -m venv backend/.venv
fi

PY="backend/.venv/bin/python"
if [ -f "backend/.venv/Scripts/python" ]; then
  PY="backend/.venv/Scripts/python"
fi

echo "Installing Python dependencies..."
$PY -m pip install --upgrade pip
$PY -m pip install -r requirements.txt

echo "Running migrations..."
$PY backend/manage.py migrate

echo "Installing web dependencies..."
cd web-frontend/chemviz-web
npm install
cd ../../

echo "Setup complete."
