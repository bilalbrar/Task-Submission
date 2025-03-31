from typing import List, Optional
from pydantic import BaseModel, Field

class PredictionRequest(BaseModel):
    sentences: List[str] = Field(
        ...,
        json_schema_extra={
            "examples": ["This product is good", "it is okay", "This book is terrible"]
        }
    )

class PredictionResponse(BaseModel):
    predictions: List[str]
    processing_time_ms: Optional[float] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "predictions": ["positive", "neutral", "negative"],
                "processing_time_ms": 42.5
            }
        }