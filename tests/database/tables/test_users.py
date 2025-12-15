import pytest
from unittest.mock import MagicMock
from werkzeug.security import generate_password_hash, check_password_hash
from database.tables.user import (
    User, User_Preference,
    create_user, create_admin,
    verify_user, user_exists,
    set_preference, preference_exists,
    get_preference, get_preferences
)
from config.errors import Errors

# -------------------------------
# 1️ Test User instantiation
# -------------------------------
def test_user_instantiation():
    user = User(
        username="lucas",
        password_hash=generate_password_hash("password123"),
        email="lucas@example.com",
        email_notifications=1,
        phone="123-456-7890",
        phone_notifications=1,
        verified="N/A",
        admin="No"
    )

    assert user.username == "lucas"
    assert check_password_hash(user.password_hash, "password123")
    assert user.email == "lucas@example.com"
    assert user.email_notifications == 1
    assert user.phone == "123-456-7890"
    assert user.phone_notifications == 1
    assert user.verified == "N/A"
    assert user.admin == "No"

# -------------------------------
# 2️ Test create_user
# -------------------------------
def test_create_user_adds_user(monkeypatch):
    mock_session = MagicMock()
    mock_session.get.return_value = None
    mock_session.query.return_value.filter.return_value.first.return_value = None

    create_user(mock_session, "lucas", "password", "lucas@example.com", 1, "123", 1)

    assert mock_session.add.called
    assert mock_session.commit.called

# -------------------------------
# 3️ Test create_user duplicate username
# -------------------------------
def test_create_user_duplicate_username_raises():
    mock_session = MagicMock()
    mock_session.get.return_value = True

    with pytest.raises(type(Errors.DUPLICATE_USER_NAME_ERROR)):
        create_user(mock_session, "lucas", "password", "a@b.com", 1, "123", 1)

# -------------------------------
# 4️ Test verify_user
# -------------------------------
def test_verify_user_success():
    password_hash = generate_password_hash("password")
    user = User(username="lucas", password_hash=password_hash)
    mock_session = MagicMock()
    mock_session.get.return_value = user

    assert verify_user(mock_session, "lucas", "password") is True
    assert verify_user(mock_session, "lucas", "wrongpass") is None

# -------------------------------
# 5️ Test user_exists
# -------------------------------
def test_user_exists_true_false():
    mock_session = MagicMock()
    mock_session.get.return_value = User(username="lucas")
    assert user_exists(mock_session, "lucas") is True

    mock_session.get.return_value = None
    assert user_exists(mock_session, "lucas") is False

# -------------------------------
# 6️ Test set_preference adds new preference
# -------------------------------
def test_set_preference_adds_new_pref():
    mock_session = MagicMock()
    user = User(username="lucas")
    mock_session.get.side_effect = lambda cls, key: user if cls == User else None

    set_preference(mock_session, "lucas", "Economics", "interest_high")
    assert mock_session.add.called
    assert mock_session.commit.called

# -------------------------------
# 7️ Test preference_exists returns True/False
# -------------------------------
def test_preference_exists_returns():
    user = User(username="lucas")
    pref = User_Preference(username="lucas", policy_area="Economics", importance_threshold=3)
    mock_session = MagicMock()
    mock_session.get.side_effect = lambda cls, key: user if cls == User else pref

    assert preference_exists(mock_session, "lucas", "Economics") is True
    mock_session.get.side_effect = lambda cls, key: user if cls == User else None
    assert preference_exists(mock_session, "lucas", "Finance") is False

# -------------------------------
# 8️ Test get_preference returns preference
# -------------------------------
def test_get_preference_returns():
    pref = User_Preference(username="lucas", policy_area="Economics", importance_threshold=3)
    user = User(username="lucas")
    mock_session = MagicMock()
    mock_session.get.side_effect = lambda cls, key: user if cls == User else pref

    result = get_preference(mock_session, "lucas", "Economics")
    assert result == pref

# -------------------------------
# 9️ Test get_preferences returns list
# -------------------------------
def test_get_preferences_returns():
    user = User(username="lucas")
    pref1 = User_Preference(username="lucas", policy_area="Economics", importance_threshold=1)
    pref2 = User_Preference(username="lucas", policy_area="Finance", importance_threshold=2)
    user.preferences = [pref1, pref2]

    mock_session = MagicMock()
    mock_session.get.return_value = user

    result = get_preferences(mock_session, "lucas")
    assert result == [pref1, pref2]
