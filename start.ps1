Write-Host "Activating virtual environment..."
. .\venv\Scripts\Activate.ps1

Write-Host "Installing dependencies..."
pip install -r requirements.txt

Write-Host "Starting the application..."
uvicorn app.main:app --reload
