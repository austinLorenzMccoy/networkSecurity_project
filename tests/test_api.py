import os
import sys
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(transport=app)

def test_health_endpoint():
    """Test the health endpoint of the API"""
    response = client.get("/health")
    # Since we don't have a model loaded, we expect a 503 Service Unavailable
    assert response.status_code == 503
    assert "Model not loaded" in response.json()["detail"]

def test_predict_endpoint_input_validation():
    """Test the predict endpoint input validation"""
    # Test with invalid input (missing required field)
    response = client.post("/predict", json={})
    assert response.status_code == 422  # Unprocessable Entity
    
    # Test with valid input structure but no model
    response = client.post("/predict", json={"features": [[1.0, 2.0, 3.0, 4.0]]})
    # Since we don't have a model loaded, we expect a 503 Service Unavailable
    assert response.status_code == 503
    assert "Model not loaded" in response.json()["detail"]

def test_model_info_endpoint():
    """Test the model-info endpoint"""
    response = client.get("/model-info")
    # Even without MLflow connection, this should return a valid response
    assert response.status_code == 200
    assert "message" in response.json()
