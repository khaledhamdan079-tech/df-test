# DF Test API (FastAPI)

A minimal FastAPI project scaffold with a health endpoint and environment-based configuration.

## Requirements
- Python 3.10+
- Windows PowerShell

## Setup (Windows)
1. Create and activate a virtual environment:
   ```powershell
   py -3 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. (Optional) Configure environment variables:
   - Create a file named `.env` in the project root with values like:
     ```
     PROJECT_NAME="DF Test API"
     VERSION="0.1.0"
     HOST="127.0.0.1"
     PORT=8000
     ```

## Run the server (local)
- Development (auto-reload):
  ```powershell
  uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
  ```

Open `http://127.0.0.1:8000/docs` for Swagger UI.

## Deploy to Railway
This repo includes `Procfile` and `railway.toml` for Nixpacks.

Steps:
1. Push this project to a GitHub repo.
2. In Railway, create a new project and deploy from your repo.
3. Railway provides `PORT` automatically. The app starts with:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port ${PORT}
   ```

## Project layout
```
app/
  api/
    v1/
      health.py
  core/
    config.py
  main.py
```

## Endpoints
- GET `/` → simple OK message
- GET `/api/v1/health` → service health status
