import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from notifications.emails import send_email

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "bill_id": [1, 2],
        "title": ["Bill A", "Bill B"]
    })

# -------------------------------
# 1️ Test email sends successfully without DataFrame
# -------------------------------
def test_send_email_success_no_df():
    with patch("notifications.emails.smtplib.SMTP_SSL") as mock_smtp:
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        result = send_email(
            email_address="test@example.com",
            bill_notification="Test message",
            sender_email="sender@example.com",
            sender_password="password"
        )

        assert result is True
        mock_server.login.assert_called_once_with("sender@example.com", "password")
        mock_server.send_message.assert_called_once()

# -------------------------------
# 2️ Test email sends successfully with DataFrame
# -------------------------------
def test_send_email_success_with_df(sample_df):
    with patch("notifications.emails.smtplib.SMTP_SSL") as mock_smtp:
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        result = send_email(
            email_address="test@example.com",
            bill_notification="Test message",
            sender_email="sender@example.com",
            sender_password="password",
            df=sample_df
        )

        assert result is True
        mock_server.login.assert_called_once_with("sender@example.com", "password")
        mock_server.send_message.assert_called_once()

# -------------------------------
# 3️ Test failure in sending email
# -------------------------------
def test_send_email_failure(monkeypatch):
    # Make SMTP_SSL raise an exception
    class FakeSMTP:
        def __enter__(self):
            raise Exception("Connection failed")
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

    monkeypatch.setattr("notifications.emails.smtplib.SMTP_SSL", lambda *args, **kwargs: FakeSMTP())

    result = send_email(
        email_address="test@example.com",
        bill_notification="Test message",
        sender_email="sender@example.com",
        sender_password="password"
    )
    assert result is False
