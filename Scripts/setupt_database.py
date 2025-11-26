from session import engine
from tables import Base
from sqlalchemy.orm import Session
from sqlalchemy import select
from tables.government import Government
import os
from tables.government_names import govt_names

def create_database():
    print("Creating database and tables...")
    Base.metadata.create_all(engine)
    print("Done!")

def setup_united_states():
    with Session(engine) as session:
        us_gov = Government(
            name = govt_names.US_GOVERNMENT_NAME,
            under= govt_names.US_GOVERNMENT_NAME
        )
        session.add(us_gov)
        setup_missouri(session)
        session.commit()

def setup_missouri(session):
    mo_gov = Government(
        name = govt_names.MO_GOVERNMENT_NAME,
        under = govt_names.US_GOVERNMENT_NAME
    )
    session.add(mo_gov)

    mo_gov = Government(
        name = govt_names.MO_UPPER_HOUSE_NAME,
        under = govt_names.MO_GOVERNMENT_NAME
    )
    session.add(mo_gov)

    mo_gov = Government(
        name = govt_names.MO_LOWER_HOUSE_NAME,
        under = govt_names.MO_GOVERNMENT_NAME
    )
    session.add(mo_gov)


if __name__ == "__main__":
    file_path = "database/database.db"

    if os.path.exists(file_path):
        os.remove(file_path)
        print("File deleted.")
    else:
        print("File does not exist.")
    create_database()
    setup_united_states()