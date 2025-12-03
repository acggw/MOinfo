from kafka import KafkaConsumer, KafkaProducer
import json
from notification_class import notification
import config

consumer = KafkaConsumer(
    "bill_version_retreived",
    bootstrap_servers=config.KAFKA_SERVER,
    auto_offset_reset="earliest",
    group_id="website_updates_1",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)
producer = KafkaProducer(
    bootstrap_servers=config.KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")  # serialize Python dict -> JSON bytes
)

for msg in consumer:
    #update the website
    #Website should include 
    '''
        bill.chamber
        bill.under
        bill.session
        bill.short_title
        bill.long_title
        
        bill.sponsors - sponsors are not yet implemented but have a spot for them

        for each Bill_Policy_Area
            policy_area.policy_area - these can be found in bill.version.policy_areas - note version is an element in the versions arrray

        bill.versions - have the newest at the top, will probably have a way to hide old versions in the future
        for each version
            bill_version.version
            bill_version.version_string
            bill_version.summary
            bill_version.text

        Also we are going to want a timeline of bill actions.
        These will be updated from a different script
        If you could create a method to create the website that can be called by that script that would be great
    '''
    pass
    

