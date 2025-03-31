import pytest
import pandas as pd
from tempfile import NamedTemporaryFile
from scripts.train_pipeline import preprocess_data, get_sentiment_label

def test_get_sentiment_label():
    """Test the sentiment label conversion function."""
    assert get_sentiment_label(1) == "negative"
    assert get_sentiment_label(2) == "negative"
    assert get_sentiment_label(3) == "neutral"
    assert get_sentiment_label(4) == "positive"
    assert get_sentiment_label(5) == "positive"

def test_preprocess_data():
    """Test the preprocess_data function."""
    sample_data = pd.DataFrame({
        "text": ["I loved this product!", "It was okay.", "Terrible experience."],
        "rating": [5, 3, 1]
    })
    with NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as temp_file:
        sample_data.to_json(temp_file.name, orient="records", lines=True)
        processed_data = preprocess_data(temp_file.name)
    assert not processed_data.empty
    assert "sentence" in processed_data.columns
    assert "label" in processed_data.columns