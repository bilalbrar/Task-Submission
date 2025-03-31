import pytest
import logging
from app.core.logging import logger, setup_logging
import os
from pathlib import Path

@pytest.fixture(autouse=True)
def setup_test_logger(tmp_path):
    """Setup a fresh logger for each test."""
    # Create temporary log file
    log_file = tmp_path / "test.log"
    
    # Store original handlers and log file
    original_handlers = logger.handlers.copy()
    original_log_file = logger.handlers[0].baseFilename if logger.handlers else None
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Setup fresh logger with temporary file
    test_logger = setup_logging()
    file_handler = logging.FileHandler(log_file)
    console_handler = logging.StreamHandler()
    test_logger.addHandler(file_handler)
    test_logger.addHandler(console_handler)
    
    yield test_logger
    
    # Cleanup
    logger.handlers.clear()
    for handler in original_handlers:
        logger.addHandler(handler)

def test_logger_configuration(caplog, setup_test_logger):
    """Test logger functionality and configuration."""
    test_logger = setup_test_logger
    
    # Test log level
    assert test_logger.getEffectiveLevel() == logging.INFO
    
    # Verify handlers
    assert len(test_logger.handlers) == 2
    assert any(isinstance(h, logging.FileHandler) for h in test_logger.handlers)
    assert any(isinstance(h, logging.StreamHandler) for h in test_logger.handlers)
    
    # Test actual logging
    with caplog.at_level(logging.INFO):
        test_logger.info("Test message")
        assert "Test message" in caplog.text
        
    # Test formatting
    for record in caplog.records:
        assert all(field in record.__dict__ for field in ['name', 'levelname', 'message'])
