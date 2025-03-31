import pytest
from unittest.mock import patch, Mock
from app.services.singleton import load_model, get_model
import app.services.singleton as singleton

@patch("app.services.singleton.joblib.load")
def test_singleton_pattern(mock_joblib_load):
    """Test complete singleton pattern behavior."""
    # Setup mock model
    mock_model = Mock()
    mock_joblib_load.return_value = mock_model
    
    # First load should initialize
    model1 = load_model("test_path.pkl")
    assert model1 == mock_model
    mock_joblib_load.assert_called_once_with("test_path.pkl")
    
    # Subsequent loads should return same instance
    model2 = load_model("different_path.pkl")
    assert model2 == model1
    assert mock_joblib_load.call_count == 1  # Still only called once
    
    # get_model should return same instance
    assert get_model() == model1

def test_get_model_uninitialized():
    """Test get_model when the model is not initialized."""
    singleton._model = None
    with pytest.raises(RuntimeError, match="Model not initialized"):
        get_model()
