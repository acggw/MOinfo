from kafka import KafkaConsumer, KafkaProducer
import json
from notification_class import notification
import config

consumer = KafkaConsumer(
    "bill_action_retreived",
    bootstrap_servers=config.KAFKA_SERVER,
    auto_offset_reset="earliest",
    group_id="missouri_senate",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

producer = KafkaProducer(
    bootstrap_servers=config.KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")  # serialize Python dict -> JSON bytes
)

for msg in consumer:
    data = msg.value
    bill_name = data["short_title"]
    #If not in database add bill to database
    #create the bill action and add importance. 
    #Create a notification with the proper fields
    print(bill_name + " processed")
    send_data = {
        "guid": data["last_action_guid"],
    }
    producer.send("bill_processed", send_data)