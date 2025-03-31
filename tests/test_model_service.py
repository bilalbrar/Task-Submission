import pytest
import numpy as np
from unittest.mock import MagicMock, patch
from app.services.model_service import ModelService
import app.services.singleton as singleton

@pytest.fixture(autouse=True)
def mock_singleton_load_model():
    """Mock the load_model function and initialize the singleton model."""
    with patch("app.services.singleton.load_model") as mock_load_model:
        mock_model = MagicMock()
        # Update mock to return single prediction for single input
        mock_model.predict.side_effect = lambda x: np.array(["positive"] * len(x))
        mock_load_model.return_value = mock_model
        singleton._model = mock_model
        yield mock_load_model
        singleton._model = None

def test_model_service_initialization():
    """Test ModelService initialization and configuration."""
    service = ModelService()
    
    # Verify model is initialized correctly
    assert service.model is not None
    assert hasattr(service.model, 'predict')
    
    # Test model service basic functionality
    test_input = ["Test sentence"]
    result = service.predict(test_input)
    assert isinstance(result, list)
    assert len(result) == len(test_input)  # Should match input length
    assert all(isinstance(pred, str) for pred in result)

def test_model_service_predict():
    """Test ModelService predict method."""
    service = ModelService()
    predictions = service.predict(["I love this!", "This is bad."])
    assert predictions == ["positive", "positive"]

def test_model_service_predict_error():
    """Test ModelService predict method with an error."""
    service = ModelService()
    service.model.predict.side_effect = Exception("Prediction error")
    with pytest.raises(RuntimeError, match="Prediction failed: Prediction error"):
        service.predict(["This will fail"])

def test_predict_empty_input(mock_model_service):
    """Test ModelService.predict with empty input."""
    service = ModelService()
    predictions = service.predict([])
    assert predictions == []

def test_predict_error_handling(mock_model_service):
    """Test ModelService.predict with an error."""
    service = ModelService()
    service.model.predict.side_effect = Exception("Test error")
    with pytest.raises(RuntimeError, match="Prediction failed: Test error"):
        service.predict(["This will fail"])
