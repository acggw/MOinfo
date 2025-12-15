from kafka import KafkaConsumer, KafkaProducer
import json
import config.servers as config
from database.session import engine
from sqlalchemy.orm import Session
from database.tables.bill_actions import Bill_Action
from database.tables.user import User_Preference
from database.tables.notifications import Notification
from sqlalchemy import select
from config.servers import FLASK_SERVER

consumer = KafkaConsumer(
    "bill_action_retreived",
    bootstrap_servers=config.KAFKA_SERVER,
    auto_offset_reset="earliest",
    group_id="notification_handler_1",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)
kafka_producer = KafkaProducer(
    bootstrap_servers=config.KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")  # serialize Python dict -> JSON bytes
)

def parse_notifications(guid, session, producer):
    
        action = session.get(Bill_Action, (guid))
        if(action == None):
            print("No action found with guid "+ str(guid))
            return
        bill_version = action.bill.get_newest_version()
        policy_areas = []
        for policy_area in bill_version.policy_areas:
            policy_areas.append(policy_area.policy_area)

        smnt = (select(User_Preference)
                .where(User_Preference.policy_area.in_(policy_areas)))
        preferences = session.execute(smnt).scalars().all()

        users = set()
        for pref in preferences:
            users.add(pref.user)

        subject = bill_version.bill_chamber + " " + bill_version.bill_id + " - " + action.description

        bill_link = FLASK_SERVER + f"/bills/{bill_version.bill_chamber}/{bill_version.bill_session}/{bill_version.bill_id}"
        content = f"\n\n" \
        f"{bill_version.bill_id} was {action.description} in the {bill_version.bill_chamber}." \
        f"Go to {bill_link} to learn more.\n\n" \
        "Thank you,\n" \
        "MOinfo"

        for user in users:
            notification_base = {
                "action_guid" : action.guid,
                "username" : user.username,
                "bill_action" : action,
                "importance" : 1,
                "sent_to" : user,
            }
            #Content needs to have an actual message that can be send as a reasonable email
            if(user.email_notifications):
                producer.send("email_notification_prepared", {"email": user.email, "subject" : subject, "content": user.username + content})
                session.add(Notification(**notification_base, sent_by="email"))

            if(user.phone_notifications):
                producer.send("phone_notification_prepared", {"phone": user.phone, "content": user.username + content})
                session.add(Notification(**notification_base, sent_by="phone"))
        session.commit()

def listen():
    for msg in consumer:
        data = msg.value
        with Session(engine) as session:
            parse_notifications(data["guid"], session, kafka_producer)
        

def __main__():
    listen()