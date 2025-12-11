from sqlalchemy import Integer, String, Date, ForeignKeyConstraint, ForeignKey, select
from sqlalchemy.orm import mapped_column, relationship
from .base import Base

def get_bill(session, chamber, under, session_num, bill_id):
    bill = session.get(Bill, (chamber, under, session_num, bill_id))
    return bill

def retreive_bill(session, chamber, session_num, bill_id):
    #should be replaced with a Get when under is eliminated
    smnt = (select(Bill)
            .where(Bill.chamber == chamber)
            .where(Bill.session == session_num)
            .where(Bill.id == bill_id))
    bill = session.execute(smnt).scalars().first()
    return bill

def get_version(session, chamber, under, session_num, bill_id, version):
    version = session.get(Bill_Version, (chamber, under, session_num, bill_id, version))
    return version

def update_bill(sql_session, **fields):
    assert "chamber" in fields
    assert "under" in fields
    assert "session" in fields
    assert "id" in fields
    old_bill_info = get_bill(sql_session, fields["chamber"], fields["under"], fields["session"], fields["id"])
    if(old_bill_info == None):
        new_bill = Bill(**fields)

        sql_session.add(new_bill)
        sql_session.commit()

        return new_bill
    else:
        return old_bill_info
    
def print_bills(session):
    print("Printing Bills")
    all_bills = session.query(Bill).all()

    for bill in all_bills:
        print(bill)
        for version in bill.versions:
            print(version)
            for area in version.policy_areas:
                print(area)

class Bill(Base):
    __tablename__ = "bills"

    chamber = mapped_column(String, primary_key=True)
    under = mapped_column(String, primary_key=True)
    __table_args__ = (
        ForeignKeyConstraint(
            ['chamber', 'under'],          # columns in Child
            ['governments.name', 'governments.under']  # columns in Parent
        ),
    )

    session = mapped_column(String, primary_key=True)
    id = mapped_column(String, primary_key=True)

    short_title = mapped_column(String)
    long_title = mapped_column(String)
    description = mapped_column(String)

    actions = relationship("Bill_Action", back_populates="bill")

    versions = relationship("Bill_Version", back_populates="bill")

    #sponsors = relationship("sponsors", back_populates="bill")

    #hearings = relationship("hearings", back_populates="bill")

    #tags = relationship("tags")

    last_updates = mapped_column(Date)

    def __str__(self):
        return self.id + " in the " + self.chamber + " under " + self.under + " - " + self.session +  " : " + self.short_title
    
    def get_newest_version(self):
        number = -1
        version = None
        for v in self.versions:
            if v.version > number:
                number = v.version
                version = v
        return version

class Sponsored_By(Base):
    __tablename__ = "sponsored_by"
    bill_chamber = mapped_column(String, primary_key=True)
    chamber_under = mapped_column(String, primary_key=True)
    bill_session = mapped_column(String, primary_key=True)
    bill_id = mapped_column(String, primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ['bill_chamber', 'chamber_under', 'bill_session', 'bill_id'],          # columns in Child
            ['bills.chamber', 'bills.under', 'bills.session', 'bills.id']  # columns in Parent
        ),
    )

    type = mapped_column(String)

    id = mapped_column(String, ForeignKey("people.id"), primary_key=True)

def print_versions(session):
    print("Printing Versions")
    all_versions = session.query(Bill_Version).all()
    for version in all_versions:
        print(version)

class Bill_Version(Base):
    __tablename__ = "bill_versions"
    bill_chamber = mapped_column(String, primary_key=True)
    under = mapped_column(String, primary_key=True)
    bill_session = mapped_column(Integer, primary_key=True)
    bill_id = mapped_column(String, primary_key=True)
    version = mapped_column(Integer, primary_key=True)
    version_string = mapped_column(String)

    bill = relationship("Bill", back_populates="versions")

    __table_args__ = (
        ForeignKeyConstraint(
            ['bill_chamber', 'under', 'bill_session', 'bill_id'],          # columns in Child
            ['bills.chamber', 'bills.under', 'bills.session', 'bills.id']  # columns in Parent
        ),
    )

    text = mapped_column(String)
    text_link = mapped_column(String)
    summary = mapped_column(String)
    summary_link = mapped_column(String)

    links = relationship("Version_Link", back_populates="bill_version")

    policy_areas = relationship("Bill_Policy_Area", back_populates="version")

    def __str__(self):
        return "Version " + str(self.version) + " : " + self.summary

def print_policy_areas(session):
    print("Printing Policy Areas")
    all_areas = session.query(Bill_Policy_Area).all()
    for area in all_areas:
        print(area)

def get_all_policy_areas(session):
    smnt = (select(Bill_Policy_Area))
    return session.execute(smnt).scalars().all()

class Bill_Policy_Area(Base):
    __tablename__ = "bill_policy_areas"
    bill_chamber = mapped_column(String, primary_key=True)
    under = mapped_column(String, primary_key=True)
    bill_session = mapped_column(Integer, primary_key=True)
    bill_id = mapped_column(String, primary_key=True)
    bill_version = mapped_column(Integer, primary_key=True)

    policy_area = mapped_column(String, primary_key=True)

    version = relationship("Bill_Version", back_populates="policy_areas")

    __table_args__ = (
        ForeignKeyConstraint(
            ['bill_chamber', 'under', 'bill_session', 'bill_id', 'bill_version'],          # columns in Child
            ['bill_versions.bill_chamber', 'bill_versions.under', 'bill_versions.bill_session', 'bill_versions.bill_id', 'bill_versions.version']  # columns in Parent
        ),
    )

    def __str__(self):
        return self.policy_area




