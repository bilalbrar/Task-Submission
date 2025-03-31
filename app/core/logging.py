import os
import logging
import time
from pathlib import Path
from app.core.config import settings

# Ensure log directory exists
log_dir = Path(os.path.dirname(settings.LOG_FILE))
log_dir.mkdir(parents=True, exist_ok=True)

def setup_logging():
    """Configure logging for the application."""
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create file handler
    file_handler = logging.FileHandler(settings.LOG_FILE, mode='a', encoding='utf-8')
    file_handler.setFormatter(formatter)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(settings.LOG_LEVEL)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # Ensure logs are flushed to the file
    file_handler.flush()
    
    # Return configured logger
    return logging.getLogger("app")

# Create global logger instance
logger = setup_logging()

class LoggerMiddleware:
    """Middleware for logging request information."""
    async def __call__(self, request, call_next):
        # Log request details
        logger.info(f"Request: {request.method} {request.url.path}")
        
        # Measure middleware execution time
        start_time = time.time()
        response = await call_next(request)
        middleware_time_ms = (time.time() - start_time) * 1000
        logger.debug(f"[LoggerMiddleware] Time spent: {middleware_time_ms:.2f}ms")
        
        # Log response details
        logger.info(f"Response: {response.status_code}")
        
        return response