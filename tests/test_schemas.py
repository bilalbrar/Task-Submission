import pytest
from pydantic import ValidationError
from app.api.schemas import PredictionRequest, PredictionResponse

def test_prediction_request_valid():
    """Test PredictionRequest schema with valid data."""
    data = {"sentences": ["I love this!", "This is bad."]}
    request = PredictionRequest(**data)
    assert request.sentences == ["I love this!", "This is bad."]

def test_prediction_request_invalid():
    """Test PredictionRequest schema with invalid data."""
    data = {"sentences": "This is not a list"}
    with pytest.raises(ValidationError) as excinfo:
        PredictionRequest(**data)
    assert "list" in str(excinfo.value)

def test_prediction_response_valid():
    """Test PredictionResponse schema with valid data."""
    data = {"predictions": ["positive", "negative"], "processing_time_ms": 123.45}
    response = PredictionResponse(**data)
    assert response.predictions == ["positive", "negative"]
    assert response.processing_time_ms == 123.45

def test_prediction_response_invalid():
    """Test PredictionResponse schema with invalid data."""
    data = {"predictions": "not a list", "processing_time_ms": "not a float"}
    with pytest.raises(ValidationError) as excinfo:
        PredictionResponse(**data)
    error_str = str(excinfo.value)
    assert "list" in error_str
    assert "float" in error_str
