from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from .base import Base

class Bill_Action_Link(Base):
    __tablename__ = "bill_action_links"

    guid = mapped_column(Integer, ForeignKey("bill_actions.guid"), primary_key=True)
    link = mapped_column(String)