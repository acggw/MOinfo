from kafka_server import KafkaConsumer, KafkaProducer
import json
from utils.xml_unpacker import get_xml_data
import requests
from notification_class import notification
import xml.etree.ElementTree as ET
import config.servers as config
from database.session import engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from database.tables.bills import Bill, Sponsored_By, Bill_Version, get_bill, get_version
from database.tables.bill_actions import Bill_Action, get_action, get_guid_prefix
from database.tables.government_names import govt_names
from datetime import datetime
from database.tables.person import get_person_by_name
from utils.pdf_util import extract_from_pdf
from classification_models.classification_util import classify_bill

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

def get_house_bills(last_ran: str):
    bills = get_xml_data(HOUSE_BILLS_LINK)
    with Session(engine) as session:
        for bill in bills:
            #Check if bill exists in database
            bill_session = bill[SESSION_YEAR].text + "-" + bill[SESSION_CODE].text
            bill_id = extract_part(bill[BILL_LINK].text)

            data = fetch_bill_data(bill)

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
                    "session":bill_session,
                    "id":data.find("BillNumber").text,
                    "short_title":short_title,
                    "long_title":long_title,
                    "description":""
                    }

            bill_sql = update_bill(session, bill, **bill_fields)

            update_versions(session, data, bill_sql)

            update_actions(session, data.findall("Action"), bill_sql)

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
        #print(str(data))
    #log
    else:
        print("Data fetched from " + bill[BILL_LINK].text)
        return ET.fromstring(data.text)[0]

def update_bill(sql_session, bill, **fields):
    old_bill_info = get_bill(sql_session, fields["chamber"], fields["under"], fields["session"], fields["id"])
    if(old_bill_info == None):
        new_bill = Bill(**fields)

        sql_session.add(new_bill)
        sql_session.commit()

        return new_bill
        #print("Bill " + new_bill.id + " added to database")
        #print(get_bill(sql_session, govt_names.MO_GOVERNMENT_NAME, govt_names.MO_LOWER_HOUSE_NAME, fields["session"], fields["id"]))
    
    else:
        #print("Bill " + old_bill_info.id + " already exists")
        #this migt not be needed
        return old_bill_info
        #update bill
        #for key, value in fields.items():
        #    setattr(bill, key, value)

    return True

def update_actions(sql_session, actions, sql_bill):

    for action in actions:
        guid = int(str(get_guid_prefix(govt_names.US_GOVERNMENT_NAME, govt_names.MO_GOVERNMENT_NAME, govt_names.MO_GOVERNMENT_NAME, govt_names.MO_LOWER_HOUSE_NAME)) + str(action.find("Guid").text))

        old_action = get_action(sql_session, guid)

        #Need to handle adding links
        if(old_action == None):
            new_action = {
                "guid" : guid,
                "description" : action.find("Description").text,
                "bill_chamber" : sql_bill.chamber,
                "under" : sql_bill.under,
                "bill_session" : sql_bill.session,
                "bill_id" : sql_bill.id,
            }

            sql_session.add(Bill_Action(bill = sql_bill, **new_action))
            sql_session.commit()

            producer.send("bill_action_retreived", new_action)

    return True
        
def update_versions(sql_session, bill, bill_sql):
    texts = bill.findall("BillText")
    summaries = bill.findall("BillSummary")
    
    #assert len(texts) == len(summaries), "Not every text has a summary for a bill"

    indexed_summaries = []
    for summary in summaries:
        indexed_summaries.append((summary, summary.find("BillVersionSort").text))
    for text in texts:
        version = int(text.find("BillVersionSort").text)
        text_link = text.find("BillTextLink").text

        summary_link = None
        for s in summaries:
            if s[1] == version:
                summary_link = s[0].find("SummaryTextLink").text
        
        if(None != get_version(sql_session, govt_names.MO_LOWER_HOUSE_NAME, govt_names.MO_GOVERNMENT_NAME, bill_sql.session, bill_sql.id, version)):
            continue
        
        bill_version = {
            "bill_chamber" : bill_sql.chamber,
            "under" : bill_sql.under,
            "bill_session" : bill_sql.session,
            "bill_id" : bill_sql.id,
            "version" : version,
            "text" : extract_from_pdf(text_link),
            "text_link" : text_link,
            "summary" : extract_from_pdf(summary_link),
            "summary_link" : summary_link,
        }
        bv = Bill_Version(bill = bill_sql, **bill_version)
        sql_session.add(bv)
        classify_bill(sql_session, bv)
        sql_session.commit()
        producer.send("bill_version_retreived", bill_version)

    return True

for msg in consumer:
    data = msg.value
    print("Getting Bills from Missouri House of Representatives...")
    get_house_bills(data["last_pulled"])
    print("Bills Fetched from Missouri House of Representatives...")

