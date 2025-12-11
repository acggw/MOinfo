from kafka import KafkaConsumer, KafkaProducer
import json
import requests
from notification_class import notification
from bs4 import BeautifulSoup
import config.config as config

consumer = KafkaConsumer(
    "bill_information_stale",
    bootstrap_servers=config.KAFKA_SERVER,
    auto_offset_reset="earliest",
    group_id="missouri_senate",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

producer = KafkaProducer(
    bootstrap_servers=config.KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")  # serialize Python dict -> JSON bytes
)

HOUSE_BILLS_LINK = "https://documents.house.mo.gov/xml/251-BillList.XML"

def get_senate_bills(datetime: str, current_time: str= "today") -> [notification]:
    LINK = "https://www.senate.mo.gov/25Info/BTS_Web/Daily.aspx?SessionType=R&ActionDate="

    data = requests.get(LINK + datetime).text
    soup = BeautifulSoup(data, "html.parser")
    bill_elements = soup.find_all("dl")

    bills = []
    for dl in bill_elements:
        text = " ".join(dl.get_text(separator=" ", strip=True).split())
        bills.append(notification(text))
        action_data = {
            "number": "PLACEHOLDER",
            "string":"PLACEHOLDER",
            "short_title": text,
            "long_title": "PLACEHOLDER",
            "description": "PLACEHOLDER",
            "last_action": "PLACEHOLDER",
            "last_action_guid": "PLACEHOLDER",
            "last_action_pub_date": "PLACEHOLDER",
            "last_action_activity_sequence": "PLACEHOLDER",
            "next_house_hearing": "PLACEHOLDER",
            "sponsor": "PLACEHOLDER",
            "bill_text": "PLACEHOLDER", #Bill text and bill summaries are pdfs 
            "bill_summary": "PLACEHOLDER",
            "link": "PLACEHOLDER",
            "subjects": ["PLACEHOLDER"] #Bills have some predefined Categories
        }
        #Send all relevant bill data to the action processor
        #producer.send("bill_action_retreived", action_data)
    return bills

for msg in consumer:
    data = msg.value
    print("Getting Bills from Missouri Senate...")
    #get_senate_bills(data["fetch_start"], data["fetch_end"])
    print("Bills Fetched from Missouri Senate...")

