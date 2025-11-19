from kafka import KafkaConsumer, KafkaProducer
import json
from notification_class import notification
import config

consumer = KafkaConsumer(
    "bill_processed",
    bootstrap_servers=config.KAFKA_SERVER,
    auto_offset_reset="earliest",
    group_id="website_updates_1",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)
producer = KafkaProducer(
    bootstrap_servers=config.KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")  # serialize Python dict -> JSON bytes
)

for msg in consumer:
    #update the website
    pass
    

