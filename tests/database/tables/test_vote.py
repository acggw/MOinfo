import pytest
from unittest.mock import MagicMock
from database.tables.vote import Vote, Voted_In
from database.tables.bill_actions import Bill_Action

# -------------------------------
# 1️ Test Vote instantiation
# -------------------------------
def test_vote_instantiation():
    vote = Vote(
        guid=1,
        result="Passed",
        yes=50,
        no=30,
        abstain=5,
        absent=10,
        description="Vote on budget",
        bill_chamber="House",
        under="MO",
        bill_session="2025",
        bill_id="B001",
        primary_link="link_to_vote"
    )

    assert vote.guid == 1
    assert vote.result == "Passed"
    assert vote.yes == 50
    assert vote.no == 30
    assert vote.abstain == 5
    assert vote.absent == 10
    assert vote.description == "Vote on budget"
    assert vote.bill_chamber == "House"
    assert vote.under == "MO"
    assert vote.bill_session == "2025"
    assert vote.bill_id == "B001"
    assert vote.primary_link == "link_to_vote"
    assert Vote.__mapper_args__["polymorphic_identity"] == "vote"

# -------------------------------
# 2️ Test Voted_In instantiation
# -------------------------------
def test_voted_in_instantiation():
    voted_in = Voted_In(
        guid=1,
        id="P001",
        vote="Yes"
    )

    assert voted_in.guid == 1
    assert voted_in.id == "P001"
    assert voted_in.vote == "Yes"

# -------------------------------
# 3️ Test adding Vote to session
# -------------------------------
def test_vote_add_to_session():
    mock_session = MagicMock()
    vote = Vote(
        guid=1,
        result="Passed",
        yes=50,
        no=30,
        abstain=5,
        absent=10,
        description="Vote on budget",
        bill_chamber="House",
        under="MO",
        bill_session="2025",
        bill_id="B001",
        primary_link="link_to_vote"
    )

    mock_session.add(vote)
    mock_session.commit()

    mock_session.add.assert_called_once_with(vote)
    mock_session.commit.assert_called_once()

# -------------------------------
# 4️ Test adding Voted_In to session
# -------------------------------
def test_voted_in_add_to_session():
    mock_session = MagicMock()
    voted_in = Voted_In(guid=1, id="P001", vote="Yes")

    mock_session.add(voted_in)
    mock_session.commit()

    mock_session.add.assert_called_once_with(voted_in)
    mock_session.commit.assert_called_once()
