import subprocess
import os
import sys

# Path to your docker-compose / podman-compose YAML
COMPOSE_FILE = "docker-compose.yml"  # Adjust path if needed

def start_kafka():
    """
    Start Kafka and Zookeeper using podman-compose
    """
    if not os.path.exists(COMPOSE_FILE):
        print(f"Error: {COMPOSE_FILE} not found.")
        sys.exit(1)

    try:
        # Pull images
        print("Pulling images...")
        subprocess.run(["podman", "pull", "docker.io/confluentinc/cp-zookeeper:7.4.0"], check=True)
        subprocess.run(["podman", "pull", "docker.io/confluentinc/cp-kafka:7.4.0"], check=True)

        # Start services
        print("Starting Kafka and Zookeeper...")
        subprocess.run(["podman-compose", "-f", COMPOSE_FILE, "up", "-d"], check=True)

        print("Kafka and Zookeeper should now be running.")
        print("Use 'podman ps' to check running containers.")
        print("Kafka broker will be available at localhost:9092")

    except subprocess.CalledProcessError as e:
        print("Error starting Kafka:", e)
        sys.exit(1)


if __name__ == "__main__":
    start_kafka()
