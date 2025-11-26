from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from .base import Base

class Government(Base):
    __tablename__ = "governments"

    name = mapped_column(String, primary_key=True)
    under = mapped_column(String, ForeignKey("governments.name"), primary_key=True)

def print_governments(session):
    print("Printing Governments")
    all_govts = session.query(Government).all()

    for govt in all_govts:
        print(govt.name + " -> " + govt.under)

    