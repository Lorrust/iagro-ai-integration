#!/bin/bash

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Starting the application..."
uvicorn app.main:app --reload
