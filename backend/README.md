# ChemViz Backend (Django + DRF)

This folder contains the Django REST API for ChemViz. It handles authentication, CSV uploads, analytics, and PDF report generation.

## Requirements
1. Python 3.11+
2. pip

## Setup
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r ..\requirements.txt
```

## Database
```powershell
python manage.py migrate
```

Optional superuser:
```powershell
python manage.py createsuperuser
```

## Run
```powershell
python manage.py runserver
```

Backend runs at:
```
http://127.0.0.1:8000
```

## Key Endpoints
1. POST `/api/auth/register/`
2. POST `/api/auth/token/`
3. POST `/api/auth/logout/`
4. GET `/api/auth/me/`
5. POST `/api/upload/`
6. GET `/api/summary/`
7. GET `/api/history/`
8. GET `/api/datasets/latest/`
9. GET `/api/report/pdf/`

## CSV Requirements
Required columns:
```
Equipment Name, Type, Flowrate, Pressure, Temperature
```

Validation rules:
1. File type: `.csv`
2. Max size: 5 MB
3. Max rows: 10,000
4. Flowrate >= 0
5. Pressure >= 0
6. Temperature between -50 and 500
