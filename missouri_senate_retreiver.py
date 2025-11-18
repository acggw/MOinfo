from kafka import KafkaConsumer
import json
import requests
from notification_class import notification
from bs4 import BeautifulSoup
import config

consumer = KafkaConsumer(
    "bill_information_stale",
    bootstrap_servers=config.KAFKA_SERVER,
    auto_offset_reset="earliest",
    group_id="missouri_house",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
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

    return bills

for msg in consumer:
    print("Getting Bills from Missouri Senate...")
    get_senate_bills(msg.fetch_start, msg.fetch_end)
    print("Bills Fetched from Missouri Senate...")

