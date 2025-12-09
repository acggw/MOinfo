from sqlalchemy import Integer, String, ForeignKey, Bool
from sqlalchemy.orm import mapped_column, relationship
from .base import Base

class User(Base):
    __tablename__ = "users"

    username = mapped_column(String, primary_key=True, nullable=False)
    password_hash = mapped_column(String)

    notifications_sent = relationship("Notification", back_populates="sent_to")

    preferences = relationship("User_Preference", back_populates="user")

    email = mapped_column(String, unique=True)

    phone = mapped_column(String, unique=True)

    verified = mapped_column(String)

class User_Preference(Base):
    __tablename__ = "user_preferences"

    user_id = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)
    policy_area = mapped_column(String, primary_key=True)
    importance_threshold = mapped_column(Integer)

    user = relationship("User", back_populates="preferences")




