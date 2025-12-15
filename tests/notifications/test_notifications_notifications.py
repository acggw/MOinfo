# tests/test_notification_listener.py
import pytest
from unittest.mock import MagicMock, patch

import json
import types

# Import the module you provided
import notifications.notifications as notif  # replace with actual module name

@pytest.fixture
def mock_session():
    session = MagicMock()
    return session

@pytest.fixture
def mock_producer():
    producer = MagicMock()
    return producer

def make_mock_bill_action():
    # Mock bill version
    mock_version = MagicMock()
    mock_version.bill_chamber = "House"
    mock_version.bill_id = "B123"
    mock_version.bill_session = "2025"
    mock_version.policy_areas = [types.SimpleNamespace(policy_area="Economics")]

    # Mock Bill_Action
    action = MagicMock()
    action.guid = 1
    action.description = "passed"
    action.bill.get_newest_version.return_value = mock_version
    return action

def make_mock_user():
    user = MagicMock()
    user.username = "testuser"
    user.email_notifications = True
    user.phone_notifications = True
    user.email = "test@example.com"
    user.phone = "1234567890"
    return user

def test_parse_bill_sends_notifications():
    session = MagicMock()
    producer = MagicMock()

    action = make_mock_bill_action()
    session.get.return_value = action

    user = make_mock_user()
    pref = MagicMock(user=user)
    session.execute.return_value.scalars.return_value.all.return_value = [pref]

    notif.parse_notifications(1, session, producer)

    assert producer.send.call_count == 2
    assert session.add.call_count == 2
    session.commit.assert_called_once()

    producer.send.assert_any_call(
        "email_notification_prepared",
        {
            "email": user.email,
            "subject": "House B123 - passed",
            "content": user.username + "\n\nB123 was passed in the House.Go to "
            + notif.FLASK_SERVER
            + "/bills/House/2025/B123 to learn more.\n\nThank you,\nMOinfo",
        },
    )
