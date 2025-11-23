from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, relationship
from .base import Base

class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String, unique=True, nullable=False)

    posts = relationship("notification", back_populates="users")
