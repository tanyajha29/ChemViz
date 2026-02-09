Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Write-Host "== ChemViz run all =="

Start-Process powershell -ArgumentList "-NoExit", "-Command", "backend\.venv\Scripts\python backend\manage.py runserver"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd web-frontend\chemviz-web; npm run dev"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "backend\.venv\Scripts\python desktop-app\chemviz-desktop\main.py"

Write-Host "Started backend, web, and desktop."
