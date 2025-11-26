from tables.bill_actions import print_actions
from tables.bills import print_bills
from tables.government import print_governments
from session import engine
from sqlalchemy.orm import Session

with Session(engine) as session:
    print_actions(session)
    print_bills(session)
    print_governments(session)

