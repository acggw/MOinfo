from database.tables.bill_actions import print_actions
from database.tables.bills import print_bills, print_policy_areas, print_versions
from database.tables.government import print_governments
from database.session import engine
from sqlalchemy.orm import Session

with Session(engine) as session:
    print_actions(session)
    print_bills(session)
    print_governments(session)
    print_versions(session)
    print_policy_areas(session)

