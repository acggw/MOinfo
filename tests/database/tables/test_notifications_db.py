import pytest
from unittest.mock import MagicMock
from database.tables.notifications import Notification

# -------------------------------
# 1️ Test Notification instantiation
# -------------------------------
def test_notification_instantiation():
    notif = Notification(
        action_guid=1,
        username=42,
        importance=5,
        sent_by="admin"
    )

    assert notif.action_guid == 1
    assert notif.username == 42
    assert notif.importance == 5
    assert notif.sent_by == "admin"

# -------------------------------
# 2️ Test bill_action relationship assignment
# -------------------------------
def test_notification_bill_action_relationship():
    mock_bill_action = MagicMock()
    notif = Notification(action_guid=1, username=42)
    notif.bill_action = mock_bill_action

    assert notif.bill_action == mock_bill_action

# -------------------------------
# 3️ Test sent_to relationship assignment
# -------------------------------
def test_notification_sent_to_relationship():
    mock_user = MagicMock()
    notif = Notification(action_guid=1, username=42)
    notif.sent_to = mock_user

    assert notif.sent_to == mock_user
