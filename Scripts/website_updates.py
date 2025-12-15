from kafka_server import KafkaConsumer, KafkaProducer
import json
from notification_class import notification
import config.servers as config
from pathlib import Path
from sqlalchemy.orm import Session
from database.tables.bills import Bill_Version
from database.session import engine

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

def build_bill_page(bill, actions=None, output_dir="website/bills"):
    """
    Generates an HTML file for the given bill.
    """

    actions = actions or list(bill.actions)

    newest_version = bill.get_newest_version()
    policy_areas = [pa.policy_area for pa in newest_version.policy_areas]
    versions_sorted = sorted(bill.versions, key=lambda v: v.version, reverse=True)

    # Build HTML fragments
    policy_areas_html = "".join(f"<li>{pa}</li>" for pa in policy_areas) or "<li>None</li>"
    sponsors_html = "<li>(Sponsors not implemented)</li>"

    versions_html = ""
    for v in versions_sorted:
        summary = (v.summary or "").replace("<", "&lt;").replace(">", "&gt;")
        text = (v.text or "").replace("<", "&lt;").replace(">", "&gt;")
        versions_html += f"""
        <section class="bill-version">
            <h3>Version {v.version} – {v.version_string}</h3>
            <h4>Summary</h4>
            <p>{summary}</p>
            <h4>Full Text</h4>
            <pre>{text}</pre>
        </section>
        """

    # Build actions section
    actions_sorted = sorted(actions, key=lambda a: getattr(a, "date", None) or 0)
    if actions_sorted:
        actions_html = "".join(
            f"<li><strong>{a.date}</strong> – {getattr(a, 'description', str(a))}</li>"
            for a in actions_sorted
        )
    else:
        actions_html = "<li>No actions yet.</li>"

    # Final HTML
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{bill.short_title}</title>
</head>
<body>
    <h1>{bill.short_title}</h1>
    <h3>{bill.long_title or ""}</h3>

    <p><strong>Chamber:</strong> {bill.chamber}</p>
    <p><strong>Under:</strong> {bill.under}</p>
    <p><strong>Session:</strong> {bill.session}</p>

    <h2>Sponsors</h2>
    <ul>{sponsors_html}</ul>

    <h2>Policy Areas</h2>
    <ul>{policy_areas_html}</ul>

    <h2>Versions (Newest First)</h2>
    {versions_html}

    <h2>Timeline of Actions</h2>
    <ul>{actions_html}</ul>

</body>
</html>
"""

    # Write to file
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    filepath = Path(output_dir) / f"{bill.under}.html"
    filepath.write_text(html, encoding="utf-8")

    return str(filepath)

for msg in consumer:
    data = msg.value
    print("Received:", data)

    chamber = data["chamber"]
    under = data["under"]
    session_num = data["session"]
    bill_id = data["id"]
    version_num = data["version"]

    with Session(engine) as session:
        bill_version = session.get(
            Bill_Version,
            (chamber, under, session_num, bill_id, version_num)
        )

        if bill_version is None:
            print("Bill version not found:", data)
            continue

        bill = bill_version.bill

        # Build or update the bill's website page
        file_path = build_bill_page(bill)
        print(f"Website updated: {file_path}")

        producer.send(
            "website_updated",
            {
                "chamber": bill.chamber,
                "under": bill.under,
                "session": bill.session,
                "id": bill.id,
                "file": file_path
            }
        )
        producer.flush()
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
    

