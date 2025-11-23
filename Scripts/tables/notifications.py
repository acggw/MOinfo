from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from .base import Base

class Notification(Base):
    __tablename__ = "Notifications"

    id = mapped_column(Integer, primary_key=True)
    content = mapped_column(String, nullable=False)
