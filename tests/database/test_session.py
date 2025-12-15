import os
from unittest.mock import patch, MagicMock
import logging
import pytest

import database.session as database_setup

def test_db_folder_created():
    with patch("os.makedirs") as mock_makedirs:
        # Re-import the module to trigger folder creation
        import importlib
        importlib.reload(database_setup)

        mock_makedirs.assert_called_once_with(database_setup.DB_FOLDER, exist_ok=True)

def test_database_url():
    expected_url = f"sqlite:///{database_setup.DB_FOLDER}/database.db"
    assert database_setup.DATABASE_URL == expected_url

def test_engine_creation():
    from sqlalchemy import create_engine
    # Ensure the engine has the correct URL
    assert str(database_setup.engine.url) == database_setup.DATABASE_URL

def test_session_factory():
    Session = database_setup.Session
    # Check if Session is callable (can create sessions)
    assert callable(Session)

    # Mock engine to test session creation
    session_instance = Session()
    assert session_instance is not None

def test_logging_setup():
    logger = database_setup.logger

    # Logger name
    assert logger.name == "sqlalchemy.engine"

    # Level
    assert logger.level == logging.INFO

    # Handlers
    handlers = logger.handlers
    assert any(isinstance(h, logging.FileHandler) for h in handlers)
    # Check formatter format string
    for h in handlers:
        fmt = h.formatter._fmt
        assert "%(asctime)s - %(levelname)s - %(message)s" in fmt






