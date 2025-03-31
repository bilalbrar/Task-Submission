import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings."""
    
    # API settings
    API_TITLE: str = "Sentiment Analysis API"
    API_VERSION: str = "1.0.0"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Model settings
    MODEL_PATH: str = os.getenv("MODEL_PATH", "models/sentiment_model.pkl")
    LATENCY_THRESHOLD_MS: float = float(os.getenv("LATENCY_THRESHOLD_MS", "300"))
    
    # Logging settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/app.log")
    
    # Data settings
    DATA_PATH: str = os.getenv("DATA_PATH", "data/Books_10k.jsonl")

# Create global settings object
settings = Settings()