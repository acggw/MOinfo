from sqlalchemy import Integer, String, ForeignKeyConstraint
from sqlalchemy.orm import mapped_column, relationship
from .base import Base
from .government_names import govt_names

class Bill_Action(Base):
    __tablename__ = "bill_actions"

    guid = mapped_column(Integer, primary_key=True)
    #guid are composed of 8 identifying the governmental body and the rest for the bill itself
    #_ _ _ for country  _ _ for State           _ for Chamber
    #0 0 0 for USA      2 4 for Missouri        0 for the House 
    primary_link = mapped_column(String)
    description = mapped_column(String, nullable=False)

    secondary_links = relationship("Bill_Action_Link", back_populates="bill_action")

    bill_chamber = mapped_column(String, nullable=False)
    under = mapped_column(String, nullable=False)
    bill_session = mapped_column(String, nullable=False)
    bill_id = mapped_column(String, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ['bill_chamber', 'under', 'bill_session', 'bill_id'],          # columns in Child
            ['bills.chamber', 'bills.under', 'bills.session', 'bills.id']  # columns in Parent
        ),
    )

    bill = relationship("Bill", back_populates="actions")

    notifications = relationship("Notification", back_populates="bill_action")

    type = mapped_column(String)

    __mapper_args__ = {
        "polymorphic_on": type,          # base class will use this column to figure out subclass
        "polymorphic_identity": "bill_action",  # identifier for the base class itself
        "with_polymorphic": "*"          # include all subclasses when querying
    }
   
    def __str__(self):
        return self.bill_id + " " + self.description


def get_guid_prefix(name_1=govt_names.US_GOVERNMENT_NAME, 
                    name_2=govt_names.MO_GOVERNMENT_NAME, 
                    name_3=govt_names.MO_GOVERNMENT_NAME, 
                    name_4=govt_names.MO_LOWER_HOUSE_NAME):
    code = ""
    match name_1:
        case govt_names.US_GOVERNMENT_NAME:
            code += "001"
            match name_2:
                case govt_names.MO_GOVERNMENT_NAME:
                    code += "024"
                    match name_3:
                        case govt_names.MO_GOVERNMENT_NAME:
                            code += "001"
                            match name_4:
                                case govt_names.MO_UPPER_HOUSE_NAME:
                                    code += "001"
                                case govt_names.MO_LOWER_HOUSE_NAME:
                                    code += "002"
                                case _:
                                    code += "000"
                        case _ :
                            code += "000"
                case _ :
                    code += "000"
        case _ :
            code += "000"

    return int(code)
def get_action(session, guid):
    bill_action = session.get(Bill_Action, (guid))
    return bill_action

def print_actions(session):
    print("Printing Bill Actions")
    all_bill_actions = session.query(Bill_Action).all()

    for bill_action in all_bill_actions:
        print(bill_action)

