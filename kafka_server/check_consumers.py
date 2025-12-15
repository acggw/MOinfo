from kafka_server.admin import KafkaAdminClient

admin_client = KafkaAdminClient(bootstrap_servers="localhost:9092")

# List all consumer groups
groups = admin_client.list_consumer_groups()
print(groups)
