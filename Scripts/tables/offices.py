from sqlalchemy import String, ForeignKeyConstraint, ForeignKey, Date
from sqlalchemy.orm import mapped_column
from .base import Base

class Office(Base):
    __tablename__ = "offices"

    name = mapped_column(String, primary_key=True)

    government = mapped_column(String, primary_key=True)
    under = mapped_column(String, primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ['government', 'under'],          # columns in Child
            ['governments.name', 'governments.under']  # columns in Parent
        ),
    )

class Held_Office(Base):
    __tablename__ = "held_office"

    office_name = mapped_column(String, primary_key=True)
    government = mapped_column(String, primary_key=True)
    under = mapped_column(String, primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ['office_name', 'government', 'under'],          # columns in Child
            ['offices.name', 'offices.name', 'offices.under']  # columns in Parent
        ),
    )

    person_id = mapped_column(String, ForeignKey("people.id"), primary_key=True)

    start = mapped_column(Date)
    end = mapped_column(Date)

    term_end = mapped_column(Date)

