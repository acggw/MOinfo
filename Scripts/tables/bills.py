from sqlalchemy import Integer, String, ForeignKeyConstraint, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from .base import Base

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

    session = mapped_column(Integer, primary_key=True)
    id = mapped_column(String, primary_key=True)

    short_title = mapped_column(String)
    long_title = mapped_column(String)
    description = mapped_column(String)

    actions = relationship("bill_actions", back_populates="bill")

    #sponsors = relationship("sponsors", back_populates="bill")

    #hearings = relationship("hearings", back_populates="bill")

    text = mapped_column(String)
    summary = mapped_column(String)

    tags = relationship("tags")

class Sponsored_By(Base):
    __tablename__ = "sponsored_by"
    bill_chamber = mapped_column(String, primary_key=True)
    chamber_under = mapped_column(String, primary_key=True)
    bill_session = mapped_column(Integer, primary_key=True)
    bill_id = mapped_column(String, primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ['bill_chamber', 'chamber_under', 'bill_session', 'bill_id'],          # columns in Child
            ['bills.chamber', 'bills.under', 'bills.session', 'bills.id']  # columns in Parent
        ),
    )

    type = mapped_column(String)

    id = mapped_column(String, ForeignKey("people.id"), primary_key=True)