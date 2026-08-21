# Run Lung Cancer Detection App Locally

Write-Host "Starting Backend and Frontend..." -ForegroundColor Cyan

# Start Backend in a new window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; .venv\Scripts\Activate.ps1; python app.py"

# Start Frontend in current window (or another window)
cd frontend
npm run dev
