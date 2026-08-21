# Setup Local Environment for Lung Cancer Detection App

Write-Host "Setting up Backend..." -ForegroundColor Cyan
cd backend
if (-not (Test-Path .venv)) {
    python -m venv .venv
}
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
cd ..

Write-Host "Setting up Frontend..." -ForegroundColor Cyan
cd frontend
npm install
cd ..

Write-Host "Setup Complete!" -ForegroundColor Green
