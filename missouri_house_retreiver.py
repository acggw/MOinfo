from kafka import KafkaConsumer, KafkaProducer
import json
from xml_unpacker import get_xml_data
import requests
from notification_class import notification
import xml.etree.ElementTree as ET
import config

consumer = KafkaConsumer(
    "bill_information_stale",
    bootstrap_servers=config.KAFKA_SERVER,
    auto_offset_reset="earliest",
    group_id="missouri_house",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)
producer = KafkaProducer(
    bootstrap_servers=config.KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")  # serialize Python dict -> JSON bytes
    )

HOUSE_BILLS_LINK = "https://documents.house.mo.gov/xml/251-BillList.XML"

def get_house_bills(last_ran: str, current_time: str = "today") -> [notification]:
    UPDATED = 5
    BILL_LINK = 4
    ACTION = 1

    Notifications = []

    bills = get_xml_data(HOUSE_BILLS_LINK)
    for bill in bills:
        #if(bill[UPDATED].text.split(" ")[0])
        data = requests.get(bill[BILL_LINK].text)
        if(str(data) != "<Response [200]>"):
            #log
            print("Error fetching data from " + bill[BILL_LINK].text)
            print(str(data))
            continue
        #log
        print("Data fetched from " + bill[BILL_LINK].text)

        info = ET.fromstring(data.text)[0]
        last_action = info.find("LastAction").text.split(" - ")    
        titles = info.find("Title")
        title = titles.find("ShortTitle").text
        description = titles.find("LongTitle").text

        bill_string = info.find("CurrentBillString").text

        msg = "Update on Bill " + bill_string + " " + title + " - " + description + " - " + last_action[ACTION]
        Notifications.append(notification(msg))
    
    return Notifications

for msg in consumer:
    print("Getting Bills from Missouri House of Representatives...")
    get_house_bills(msg.fetch_start, msg.fetch_end)
    print("Bills Fetched from Missouri House of Representatives...")

