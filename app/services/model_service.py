from fastapi import Request
from typing import List
from app.core.logging import logger
from app.services.singleton import get_model

class ModelService:
    """Service for handling model predictions."""
    
    def __init__(self):
        """Initialize the model service using the singleton model."""
        self.model = get_model()

    def predict(self, sentences: List[str]) -> List[str]:
        """
        Predict sentiment for a list of sentences.
        
        Args:
            sentences: List of sentences to analyze.
        
        Returns:
            List of sentiment predictions.
        """
        # Return empty list immediately if no input
        if not sentences:
            return []
        try:
            predictions = self.model.predict(sentences)
            # If predictions is a numpy array convert it to list; if already a list, return as-is.
            if hasattr(predictions, "tolist"):
                return predictions.tolist()
            return predictions
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            raise RuntimeError(f"Prediction failed: {str(e)}")

def get_model_service(request: Request) -> ModelService:
    """Get the ModelService instance from app state."""
    return request.app.state.model_service