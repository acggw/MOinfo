import os
import pytest
from unittest.mock import patch, MagicMock, ANY
import database.setupt_database as db_init  # adjust import path if different
from database.tables.government_names import govt_names

def test_create_database_calls_create_all():
    mock_engine = MagicMock()

    with patch("database.setupt_database.engine", mock_engine), \
         patch("database.setupt_database.Base.metadata.create_all") as mock_create_all:

        db_init.create_database()

        mock_create_all.assert_called_once_with(mock_engine)

def test_setup_united_states_adds_govts():
    mock_session = MagicMock()

    db_init.setup_united_states(mock_session)

    # US government added
    mock_session.add.assert_any_call(ANY)
    # Missouri governments added (3)
    assert mock_session.add.call_count >= 4

    # Inspect the first added object (US)
    us_gov = mock_session.add.call_args_list[0][0][0]
    assert us_gov.name == govt_names.US_GOVERNMENT_NAME
    assert us_gov.under == govt_names.US_GOVERNMENT_NAME

    # Inspect a Missouri upper house
    mo_upper = mock_session.add.call_args_list[2][0][0]
    assert mo_upper.name == govt_names.MO_UPPER_HOUSE_NAME
    assert mo_upper.under == govt_names.MO_GOVERNMENT_NAME

def test_setup_missouri_adds_three_govts():
    mock_session = MagicMock()
    db_init.setup_missouri(mock_session)

    # Should add exactly 3 government entries
    assert mock_session.add.call_count == 3

    names = [call[0][0].name for call in mock_session.add.call_args_list]
    assert govt_names.MO_GOVERNMENT_NAME in names
    assert govt_names.MO_UPPER_HOUSE_NAME in names
    assert govt_names.MO_LOWER_HOUSE_NAME in names

def test_main_block_removes_existing_file_and_creates_db():
    mock_exists = MagicMock(return_value=True)
    mock_remove = MagicMock()
    mock_create_db = MagicMock()
    mock_session_class = MagicMock()
    mock_session_instance = MagicMock()
    mock_session_class.return_value.__enter__.return_value = mock_session_instance

    with patch("database.setupt_database.os.path.exists", mock_exists), \
         patch("database.setupt_database.os.remove", mock_remove), \
         patch("database.setupt_database.create_database", mock_create_db), \
         patch("database.setupt_database.Session", mock_session_class), \
         patch("database.setupt_database.setup_united_states") as mock_setup_us, \
         patch("database.setupt_database.create_admin") as mock_create_admin, \
         patch("database.setupt_database.create_user") as mock_create_user, \
         patch("database.setupt_database.set_preference") as mock_set_pref:

        db_init.main()

        # Assertions
        mock_exists.assert_called_once_with(db_init.DATABASE_LOCATION)
        mock_remove.assert_called_once_with(db_init.DATABASE_LOCATION)
        mock_create_db.assert_called_once()
        mock_setup_us.assert_called_once_with(mock_session_instance)
        mock_create_admin.assert_called_once_with(mock_session_instance, "lucas", "Br!singr^sf1re", "", "")
        mock_create_user.assert_called_once()
        mock_set_pref.assert_called_once()
        mock_session_instance.commit.assert_called_once()

