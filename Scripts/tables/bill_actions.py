from sqlalchemy import Integer, String, ForeignKeyConstraint
from sqlalchemy.orm import mapped_column, relationship
from .base import Base

class Bill_Action(Base):
    __tablename__ = "bill_actions"

    guid = mapped_column(Integer, primary_key=True)
    primary_link = mapped_column(String)
    description = mapped_column(String, nullable=False)

    secondary_links = relationship("bill_action_links", back_populates=True)

    bill_chamber = mapped_column(String)
    under = mapped_column(String)
    bill_session = mapped_column(Integer)
    bill_id = mapped_column(String)

    __table_args__ = (
        ForeignKeyConstraint(
            ['bill_chamber', 'under', 'bill_session', 'bill_id'],          # columns in Child
            ['bills.chamber', 'bills.under', 'bills.session', 'bills.id']  # columns in Parent
        ),
    )

    type = mapped_column(String)

    __mapper_args__ = {
        "polymorphic_on": type,          # base class will use this column to figure out subclass
        "polymorphic_identity": "bill_action",  # identifier for the base class itself
        "with_polymorphic": "*"          # include all subclasses when querying
    }
