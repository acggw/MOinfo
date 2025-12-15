import pytest
from unittest.mock import patch, MagicMock
import sys

import kafka_server.restart as kafka_pod_setup  # replace with your module name

# -------------------------------
# 1️ Test cleanup when pod exists
# -------------------------------
def test_cleanup_old_pod_exists():
    # Mock subprocess.run to simulate pod exists
    mock_run = MagicMock()
    mock_run.return_value.returncode = 0  # pod exists

    with patch("subprocess.run", mock_run):
        with patch.object(kafka_pod_setup, "run_command") as mock_run_command:
            kafka_pod_setup.cleanup_old_pod()

            # Should call podman pod rm -f
            mock_run_command.assert_any_call(["podman", "pod", "rm", "-f", kafka_pod_setup.POD_NAME])
            # Should prune containers
            mock_run_command.assert_any_call(["podman", "container", "prune", "-f"])

# -------------------------------
# 2️ Test cleanup when pod does not exist
# -------------------------------
def test_cleanup_old_pod_not_exists():
    mock_run = MagicMock()
    mock_run.return_value.returncode = 1  # pod does NOT exist

    with patch("subprocess.run", mock_run):
        with patch.object(kafka_pod_setup, "run_command") as mock_run_command:
            kafka_pod_setup.cleanup_old_pod()

            # Should NOT call podman pod rm -f
            for call in mock_run_command.call_args_list:
                assert ["podman", "pod", "rm", "-f", kafka_pod_setup.POD_NAME] not in call[0]
            # Should prune containers
            mock_run_command.assert_any_call(["podman", "container", "prune", "-f"])

# -------------------------------
# 3️ Test start_kafka_pod with missing compose file
# -------------------------------
def test_start_kafka_missing_file():
    with patch("os.path.exists", return_value=False):
        with pytest.raises(SystemExit) as e:
            kafka_pod_setup.start_kafka_pod()
        assert e.type == SystemExit
        assert e.value.code == 1

# -------------------------------
# 4️ Test start_kafka_pod normal execution
# -------------------------------
def test_start_kafka_pod_success():
    with patch("os.path.exists", return_value=True):
        with patch.object(kafka_pod_setup, "run_command") as mock_run_command:
            with patch("time.sleep") as mock_sleep:
                kafka_pod_setup.start_kafka_pod()

                # run_command should be called with podman-compose up and podman ps
                mock_run_command.assert_any_call(["podman-compose", "-f", kafka_pod_setup.COMPOSE_FILE, "up", "-d"])
                mock_run_command.assert_any_call(["podman", "ps"])
                # time.sleep should be called
                mock_sleep.assert_called_once_with(10)

# -------------------------------
# 5️ Test run_command prints and calls subprocess.run
# -------------------------------
def test_run_command_calls_subprocess():
    mock_run = MagicMock()
    with patch("subprocess.run", mock_run):
        cmd = ["echo", "hello"]
        kafka_pod_setup.run_command(cmd)
        mock_run.assert_called_once_with(cmd, check=True)
