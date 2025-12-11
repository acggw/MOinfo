from kafka import KafkaConsumer, KafkaProducer
import json
import config.servers as config
from database.session import engine
from sqlalchemy.orm import Session
from database.tables.bill_actions import Bill_Action
from database.tables.user import User_Preference
from database.tables.notifications import Notification
from sqlalchemy import select

consumer = KafkaConsumer(
    "bill_action_retreived",
    bootstrap_servers=config.KAFKA_SERVER,
    auto_offset_reset="earliest",
    group_id="notification_handler_1",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)
producer = KafkaProducer(
    bootstrap_servers=config.KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")  # serialize Python dict -> JSON bytes
)

for msg in consumer:
    data = msg.value
    with Session(engine) as session:
        action = session.get(Bill_Action, (data["guid"]))
        if(action == None):
            print("No action found with guid "+ str(data["guid"]))
            break
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
                producer.send("email_notification_prepared", {"email": user.email, "content": "Something Happened"})
                session.add(Notification(**notification_base, sent_by="email"))

            if(user.phone_notifications):
                producer.send("phone_notification_prepared", {"phone": user.phone, "content": "Something Happened"})
                session.add(Notification(**notification_base, sent_by="phone"))
        session.commit()