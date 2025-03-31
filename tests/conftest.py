import os
import pytest
import pandas as pd
import joblib
import numpy as np
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from app.main import app
from app.services.model_service import ModelService
from app.services import singleton 

@pytest.fixture(autouse=True)
def init_dummy_model(request):
    """Pre-initialize the singleton with a dummy model for tests (skip for test_singleton.py)."""
    if "test_singleton.py" in request.fspath.basename:
        yield
    else:
        class DummyModel:
            def predict(self, sentences):
                return np.array(["positive"] * len(sentences))
        singleton._model = DummyModel()
        yield
        singleton._model = None

@pytest.fixture
def test_client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)

@pytest.fixture
def mock_model_service():
    """Mock the ModelService and set it in app.state."""
    mock_model = MagicMock()
    mock_model.predict.return_value = ["positive", "negative"]
    app.state.model_service = ModelService()
    app.state.model_service.model = mock_model
    return mock_model

@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    return pd.DataFrame({
        "sentence": [
            "I loved this product!",
            "It was okay, nothing special.",
            "Terrible experience, would not recommend."
        ],
        "label": ["positive", "neutral", "negative"]
    })

@pytest.fixture
def test_model_path(tmp_path):
    """Create a test model and return its path."""
    model_path = tmp_path / "test_model.pkl"
    
    # Create a simple model
    model = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', LogisticRegression(random_state=42))
    ])
    X = ["I love this", "I hate this", "It's okay"]
    y = ["positive", "negative", "neutral"]
    model.fit(X, y)
    joblib.dump(model, model_path)
    return str(model_path)