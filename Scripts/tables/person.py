from sqlalchemy import String, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import mapped_column, relationship
from .base import Base

class Person(Base):
    __tablename__ = "people"

    id = mapped_column(String, primary_key=True)
    name = mapped_column(String)
    party = mapped_column(String(1))
    email = mapped_column(String)
    phone = mapped_column(String)

'''
class Politician(Person):
    __tablename__ = "politicians"

    id = mapped_column(String, ForeignKey("people.id"), primary_key=True)

    office_name = mapped_column(String, primary_key=True)
    government = mapped_column(String, primary_key=True)
    under = mapped_column(String, primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ['office_name', 'government', 'under'],          # columns in Child
            ['offices.name', 'offices.name', 'offices.under']  # columns in Parent
        ),
    )
'''