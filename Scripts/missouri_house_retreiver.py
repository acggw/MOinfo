from kafka import KafkaConsumer, KafkaProducer
import json
from xml_unpacker import get_xml_data
import requests
from notification_class import notification
import xml.etree.ElementTree as ET
import config
from session import engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from tables.bills import Bill, Sponsored_By, Bill_Version, get_bill
from tables.bill_actions import Bill_Action, get_action, get_guid_prefix
from tables.government_names import govt_names
from datetime import datetime
from tables.person import get_person_by_name
from pdf_util import extract_from_pdf

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
UPDATED = 5
BILL_LINK = 4
SESSION_CODE = 3
SESSION_YEAR = 2
ACTION = 1

def extract_part(url: str) -> str:
    # Get the last segment after the final '/'
    filename = url.rsplit('/', 1)[-1]

    # Remove the extension
    name_without_ext = filename.replace('.xml', '')

    # Split on '-' and take the second part
    return name_without_ext.split('-', 1)[-1]

def get_house_bills(last_ran: str) -> [notification]:

    Notifications = []

    bills = get_xml_data(HOUSE_BILLS_LINK)
    with Session(engine) as session:
        for bill in bills:
            #Check if bill exists in database
            bill_session = bill[SESSION_YEAR].text + "-" + bill[SESSION_CODE].text
            bill_id = extract_part(bill[BILL_LINK].text)

            data = fetch_bill_data(bill)

            print(data)

            if(data == None):
                continue

            titles = data.find("Title")
            try:
                short_title = titles.find("ShortTitle").text
            except:
                print("Bill " + bill_id + " short title not found")
                short_title = ""

            try:
                long_title = titles.find("LongTitle").text
            except:
                print("Bill " + bill_id + " long title not found")
                long_title = ""
        

            bill_fields = {"chamber":govt_names.MO_LOWER_HOUSE_NAME,
                    "under":govt_names.MO_GOVERNMENT_NAME,
                    "session":bill[SESSION_YEAR].text + "-" + bill[SESSION_CODE].text,
                    "id":data.find("BillNumber").text,
                    "short_title":short_title,
                    "long_title":long_title,
                    "description":""
                    }

            update_bill(session, bill, bill_session, bill_id, **bill_fields)

            update_versions(session, bill, bill_session, bill_id)

            for action in data.findall("Action"):
                update_action(session, action, bill_session, bill_id)

            #Add Sponsors
            #add_sponsors(session, data, bill_id, bill_session)


def add_sponsors(session, data, bill_id, bill_session):
    sponsors = data.find("Sponsor")
    for sponsor in sponsors:
        Sponsored_By(
            bill_chamber=govt_names.MO_LOWER_HOUSE_NAME,
            chamber_under=govt_names.MO_GOVERNMENT_NAME,
            bill_session=bill_session,
            bill_id=bill_id,
            type=sponsor.find("SponsorType").text,
            id=get_person_by_name(session, sponsor.find("FullName").text, govt_names.MO_LOWER_HOUSE_NAME, govt_names.MO_GOVERNMENT_NAME)
        )

def fetch_bill_data(bill):
    data = requests.get(bill[BILL_LINK].text)
    if(str(data) != "<Response [200]>"):
        #log
        print("Error fetching data from " + bill[BILL_LINK].text)
        print(str(data))
    #log
    else:
        print("Data fetched from " + bill[BILL_LINK].text)
        return ET.fromstring(data.text)[0]

def update_bill(sql_session, bill, bill_session, bill_id, **fields):
    old_bill_info = get_bill(sql_session, govt_names.MO_GOVERNMENT_NAME, govt_names.MO_LOWER_HOUSE_NAME, bill_session, bill_id)

    if(old_bill_info == None):
        new_bill = Bill(**fields)

        sql_session.add(new_bill)
    
    else:
        #this migt not be needed
        pass
        #update bill
        #for key, value in fields.items():
        #    setattr(bill, key, value)

    return True

def update_action(sql_session, action, bill_session, bill_id):

    guid = int(str(get_guid_prefix(govt_names.US_GOVERNMENT_NAME, govt_names.MO_GOVERNMENT_NAME, govt_names.MO_GOVERNMENT_NAME, govt_names.MO_LOWER_HOUSE_NAME)) + str(action.find("Guid").text))

    old_action = get_action(sql_session, guid)

    #Need to handle adding links
    if(old_action == None):
        new_action = Bill_Action(
            guid = guid,
            description = action.find("Description").text,
            bill_chamber = govt_names.MO_LOWER_HOUSE_NAME,
            under = govt_names.MO_GOVERNMENT_NAME,
            bill_session = bill_session,
            bill_id = bill_id
        )
        sql_session.add(new_action)

    producer.send("bill_action_retreived", guid)

def update_versions(sql_session, bill, bill_session, bill_id):
    texts = bill.findall("BillText")
    summaries = bill.findall("BillSummary")
    
    assert len(texts) == len(summaries), "Not every text has a summary for a bill"

    for text in texts:
        version = text.find("BillVersionSort").text
        text_link = text.find("BillTextLink").text
        for summary in summaries:
            if(summary.find("BillVersionSort").text != version):
                continue 
            summary_link = summary.find("SummaryTextLink").text
            bill_version = Bill_Version(
                bill_chamber = govt_names.MO_LOWER_HOUSE_NAME,
                under = govt_names.MO_GOVERNMENT_NAME,
                bill_session = bill_session,
                bill_id = bill_id,
                version = version,
                text = extract_from_pdf(text_link),
                text_link = text_link,
                summary = extract_from_pdf(summary_link),
                summary_link = summary_link
            )
            sql_session.add(bill_version)
            producer.send("new_bill_version", {"bill_chamber" : govt_names.MO_LOWER_HOUSE_NAME,
                "under" : govt_names.MO_GOVERNMENT_NAME,
                "bill_session" : bill_session,
                "bill_id" : bill_id,
                "version" : version})
            
    '''
            #if(bill[UPDATED].text.split(" ")[0])
            

            info = ET.fromstring(data.text)[0]
            last_action = info.find("LastAction").text.split(" - ")    
            titles = info.find("Title")
            short_title = titles.find("ShortTitle").text
            long_title = titles.find("LongTitle").text
            description = titles.find("LongTitle").text

            bill_string = info.find("CurrentBillString").text

            msg = "Update on Bill " + bill_string + " " + short_title + " - " + description + " - " + last_action[ACTION]
            Notifications.append(notification(msg))
            #TODO Finish all fields
            #TODO Deal with multiple actions in a day
            action_data = {
                "chamber": "PLACEHOLDER",
                "session": "PLACEHOLDER",
                "number": "PLACEHOLDER",
                "id":bill_string,
                "short_title": short_title,
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

            bill_data = Bill(chamber="Missouri House of Representatives",
                        under="State of Missouri",
                        session=bill.find("SessionYear").text + "-" + bill.find("SessionCode").text,
                        id="bill_string",
                        short_title=short_title,
                        long_title=long_title,
                        description=description,
                        text="",
                        text_link=info.find("BillText").find("BillTextLink").text,
                        summary="",
                        summary_link=info.find("BillSummary").find("SummaryTextLink").text
                        )
            session.add(bill_data)
            session.commit()
            stmt = select(Bill)
            results = session.scalars(stmt).all()

            for result in results:
                print(bill.id)

        #Send all relevant bill data to the action processor
        
    
    return Notifications
'''

for msg in consumer:
    data = msg.value
    print("Getting Bills from Missouri House of Representatives...")
    print(data)
    get_house_bills(data["last_pulled"])
    print("Bills Fetched from Missouri House of Representatives...")

