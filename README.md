# ChemViz - Chemical Equipment Parameter Visualizer

ChemViz is a hybrid Web + Desktop application for uploading chemical equipment datasets, computing analytics, and visualizing results. It ships with a Django REST backend, a React + Chart.js web UI, and a PyQt5 + Matplotlib desktop app.

## Highlights
1. CSV upload with schema + data validation
2. Validation summary with row-level issues
3. Summary analytics and charts on web + desktop
4. History + audit details (rows, file size, uploader)
5. Last 5 uploads stored per user
6. Polished PDF report generation
7. Token-based authentication

## Architecture
CSV -> Django REST API -> Pandas analytics -> Web (React) + Desktop (PyQt5)

## Project Structure
```
ChemViz/
|-- backend/                # Django + DRF + Pandas
|-- web-frontend/           # React + Chart.js
|-- desktop-app/            # PyQt5 + Matplotlib
|-- sample_data/            # Sample CSVs
|-- scripts/                # Setup/run scripts
|-- requirements.txt        # Combined Python deps (backend + desktop)
`-- README.md
```
Backend docs:
```
backend/README.md
```

## Prerequisites
1. Python 3.11+ (recommended)
2. Node.js 18+ and npm
3. Git

## Quick Start
Windows PowerShell:
```powershell
scripts\setup.ps1
scripts\run-all.ps1
```

Git Bash / macOS / Linux:
```bash
bash scripts/setup.sh
bash scripts/run-all.sh
```

## Manual Setup
Backend (Django + DRF):
```powershell
python -m venv backend\.venv
backend\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python backend\manage.py migrate
python backend\manage.py runserver
```
Backend runs at:
```
http://127.0.0.1:8000
```

Web Frontend (React + Chart.js):
```powershell
cd web-frontend\chemviz-web
npm install
npm run dev
```
Frontend runs at:
```
http://localhost:5173
```

Optional API base URL (create `web-frontend/chemviz-web/.env`):
```
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Desktop App (PyQt5 + Matplotlib):
```powershell
cd desktop-app\chemviz-desktop
python main.py
```

## Build Desktop Executable (PyInstaller)
From `desktop-app/chemviz-desktop`:
```powershell
pyinstaller --noconsole --onefile --name ChemVizDesktop --add-data "assets;assets" main.py
```
Executable path:
```
desktop-app/chemviz-desktop/dist/ChemVizDesktop.exe
```

## Authentication
Login:
```
POST /api/auth/token/
{
  "username": "email_or_username",
  "password": "your_password"
}
```

Register:
```
POST /api/auth/register/
{
  "full_name": "Your Name",
  "email": "name@domain.com",
  "password": "StrongPass1",
  "confirm_password": "StrongPass1"
}
```

Use the token:
```
Authorization: Token <token>
```

## Key API Endpoints
1. POST /api/auth/register/
2. POST /api/auth/token/
3. POST /api/auth/logout/
4. GET /api/auth/me/
5. POST /api/upload/
6. GET /api/summary/
7. GET /api/history/
8. GET /api/datasets/latest/
9. GET /api/datasets/report/<id>/
10. GET /api/report/pdf/

## CSV Requirements
Required columns:
```
Equipment Name, Type, Flowrate, Pressure, Temperature
```

Validation rules:
1. File type: .csv
2. Max size: 5 MB
3. Max rows: 10,000
4. Flowrate >= 0
5. Pressure >= 0
6. Temperature between -50 and 500

Validation summary includes:
1. Total rows
2. Accepted rows
3. Rejected rows
4. Missing values per column
5. Invalid numeric values per column
6. Out-of-range counts per column
7. Row-level issues (line numbers)

Sample data:
```
sample_data/sample_equipment_data.csv
```

## Notes
1. Each user sees only their own uploads.
2. Only the latest 5 uploads are stored per user.

## Troubleshooting
1. ModuleNotFoundError: pandas
   Run: `python -m pip install -r requirements.txt`
2. 401 Unauthorized
   Ensure token is set and request headers include `Authorization: Token ...`
3. no such table: datasets_datasetupload
   Run: `python backend\manage.py migrate`
4. Frontend shows no data
   Upload a CSV first or verify auth token storage

## Screenshots
Web Login:
![Web Login](docs/web-login.png)

Web Dashboard:
![Web Dashboard](docs/web-Dashboard.png)

Web Upload:
![Web Upload](docs/web-upload.png)

Desktop Dashboard:
![Desktop Dashboard](docs/desktop-Dashboard.png)

Desktop Upload:
![Desktop Upload](docs/desktop-upload.png)

## Release
Desktop download link (GitHub Releases):
```
https://github.com/tanyajha29/ChemViz/releases/latest/download/ChemVizDesktop.exe
```

Release steps:
1. Build the exe with PyInstaller
2. Create a GitHub release tag (example: v1.0.0)
3. Upload `ChemVizDesktop.exe` as a release asset

## License
MIT (update if required)
