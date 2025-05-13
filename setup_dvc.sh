#!/bin/bash

# Initialize DVC if not already initialized
if [ ! -d ".dvc" ]; then
    echo "Initializing DVC..."
    dvc init
    git add .dvc/.gitignore .dvc/config
    git commit -m "Initialize DVC"
fi

# Create reports directory for metrics
mkdir -p reports

# Add data to DVC
echo "Adding data to DVC..."
dvc add Network_Data

# Set up remote storage (if DAGsHub credentials are available)
if [ ! -z "$DAGSHUB_TOKEN" ]; then
    echo "Setting up DAGsHub remote..."
    dvc remote add origin https://dagshub.com/austinLorenzMccoy/networkSecurity_project.dvc
    git add .dvc/config
    git commit -m "Configure DVC remote storage"
fi

# Create empty params file for DAGsHub
echo "{}" > reports/params.json

echo "DVC setup complete!"
echo "Run 'dvc repro' to execute the pipeline"
