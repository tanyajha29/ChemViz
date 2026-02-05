# ChemViz — Chemical Equipment Parameter Visualizer

ChemViz is a hybrid **Web + Desktop** application for uploading chemical equipment datasets, calculating analytics, and visualizing results.  
The project includes a Django REST backend, a React + Chart.js web frontend, and a PyQt5 + Matplotlib desktop app.

**Core Features**
1. CSV upload with schema validation
2. Summary analytics (count, averages, type distribution)
3. Chart visualizations (web + desktop)
4. Last 5 uploads stored per user
5. PDF report generation
6. Token-based authentication

---

**Project Structure**
```
ChemViz/
├── backend/                # Django + DRF + Pandas
├── web-frontend/           # React + Chart.js
├── desktop-app/            # PyQt5 + Matplotlib
├── sample_data/            # Sample CSVs
├── requirements.txt        # Combined Python deps (backend + desktop)
└── README.md
```

---

**Prerequisites**
1. Python 3.11+ (recommended)
2. Node.js 18+ and npm
3. Git

---

**Backend Setup (Django + DRF)**

1. Create and activate a virtual environment:
```powershell
python -m venv backend\.venv
backend\.venv\Scripts\Activate.ps1
```

2. Install dependencies:
```powershell
python -m pip install --upgrade pip
python -m pip install -r backend\requirements.txt
```

3. Run migrations:
```powershell
python backend\manage.py migrate
```

4. Create a superuser:
```powershell
python backend\manage.py createsuperuser
```

5. Start the backend:
```powershell
python backend\manage.py runserver
```

Backend runs at:
```
http://127.0.0.1:8000
```

---

**Web Frontend Setup (React + Chart.js)**

1. Install dependencies:
```powershell
cd web-frontend\chemviz-web
npm install
```

2. Start the dev server:
```powershell
npm run dev
```

Frontend runs at:
```
http://localhost:5173
```

Optional: set API base URL in `.env`:
```
VITE_API_BASE_URL=http://127.0.0.1:8000
```

---

**Desktop App Setup (PyQt5 + Matplotlib)**

1. Install desktop requirements:
```powershell
python -m pip install -r desktop-app\chemviz-desktop\requirements.txt
```

2. Run the app:
```powershell
cd desktop-app\chemviz-desktop
python main.py
```

---

**Authentication Flow**

1. Get a token:
```
POST /api/auth/token/
{
  "username": "your_user",
  "password": "your_pass"
}
```

2. Use token in requests:
```
Authorization: Token <token>
```

Web and desktop clients store and reuse the token automatically.

---

**Key API Endpoints**
1. `POST /api/auth/token/` → login
2. `POST /api/auth/register/` → register
3. `POST /api/datasets/upload/` → upload CSV
4. `GET /api/datasets/summaries/` → last 5 summaries (per user)
5. `GET /api/datasets/report/<id>/` → PDF report

---

**CSV Format (Required Columns)**
```
Equipment Name, Type, Flowrate, Pressure, Temperature
```

Sample file:
```
sample_data/sample_equipment_data.csv
```

---

**Running Both Frontend + Backend**

1. Start backend:
```powershell
python backend\manage.py runserver
```

2. Start frontend:
```powershell
cd web-frontend\chemviz-web
npm run dev
```

---

**Troubleshooting**

1. `ModuleNotFoundError: pandas`
   - Run: `python -m pip install -r backend\requirements.txt`

2. `401 Unauthorized`
   - You are not logged in or token is missing.

3. `no such table: datasets_datasetupload`
   - Run migrations: `python backend\manage.py migrate`

4. Frontend shows no data
   - Upload a CSV first or verify token is stored.

---

**Notes**
1. Each user sees **only their own uploads**.
2. Only the **latest 5 uploads** are stored per user.

---

**Submission Checklist**
1. Source code on GitHub
2. README with setup instructions
3. Demo video (2–3 minutes)
4. Optional deployment link

---

**License**
MIT (or update if required)
