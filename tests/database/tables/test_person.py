import pytest
from unittest.mock import MagicMock
from database.tables.person import Person, get_person, get_person_by_name, get_next_id

# -------------------------------
# 1️ Test Person instantiation
# -------------------------------
def test_person_instantiation():
    p = Person(
        id="P001",
        name="John Doe",
        party="D",
        email="john@example.com",
        phone="123-456-7890"
    )

    assert p.id == "P001"
    assert p.name == "John Doe"
    assert p.party == "D"
    assert p.email == "john@example.com"
    assert p.phone == "123-456-7890"

# -------------------------------
# 2️ Test get_person
# -------------------------------
def test_get_person_calls_session_get():
    mock_session = MagicMock()
    person = Person(id="P001")
    mock_session.get.return_value = person

    result = get_person(mock_session, "P001")

    mock_session.get.assert_called_once_with(Person, ("P001"))
    assert result == person

# -------------------------------
# 3️ Test get_next_id
# -------------------------------
def test_get_next_id_calls_session_scalar():
    mock_session = MagicMock()
    mock_session.scalar.return_value = "P042"

    result = get_next_id(mock_session)

    mock_session.scalar.assert_called_once()
    assert result == "P042"

# -------------------------------
# 4️ Test get_person_by_name returns single result
# -------------------------------
def test_get_person_by_name_single_result():
    mock_session = MagicMock()
    person = Person(id="P001", name="John Doe")
    mock_session.scalars.return_value.all.return_value = [person]

    result = get_person_by_name(mock_session, "John Doe", "House", "MO")

    mock_session.scalars.assert_called_once()
    assert result == person

# -------------------------------
# 5️ Test get_person_by_name returns None for no results
# -------------------------------
def test_get_person_by_name_no_results():
    mock_session = MagicMock()
    mock_session.scalars.return_value.all.return_value = []

    result = get_person_by_name(mock_session, "Jane Doe", "House", "MO")
    assert result is None

# -------------------------------
# 6️ Test get_person_by_name multiple candidates with matching office
# -------------------------------
def test_get_person_by_name_multiple_candidates():
    mock_session = MagicMock()

    person1 = Person(id="P001", name="John Doe")
    person2 = Person(id="P002", name="John Doe")
    
    # Person2 has a matching office
    office = MagicMock()
    office.government = "House"
    office.under = "MO"
    person2.offices = [office]

    person1.offices = []

    mock_session.scalars.return_value.all.return_value = [person1, person2]

    result = get_person_by_name(mock_session, "John Doe", "House", "MO")
    
    assert result == person2
