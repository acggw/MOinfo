from kafka import KafkaConsumer, KafkaProducer
import json
from notification_class import notification
from tables.bill_actions import Bill_Action
from tables.bills import Bill
import config
from session import engine
from sqlalchemy.orm import Session

consumer = KafkaConsumer(
    "bill_retreived",
    bootstrap_servers=config.KAFKA_SERVER,
    auto_offset_reset="earliest",
    group_id="bill_processor_1",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

producer = KafkaProducer(
    bootstrap_servers=config.KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")  # serialize Python dict -> JSON bytes
)


for msg in consumer:
    with Session(engine) as session:
        data = msg.value
        #If not in database add bill to database
        #create the bill action and add importance. 
        #Create a notification with the proper fields

        #producer.send("bill_processed", send_data)
