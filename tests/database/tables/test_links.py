import pytest
from unittest.mock import MagicMock
from database.tables.links import Bill_Action_Link, Version_Link

# -------------------------------
# 1️ Test Bill_Action_Link instantiation
# -------------------------------
def test_bill_action_link_instantiation():
    # Create a Bill_Action_Link instance
    link = Bill_Action_Link(
        guid=1,
        link="https://example.com",
        link_type="reference"
    )

    assert link.guid == 1
    assert link.link == "https://example.com"
    assert link.link_type == "reference"

# -------------------------------
# 2️ Test Bill_Action_Link relationship assignment
# -------------------------------
def test_bill_action_link_relationship():
    mock_action = MagicMock()
    link = Bill_Action_Link(guid=1)
    link.bill_action = mock_action

    assert link.bill_action == mock_action

# -------------------------------
# 3️ Test Version_Link instantiation
# -------------------------------
def test_version_link_instantiation():
    vlink = Version_Link(
        bill_chamber="House",
        under="MO",
        bill_session="2025",
        bill_id="B001",
        version=1,
        link="https://example.com/version",
        link_type="summary"
    )

    assert vlink.bill_chamber == "House"
    assert vlink.under == "MO"
    assert vlink.bill_session == "2025"
    assert vlink.bill_id == "B001"
    assert vlink.version == 1
    assert vlink.link == "https://example.com/version"
    assert vlink.link_type == "summary"

# -------------------------------
# 4️ Test Version_Link relationship assignment
# -------------------------------
def test_version_link_relationship():
    mock_version = MagicMock()
    vlink = Version_Link(
        bill_chamber="House",
        under="MO",
        bill_session="2025",
        bill_id="B001",
        version=1
    )

    vlink.bill_version = mock_version
    assert vlink.bill_version == mock_version
