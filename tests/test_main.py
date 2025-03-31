import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)

def test_metrics_endpoint():
    """Test the Prometheus metrics endpoint."""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text

def test_startup_event():
    """Test the startup event."""
    assert hasattr(app.state, "model_service")
    assert app.state.model_service is not None
