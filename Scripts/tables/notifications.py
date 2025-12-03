from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from .base import Base

class Notification(Base):
    __tablename__ = "notifications"

    content = mapped_column(String, nullable=False)
    action_guid = mapped_column(Integer, ForeignKey("bill_actions.guid"), primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)

    bill_action = relationship("Bill_Action", back_populates="notifications")

    importance = mapped_column(Integer)

    sent_to = relationship("User", back_populates="notifications_sent")
