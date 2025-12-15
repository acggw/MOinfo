import pytest
from unittest.mock import MagicMock
from datetime import date
from database.tables.offices import Office, Held_Office

# -------------------------------
# 1️ Test Office instantiation
# -------------------------------
def test_office_instantiation():
    office = Office(
        name="Governor",
        government="Missouri",
        under="USA"
    )

    assert office.name == "Governor"
    assert office.government == "Missouri"
    assert office.under == "USA"

# -------------------------------
# 2️ Test Held_Office instantiation
# -------------------------------
def test_held_office_instantiation():
    held = Held_Office(
        office_name="Governor",
        government="Missouri",
        under="USA",
        person_id="P001",
        start=date(2020, 1, 1),
        end=date(2024, 12, 31),
        term_end=date(2024, 12, 31)
    )

    assert held.office_name == "Governor"
    assert held.government == "Missouri"
    assert held.under == "USA"
    assert held.person_id == "P001"
    assert held.start == date(2020, 1, 1)
    assert held.end == date(2024, 12, 31)
    assert held.term_end == date(2024, 12, 31)

# -------------------------------
# 3️ Test relationship assignment (person)
# -------------------------------
def test_held_office_person_relationship():
    mock_person = MagicMock()
    held = Held_Office(
        office_name="Governor",
        government="Missouri",
        under="USA",
        person_id="P001"
    )
    held.person = mock_person

    assert held.person == mock_person
