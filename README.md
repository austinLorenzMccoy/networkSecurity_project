# Network Security Classification Project

[![DVC](https://img.shields.io/badge/DVC-Data%20Version%20Control-945DD6?logo=dvc)](https://dvc.org/)
[![MLflow](https://img.shields.io/badge/MLflow-Platform%20for%20ML%20Lifecycle-0194E2?logo=mlflow)](https://mlflow.org/)
[![DAGsHub](https://img.shields.io/badge/DAGsHub-Hosted%20MLOps%20Platform-FF69B4)](https://dagshub.com/)

## 📋 Project Overview

This project implements a machine learning pipeline for network security classification, focusing on detecting and classifying network security threats. The pipeline is built with reproducibility, versioning, and tracking in mind, leveraging modern MLOps tools.

### 🔍 Key Features

- **End-to-End ML Pipeline**: Automated data ingestion, validation, transformation, and model training
- **Data Version Control**: Track and version datasets using DVC
- **Experiment Tracking**: Monitor model metrics and parameters with MLflow
- **Reproducibility**: Ensure consistent results across different environments
- **CI/CD Integration**: Automated testing and deployment workflows
- **Containerization**: Docker support for consistent deployment
- **REST API**: FastAPI-based API for real-time predictions
- **Text Classification**: Support for text-based cyber threat intelligence data
- **Multiple Training Approaches**: Support for both MongoDB-based and direct file-based training

## 🛠️ Technology Stack

- **Python**: Core programming language
- **MongoDB**: Database for storing network security data
- **Scikit-learn & XGBoost**: ML algorithms for classification
- **DVC**: Data version control
- **MLflow**: Experiment tracking and model registry
- **DAGsHub**: Collaborative MLOps platform
- **Docker**: Containerization
- **Pytest**: Testing framework
- **FastAPI**: High-performance API framework
- **Uvicorn**: ASGI server for FastAPI

## 🚀 Getting Started

### Prerequisites

- Python 3.8+ (Python 3.10 or 3.11 recommended for best compatibility)
- Git
- Docker (optional)
- MongoDB connection string
- DAGsHub account (for MLflow tracking)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/austinLorenzMccoy/networkSecurity_project.git
   cd networkSecurity_project
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

4. Set up environment variables:
   ```bash
   # Create a .env file with your MongoDB connection string and DAGsHub credentials
   cp .env.template .env
   # Edit the .env file with your credentials
   ```

5. Initialize DVC:
   ```bash
   dvc init
   ```

6. Connect to DAGsHub (optional):
   ```bash
   # Set up DAGsHub as a remote
   dvc remote add origin https://dagshub.com/austinLorenzMccoy/networkSecurity_project.dvc
   ```

## 📊 DVC Pipeline

The project uses DVC to define and run the ML pipeline stages:

```bash
# Run the entire pipeline
dvc repro

# Run a specific stage
dvc repro -s data_ingestion
dvc repro -s data_validation
dvc repro -s data_transformation
dvc repro -s model_training

# Run the direct training pipeline (using cyber threat intelligence data)
dvc repro -s direct_training

# View pipeline visualization
dvc dag
```

## 📈 MLflow Tracking

MLflow is used to track experiments, including parameters, metrics, and artifacts:

```bash
# Start the MLflow UI locally
mlflow ui

# Or view experiments on DAGsHub
# Visit: https://dagshub.com/austinLorenzMccoy/networkSecurity_project.mlflow
```

### DAGsHub Integration

To enable MLflow tracking with DAGsHub:

1. Set your DAGsHub credentials in the `.env` file:
   ```
   MLFLOW_TRACKING_USERNAME=your_dagshub_username
   MLFLOW_TRACKING_PASSWORD=your_dagshub_token
   ```

2. Run the training pipeline with MLflow tracking:
   ```bash
   dvc repro direct_training
   ```

3. View your experiments on DAGsHub's MLflow interface

## 🧪 Testing

The project includes unit tests using pytest:

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=networksecurity
```

## 🐳 Docker

Build and run the project using Docker:

```bash
# Build the Docker image
docker build -t network-security-project .

# Run the container
docker run -p 8000:8000 -e MONGODB_URI=your_mongodb_connection_string network-security-project
```

## 🌐 FastAPI Application

The project includes a FastAPI application for serving predictions:

```bash
# Run the FastAPI application
python app.py

# Or use the convenience script
bash run_api.sh
```

### API Endpoints

- **GET /health**: Check if the model is loaded and ready
- **GET /model-info**: Get information about the trained model
- **POST /predict**: Make predictions using feature vectors
- **POST /predict/text**: Make predictions using raw text input

### Example Usage

```bash
# Check health status
curl -X GET "http://localhost:8000/health"

# Get model information
curl -X GET "http://localhost:8000/model-info"

# Make a prediction with text
curl -X POST "http://localhost:8000/predict/text" \
  -H "Content-Type: application/json" \
  -d '{"text": "A new ransomware attack has been detected that encrypts files."}'
```

## 📁 Project Structure

```
.
├── .dvc/                  # DVC configuration
├── .dagshub/              # DAGsHub configuration
├── artifact/              # Generated artifacts from pipeline
│   └── direct_training/   # Artifacts from direct training approach
├── data_schema/           # Data schema definitions
├── logs/                  # Application logs
├── Network_Data/          # Raw data (tracked by DVC)
├── networksecurity/       # Main package
│   ├── components/        # Pipeline components
│   ├── constants/         # Constants and configurations
│   ├── entity/            # Data entities and models
│   ├── exception/         # Custom exceptions
│   ├── logging/           # Logging utilities
│   ├── pipeline/          # Pipeline orchestration
│   └── utils/             # Utility functions
├── notebooks/             # Jupyter notebooks for exploration
├── reports/               # Generated reports and metrics
├── tests/                 # Test cases
├── .env                   # Environment variables
├── .env.template          # Template for environment variables
├── .gitignore             # Git ignore file
├── app.py                 # FastAPI application
├── custom_model_trainer.py # Custom model trainer implementation
├── dvc.yaml               # DVC pipeline definition
├── Dockerfile             # Docker configuration
├── main.py                # Main entry point
├── pytest.ini             # Pytest configuration
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
├── run_api.sh             # Script to run the FastAPI application
├── setup.py               # Package setup file
└── train_with_components.py # Direct training script using components
```

## 🔄 CI/CD Integration

The project is set up with GitHub Actions for CI/CD:

- **Continuous Integration**: Automated testing on pull requests
- **Continuous Deployment**: Automatic model training and evaluation
- **DVC and MLflow Integration**: Track experiments and data versions

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Contributors

- Augustine Chibueze - [GitHub](https://github.com/austinLorenzMccoy)

## 🙏 Acknowledgements

- [DVC](https://dvc.org/) for data version control
- [MLflow](https://mlflow.org/) for experiment tracking
- [DAGsHub](https://dagshub.com/) for MLOps collaboration
