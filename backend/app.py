import os
import sys
import json
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
import mlflow
import mlflow.sklearn
import uvicorn
from contextlib import asynccontextmanager

from exception.exception import NetworkSecurityException
import logging
from utils.main_utils import load_object

# Define paths for model and preprocessor
MODEL_PATH = os.path.join("artifact", "model_trainer", "model", "model.pkl")

# Find the latest model artifact directory
def find_latest_model():
    artifact_dir = "artifact"
    if not os.path.exists(artifact_dir):
        return MODEL_PATH
    
    # Get all timestamp directories
    timestamp_dirs = [d for d in os.listdir(artifact_dir) 
                     if os.path.isdir(os.path.join(artifact_dir, d)) and 
                     d[0].isdigit()]
    
    if not timestamp_dirs:
        return MODEL_PATH
    
    # Sort by timestamp (newest first)
    timestamp_dirs.sort(reverse=True)
    
    # Find the first directory that contains a model
    for ts_dir in timestamp_dirs:
        model_path = os.path.join(artifact_dir, ts_dir, "model_trainer", "trained_model", "model.pkl")
        if os.path.exists(model_path):
            return model_path
    
    return MODEL_PATH

# Use the latest model
LATEST_MODEL_PATH = find_latest_model()

# Define lifespan to load model on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load model on startup
    try:
        app.state.model = load_object(LATEST_MODEL_PATH)
        logging.info(f"Model loaded from {LATEST_MODEL_PATH}")
        logging.info("Model loaded successfully")
    except Exception as e:
        logging.error(f"Error loading model: {e}")
        app.state.model = None
    yield
    # Cleanup on shutdown
    app.state.model = None

# Initialize FastAPI app
app = FastAPI(
    title="Network Security Classification API",
    description="API for classifying network security threats",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware (configure allowed origins via env var)
# Note: when allow_credentials=True, wildcard origins are not allowed by browsers
origins = os.getenv("FRONTEND_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in origins if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define input schema for text-based classification
class TextInput(BaseModel):
    text: str = Field(..., description="Text to classify for security threats")

# Define input schema for feature-based classification (keeping for backward compatibility)
class NetworkFeatures(BaseModel):
    features: List[List[float]] = Field(..., description="List of feature vectors to classify")
    feature_names: Optional[List[str]] = Field(None, description="Names of features in the same order as the feature vectors")

# Define output schema
class PredictionResponse(BaseModel):
    predictions: List[int] = Field(..., description="Predicted class labels")
    prediction_probabilities: Optional[List[Dict[str, float]]] = Field(None, description="Prediction probabilities for each class")
    
# Error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": f"An error occurred: {str(exc)}"}
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    if app.state.model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "healthy", "model_loaded": True}

# Text-based prediction endpoint
@app.post("/predict/text", response_model=PredictionResponse)
async def predict_text(request: TextInput):
    if app.state.model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Process the text to extract features
        text = request.text.lower()
        
        # Extract the same features we used during training
        features = [
            # Text length (normalized)
            min(len(request.text) / 5000.0, 1.0),
            
            # Word count (normalized)
            min(len(request.text.split()) / 500.0, 1.0),
            
            # Keyword-based features
            0.7 if 'malware' in text else 0.0,
            0.6 if 'trojan' in text else 0.0,
            0.6 if 'virus' in text else 0.0,
            0.8 if 'ransomware' in text else 0.0,
            0.4 if 'attack' in text else 0.0,
            0.3 if 'threat' in text else 0.0,
            0.5 if 'vulnerability' in text else 0.0,
            0.5 if 'exploit' in text else 0.0,
            0.2 if 'security' in text else 0.0,
        ]
        
        # Convert to numpy array and reshape for prediction
        features_array = np.array([features])
        
        # Make predictions
        predictions = app.state.model.predict(features_array)
        
        # Get prediction probabilities if available
        prediction_probs = None
        if hasattr(app.state.model, "predict_proba"):
            probs = app.state.model.predict_proba(features_array)
            prediction_probs = []
            for prob in probs:
                prob_dict = {str(i): float(p) for i, p in enumerate(prob)}
                prediction_probs.append(prob_dict)
        
        # Return predictions with interpretation
        result = {
            "predictions": predictions.tolist(),
            "prediction_probabilities": prediction_probs,
            "interpretation": "Malware detected" if predictions[0] == 1 else "No malware detected"
        }
        
        return result
    
    except Exception as e:
        logging.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

# Original feature-based prediction endpoint (keeping for backward compatibility)
@app.post("/predict", response_model=PredictionResponse)
async def predict(request: NetworkFeatures):
    if app.state.model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Convert input to numpy array
        features = np.array(request.features)
        
        # Make predictions
        predictions = app.state.model.predict(features)
        
        # Get prediction probabilities if available
        prediction_probs = None
        if hasattr(app.state.model, "predict_proba"):
            probs = app.state.model.predict_proba(features)
            prediction_probs = []
            for prob in probs:
                prob_dict = {str(i): float(p) for i, p in enumerate(prob)}
                prediction_probs.append(prob_dict)
        
        # Return predictions
        return {
            "predictions": predictions.tolist(),
            "prediction_probabilities": prediction_probs
        }
    
    except Exception as e:
        logging.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

# MLflow integration endpoint
@app.get("/model-info")
async def model_info():
    try:
        # Try to get model info from MLflow if available
        try:
            mlflow.set_tracking_uri("https://dagshub.com/austinLorenzMccoy/networkSecurity_project.mlflow")
            model_info = mlflow.search_registered_models(filter_string="name='NetworkSecurityModel'")
            
            if model_info and len(model_info) > 0:
                latest_version = model_info[0].latest_versions[0]
                return {
                    "model_name": "NetworkSecurityModel",
                    "version": latest_version.version,
                    "status": latest_version.status,
                    "creation_timestamp": latest_version.creation_timestamp,
                    "last_updated_timestamp": latest_version.last_updated_timestamp,
                    "metrics": {
                        "accuracy": latest_version.run.data.metrics.get("test_accuracy", None),
                        "f1_score": latest_version.run.data.metrics.get("test_f1", None)
                    }
                }
        except Exception as mlflow_error:
            logging.warning(f"MLflow connection error: {mlflow_error}")
            # If MLflow connection fails, try to get metrics from local file
            try:
                with open("reports/metrics.json", "r") as f:
                    metrics = json.load(f)
                return {
                    "model_name": "NetworkSecurityModel (Local)",
                    "version": "1.0.0",
                    "status": "READY",
                    "metrics": metrics
                }
            except Exception as file_error:
                logging.warning(f"Local metrics file error: {file_error}")
                return {"message": "No model information available from MLflow or local files"}
    
    except Exception as e:
        logging.error(f"Error getting model info: {e}")
        return {"message": f"Error getting model info: {str(e)}"}

# Run the app
if __name__ == "__main__":
    try:
        uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
