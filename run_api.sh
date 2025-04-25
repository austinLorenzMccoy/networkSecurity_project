#!/bin/bash

# Make the script executable
chmod +x setup_dvc.sh

# Check if model exists
if [ ! -f "artifact/model_trainer/model/model.pkl" ]; then
    echo "Model not found. Running the pipeline first..."
    python main.py
fi

# Start the FastAPI application
echo "Starting the FastAPI application..."
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
