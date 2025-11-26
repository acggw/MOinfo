from sqlalchemy import String, ForeignKey, ForeignKeyConstraint, select, func
from sqlalchemy.orm import mapped_column, relationship
from .base import Base

def get_person(session, id):
    bill = session.get(Person, (id))
    return bill

def get_person_by_name(session, name, chamber, under):
    stmt = select(Person).where(Person.name == name)
    results = session.scalars(stmt).all()
    if(len(results == 1)):
        return results[0]
    elif(len(results) > 1):
        canidates = []
        for person in results:
            for office in person.offices:
                #TODO also check that they currently hold this position
                if(office.government == chamber and office.under == under):
                    canidates.append(person)
        if(len(canidates) == 1):
            return canidates[0]
        else:
            #Hope against hope we don't end up here.
            #This should probably call some asynchornous function that waits for human resolution before continueing
            pass
    else:
        return None
        

def get_next_id(session):
    stmt = select(func.max(Person.id))
    max_id = session.scalar(stmt)

    return max_id

class Person(Base):
    __tablename__ = "people"

    id = mapped_column(String, primary_key=True)
    name = mapped_column(String)
    party = mapped_column(String(1))
    email = mapped_column(String)
    phone = mapped_column(String)

    offices = relationship("Held_Office", back_populates="person")

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