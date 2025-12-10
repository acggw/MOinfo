from database.session import engine
from database.tables import Base
from sqlalchemy.orm import Session
from sqlalchemy import select
from database.tables.government import Government
import os
from database.tables.government_names import govt_names
from database.tables.user import create_admin
from config.database import DATABASE_LOCATION

def create_database():
    print("Creating database and tables...")
    Base.metadata.create_all(engine)
    print("Done!")

def setup_united_states(session):
    us_gov = Government(
        name = govt_names.US_GOVERNMENT_NAME,
        under= govt_names.US_GOVERNMENT_NAME
    )
    session.add(us_gov)
    setup_missouri(session)

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
    file_path = DATABASE_LOCATION

    if os.path.exists(file_path):
        os.remove(file_path)
        print("File deleted.")
    else:
        print("File does not exist.")
    create_database()
    with Session(engine) as session:
        setup_united_states(session)
        create_admin(session, "lucas", "Br!singr^sf1re", "lucasjamesnavarro@gmail.com", "314-285-2963")

        session.commit()
