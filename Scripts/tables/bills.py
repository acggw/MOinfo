from sqlalchemy import Integer, String, Date, ForeignKeyConstraint, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from .base import Base

def get_bill(session, chamber, under, session_num, bill_id):
    bill = session.get(Bill, (chamber, under, session_num, bill_id))
    return bill

class Bill(Base):
    __tablename__ = "bills"

    chamber = mapped_column(String, primary_key=True)
    under = mapped_column(String, primary_key=True)
    __table_args__ = (
        ForeignKeyConstraint(
            ['chamber', 'under'],          # columns in Child
            ['governments.name', 'governments.under']  # columns in Parent
        ),
    )

    session = mapped_column(String, primary_key=True)
    id = mapped_column(String, primary_key=True)

    short_title = mapped_column(String)
    long_title = mapped_column(String)
    description = mapped_column(String)

    actions = relationship("Bill_Action", back_populates="bill")

    versions = relationship("Bill_Version", back_populates="bill")

    #sponsors = relationship("sponsors", back_populates="bill")

    #hearings = relationship("hearings", back_populates="bill")

    #tags = relationship("tags")

    last_updates = mapped_column(Date)

class Sponsored_By(Base):
    __tablename__ = "sponsored_by"
    bill_chamber = mapped_column(String, primary_key=True)
    chamber_under = mapped_column(String, primary_key=True)
    bill_session = mapped_column(String, primary_key=True)
    bill_id = mapped_column(String, primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ['bill_chamber', 'chamber_under', 'bill_session', 'bill_id'],          # columns in Child
            ['bills.chamber', 'bills.under', 'bills.session', 'bills.id']  # columns in Parent
        ),
    )

    type = mapped_column(String)

    id = mapped_column(String, ForeignKey("people.id"), primary_key=True)

class Bill_Version(Base):
    __tablename__ = "bill_versions"
    bill_chamber = mapped_column(String, primary_key=True)
    under = mapped_column(String, primary_key=True)
    bill_session = mapped_column(Integer, primary_key=True)
    bill_id = mapped_column(String, primary_key=True)
    version = mapped_column(Integer, primary_key=True)
    version_string = mapped_column(String)

    bill = relationship("Bill", back_populates="versions")

    __table_args__ = (
        ForeignKeyConstraint(
            ['bill_chamber', 'under', 'bill_session', 'bill_id'],          # columns in Child
            ['bills.chamber', 'bills.under', 'bills.session', 'bills.id']  # columns in Parent
        ),
    )

    text = mapped_column(String)
    text_link = mapped_column(String)
    summary = mapped_column(String)
    summary_link = mapped_column(String)

    links = relationship("Version_Link", back_populates="bill_version")



