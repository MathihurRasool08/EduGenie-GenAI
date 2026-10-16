$ErrorActionPreference = 'Stop'

Write-Host 'Creating virtual environment...'
python -m venv .venv

Write-Host 'Activating virtual environment...'
.\.venv\Scripts\python.exe -m pip install --upgrade pip

Write-Host 'Installing dependencies...'
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

if (-not (Test-Path '.env')) {
    Copy-Item '.env.example' '.env'
    Write-Host 'Created .env from .env.example. Add your GEMINI_API_KEY before starting the app.'
}

Write-Host ''
Write-Host 'Setup complete.'
Write-Host 'Start the app with: .\.venv\Scripts\python.exe -m uvicorn main:app --reload'
