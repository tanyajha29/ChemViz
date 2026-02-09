Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Write-Host "== ChemViz setup =="

if (-not (Test-Path "backend\.venv")) {
  Write-Host "Creating virtual environment..."
  python -m venv backend\.venv
}

Write-Host "Installing Python dependencies..."
& backend\.venv\Scripts\python -m pip install --upgrade pip
& backend\.venv\Scripts\python -m pip install -r requirements.txt

Write-Host "Running migrations..."
& backend\.venv\Scripts\python backend\manage.py migrate

Write-Host "Installing web dependencies..."
Push-Location web-frontend\chemviz-web
npm install
Pop-Location

Write-Host "Setup complete."
