from sqlalchemy import Integer, String, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import mapped_column, relationship
from .base import Base

class Bill_Action_Link(Base):
    __tablename__ = "bill_action_links"

    guid = mapped_column(Integer, ForeignKey("bill_actions.guid"), primary_key=True)
    link = mapped_column(String)
    link_type = mapped_column(String)

    bill_action = relationship("Bill_Action", back_populates="secondary_links")

class Version_Link(Base):
    __tablename__ = "version_links"

    bill_chamber = mapped_column(String, primary_key=True)
    under = mapped_column(String, primary_key=True)
    bill_session = mapped_column(String, primary_key=True)
    bill_id = mapped_column(String, primary_key=True)
    version = mapped_column(Integer, primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ['bill_chamber', 'under', 'bill_session', 'bill_id', 'version'],          # columns in Child
            ['bill_versions.bill_chamber', 'bill_versions.under', 'bill_versions.bill_session', 'bill_versions.bill_id', 'bill_versions.version']  # columns in Parent
        ),
    )
    link = mapped_column(String)
    link_type = mapped_column(String)

    bill_version = relationship("Bill_Version", back_populates="links")