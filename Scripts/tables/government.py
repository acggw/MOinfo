from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from .base import Base

class Government(Base):
    __tablename__ = "governments"

    name = mapped_column(String, primary_key=True)
    under = mapped_column(String, ForeignKey("governments.name"), primary_key=True)

    