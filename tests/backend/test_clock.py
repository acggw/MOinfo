import json
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import backend.clock as clock

def test_get_formatted_date():
    fixed_time = datetime(2025, 7, 11)

    with patch("backend.clock.datetime") as mock_datetime:
        mock_datetime.now.return_value = fixed_time
        mock_datetime.strftime = datetime.strftime

        result = clock.get_formatted_date()

    assert result == "07/11/2025"

def test_get_formatted_time():
    fixed_time = datetime(2025, 7, 11, 15, 30)

    with patch("backend.clock.datetime") as mock_datetime:
        mock_datetime.now.return_value = fixed_time
        mock_datetime.strftime = datetime.strftime

        result = clock.get_formatted_time()

    assert result == "07/11/2025 15:30"

def test_get_last_pulled():
    assert clock.get_last_pulled() == "7/11/2025"

def test_start_application_sends_kafka_message():
    mock_producer = MagicMock()

    fixed_now = datetime(2025, 7, 11, 10, 0)
    target_time = fixed_now - timedelta(seconds=1)  # already reached

    with patch("backend.clock.KafkaProducer", return_value=mock_producer), \
         patch("backend.clock.datetime") as mock_datetime, \
         patch("backend.clock.time.sleep", side_effect=KeyboardInterrupt), \
         patch("backend.clock.get_formatted_date", return_value="07/11/2025"), \
         patch("backend.clock.get_last_pulled", return_value="7/11/2025"):

        mock_datetime.now.return_value = fixed_now
        mock_datetime.strftime = datetime.strftime

        try:
            clock.start_application(target_time)
        except KeyboardInterrupt:
            pass

        mock_producer.send.assert_called_once_with(
        "bill_information_stale",
        {"last_pulled": "7/11/2025"}
    )





