Write-Host "Installing dependencies with Poetry..."
poetry install

Write-Host "Starting the application with Uvicorn..."
poetry run uvicorn app.main:app --reload
