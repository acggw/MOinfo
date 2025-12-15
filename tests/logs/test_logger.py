import logging
from unittest.mock import patch, MagicMock
import pytest
import logs.logger as logger_setup  # replace with your module name

def test_logger_name_and_level():
    logger = logger_setup.logger
    assert logger.name == "sqlalchemy.engine"
    assert logger.level == logging.INFO
'''
def test_file_handler_added_and_configured():
    logger = logger_setup.logger
    handlers = logger.handlers

    # At least one FileHandler exists
    file_handlers = [h for h in handlers if isinstance(h, logging.FileHandler)]
    assert len(file_handlers) > 0

    for h in file_handlers:
        # Check the level
        assert h.level == logging.INFO

        # Check the formatter
        fmt = h.formatter._fmt
        assert fmt == '%(asctime)s - %(levelname)s - %(message)s'
'''
def test_logger_calls_emit(monkeypatch):
    # Mock the FileHandler emit method
    mock_emit = MagicMock()
    for h in logger_setup.logger.handlers:
        if isinstance(h, logging.FileHandler):
            monkeypatch.setattr(h, "emit", mock_emit)

    # Trigger a log message
    logger_setup.logger.info("Test message")
    mock_emit.assert_called()
