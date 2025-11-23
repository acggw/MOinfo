from kafka import KafkaProducer
from datetime import datetime, timedelta
import json
import time
import config

def get_formatted_date():
    now = datetime.now()
    return now.strftime("%m/%d/%Y")

def get_formatted_time():
    now = datetime.now()
    return now.strftime("%m/%d/%Y %H:%M")

def get_last_pulled():
    return "7/11/2025"

def start_application(target: datetime):
    producer = KafkaProducer(
    bootstrap_servers=config.KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")  # serialize Python dict -> JSON bytes
    )
    while True:
        if datetime.now() >= target:
            date = get_formatted_date()
            last_pulled = get_last_pulled()
            target = datetime.now() + timedelta(days=1)

            print("Getting New Updates for " + date)

            data = {
                "fetch_start": last_pulled,
                "fetch_end": date
            }

            producer.send("bill_information_stale", data)

            print("Next Updates on " + target.strftime("%m/%d/%Y %H:%M"))
        print(get_formatted_time())
        time.sleep(10)

start_application(datetime.now())