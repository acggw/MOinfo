from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from .base import Base
from .bill_actions import Bill_Action

class Vote(Bill_Action):
    __tablename__ = "votes"

    guid = mapped_column(Integer, ForeignKey("bill_actions.guid"), primary_key=True)

    result = mapped_column(String)

    yes = mapped_column(Integer)
    no = mapped_column(Integer)
    abstain = mapped_column(Integer)
    absent = mapped_column(Integer)

    __mapper_args__ = {
        "polymorphic_identity": "vote",  # identifier for the base class itself
    }

class Voted_In(Base):
    __tablename__ = "voted_in"

    guid = mapped_column(Integer, ForeignKey("votes.guid"), primary_key=True)
    id = mapped_column(String, ForeignKey("people.id"), primary_key=True)
    vote = mapped_column(String)
