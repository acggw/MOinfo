from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from .base import Base

class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String, unique=True, nullable=False)

    notifications_sent = relationship("Notification", back_populates="sent_to")

    preferences = relationship("User_Preference", back_populates="user")

class User_Preference(Base):
    __tablename__ = "user_preferences"

    user_id = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)
    policy_area = mapped_column(String, primary_key=True)
    importance_threshold = mapped_column(Integer)

    user = relationship("User", back_populates="preferences")

