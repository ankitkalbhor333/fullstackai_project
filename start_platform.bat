@echo off
echo ===================================================
echo   Starting Disinformation Detection Platform
echo ===================================================

echo [1/2] Starting Python FastAPI Backend on port 8000...
start "FastAPI Backend (Port 8000)" cmd /k "cd /d %~dp0anti_campaign_detector && .\venv\Scripts\python.exe main.py"

echo [2/2] Starting React Frontend Dashboard on port 3000...
start "React Dashboard (Port 3000)" cmd /k "cd /d %~dp0my-dashboard && node server.js"

echo ===================================================
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo ===================================================
pause
