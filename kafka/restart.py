import subprocess
import os
import sys
import time

# Path to your docker-compose / podman-compose YAML
COMPOSE_FILE = "docker-compose.yml"  # Adjust path if needed
POD_NAME = "pod_kafka"               # Pod name used by podman-compose

def run_command(cmd):
    """Run a shell command and raise error if it fails."""
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)

def cleanup_old_pod():
    """Remove old Kafka/Zookeeper pod and containers."""
    print("Cleaning up any existing Kafka pods/containers...")

    # Check if pod exists
    result = subprocess.run(["podman", "pod", "exists", POD_NAME])
    if result.returncode == 0:
        print(f"Pod '{POD_NAME}' exists. Removing...")
        run_command(["podman", "pod", "rm", "-f", POD_NAME])
    else:
        print(f"No existing pod named '{POD_NAME}' found.")

    # Optionally remove stopped containers (cleanup)
    run_command(["podman", "container", "prune", "-f"])

def start_kafka_pod():
    """Start Kafka and Zookeeper using podman-compose."""
    if not os.path.exists(COMPOSE_FILE):
        print(f"Error: {COMPOSE_FILE} not found.")
        sys.exit(1)

    print("Starting Kafka and Zookeeper pod...")
    run_command(["podman-compose", "-f", COMPOSE_FILE, "up", "-d"])

    print("Waiting a few seconds for services to initialize...")
    time.sleep(10)  # adjust if needed for slow systems

    print("Kafka and Zookeeper should now be running!")
    run_command(["podman", "ps"])

if __name__ == "__main__":
    cleanup_old_pod()
    start_kafka_pod()
