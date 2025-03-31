import joblib
from app.core.logging import logger

_model = None

def load_model(model_path: str):
    """
    Load model once and store in global singleton.
    
    Args:
        model_path: Path to the model file.
    """
    global _model
    if _model is None:
        logger.info(f"Loading model from {model_path}")
        _model = joblib.load(model_path)
        logger.info("Model loaded successfully")
    return _model

def get_model():
    """
    Get the singleton model instance.
    
    Returns:
        The loaded model instance.
    """
    global _model
    if _model is None:
        raise RuntimeError("Model not initialized")
    return _model
