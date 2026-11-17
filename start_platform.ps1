# PowerShell Launcher for Disinformation Detection Platform
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "  Starting Disinformation Detection Platform" -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan

$root = $PSScriptRoot
Write-Host "[1/2] Starting Python FastAPI Backend on port 8000..." -ForegroundColor Green
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", "cd '$root\anti_campaign_detector'; .\venv\Scripts\python.exe main.py"

Write-Host "[2/2] Starting React Frontend Dashboard on port 3000..." -ForegroundColor Green
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", "cd '$root\my-dashboard'; node server.js"

Write-Host "`nBackend:  http://localhost:8000" -ForegroundColor Yellow
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Yellow
