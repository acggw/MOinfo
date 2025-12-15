import pytest
from unittest.mock import patch, MagicMock
import sys

from kafka_server.start_kafka import start_kafka, COMPOSE_FILE

# -------------------------------
# 1️ Test missing compose file
# -------------------------------
def test_compose_file_missing(monkeypatch):
    # Mock os.path.exists to return False
    with patch("os.path.exists", return_value=False):
        # Expect SystemExit when file does not exist
        with pytest.raises(SystemExit) as e:
            start_kafka()
        assert e.type == SystemExit
        assert e.value.code == 1

# -------------------------------
# 2️ Test subprocess.run called correctly
# -------------------------------
def test_subprocess_run_called(monkeypatch):
    # Mock os.path.exists to return True
    with patch("os.path.exists", return_value=True):
        # Mock subprocess.run so it does not actually run commands
        mock_run = MagicMock()
        with patch("subprocess.run", mock_run):
            start_kafka()

            # Check that podman pull was called for zookeeper and kafka
            mock_run.assert_any_call(
                ["podman", "pull", "docker.io/confluentinc/cp-zookeeper:7.4.0"],
                check=True
            )
            mock_run.assert_any_call(
                ["podman", "pull", "docker.io/confluentinc/cp-kafka:7.4.0"],
                check=True
            )

            # Check that podman-compose up was called
            mock_run.assert_any_call(
                ["podman-compose", "-f", COMPOSE_FILE, "up", "-d"],
                check=True
            )

# -------------------------------
# 3️ Test subprocess.CalledProcessError handling
# -------------------------------
def test_subprocess_raises(monkeypatch):
    # Mock os.path.exists to return True
    with patch("os.path.exists", return_value=True):
        # Make subprocess.run raise CalledProcessError
        from subprocess import CalledProcessError

        def mock_run_fail(*args, **kwargs):
            raise CalledProcessError(returncode=1, cmd=args[0])

        with patch("subprocess.run", mock_run_fail):
            # Expect SystemExit due to failure
            with pytest.raises(SystemExit) as e:
                start_kafka()
            assert e.type == SystemExit
            assert e.value.code == 1
