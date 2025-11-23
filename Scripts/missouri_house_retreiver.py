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
        #TODO Finish all fields
        #TODO Deal with multiple actions in a day
        action_data = {
            "chamber": "PLACEHOLDER",
            "session": "PLACEHOLDER",
            "number": "PLACEHOLDER",
            "id":bill_string,
            "short_title": title,
            "long_title": "PLACEHOLDER",
            "description": description,
            "last_action": last_action[ACTION],
            "last_action_guid": "PLACEHOLDER",
            "last_action_pub_date": "PLACEHOLDER",
            "last_action_activity_sequence": "PLACEHOLDER",
            "next_house_hearing": "PLACEHOLDER",
            "sponsor": "PLACEHOLDER",
            "bill_text": "PLACEHOLDER", #Bill text and bill summaries are pdfs 
            "bill_summary": "PLACEHOLDER",
            "link": bill[BILL_LINK].text,
            "subjects": ["PLACEHOLDER"] #Bills have some predefined Categories
        }
        #Send all relevant bill data to the action processor
        producer.send("bill_action_retreived", action_data)
    
    return Notifications

for msg in consumer:
    data = msg.value
    print("Getting Bills from Missouri House of Representatives...")
    #get_house_bills(data["fetch_start"], data["fetch_end"])
    print("Bills Fetched from Missouri House of Representatives...")

