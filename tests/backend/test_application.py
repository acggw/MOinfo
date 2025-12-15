import pytest
from unittest.mock import MagicMock, patch

from backend.application import start_all, services, monitor_processes
import subprocess
import time

def test_start_all_starts_all_services():
    mock_process = MagicMock()

    with patch("subprocess.Popen", return_value=mock_process) as popen_mock:
        processes = start_all()

        # One process per service
        assert len(processes) == len(services)

        # subprocess.Popen called correctly for each service
        expected_calls = [
            (["python", service],)
            for service in services
        ]
        actual_calls = [call.args for call in popen_mock.call_args_list]

        assert actual_calls == expected_calls

def test_monitor_processes_restarts_crashed_process():
    crashed_process = MagicMock()
    crashed_process.poll.return_value = 1  # crashed

    new_process = MagicMock()

    processes = []

    processes.append(crashed_process)

    with patch("subprocess.Popen", return_value=new_process) as popen_mock, \
         patch("time.sleep", side_effect=KeyboardInterrupt):

        monitor_processes(processes)

        # Process should be replaced
        assert processes[0] is new_process

        popen_mock.assert_called_once_with(
            ["python", services[0]]
        )

def test_monitor_processes_terminates_on_keyboard_interrupt():
    p1 = MagicMock()
    p1.poll.return_value = None  # still running

    p2 = MagicMock()
    p2.poll.return_value = None

    processes = []

    processes.extend([p1, p2])

    with patch("time.sleep", side_effect=KeyboardInterrupt):
        monitor_processes(processes)

    p1.terminate.assert_called_once()
    p2.terminate.assert_called_once()



