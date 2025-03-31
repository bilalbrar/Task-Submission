import json
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)

def test_health_endpoint(test_client):
    """Test the health check endpoint."""
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_status_endpoint(test_client, mock_model_service):
    """Test the status endpoint."""
    response = test_client.get("/status")
    assert response.status_code == 200
    assert response.json() == {
        "model_loaded": True,
        "uvicorn_reload": False
    }

@patch("app.services.model_service.ModelService.predict")
def test_predict_endpoint(mock_predict, test_client, mock_model_service):
    """Test the prediction endpoint."""
    mock_predict.return_value = ["positive", "negative"]
    test_data = {"sentences": ["I love this product!", "This was a terrible experience."]}
    response = test_client.post("/api/v1/predict", json=test_data)
    assert response.status_code == 200
    assert response.json() == {
        "predictions": ["positive", "negative"],
        "processing_time_ms": response.json().get("processing_time_ms")  # Ensure processing_time_ms exists
    }