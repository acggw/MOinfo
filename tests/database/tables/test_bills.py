import pytest
from unittest.mock import MagicMock
from database.tables.bills import (
    Bill, Bill_Version, Bill_Policy_Area, Sponsored_By,
    get_bill, get_version, update_bill, print_bills, retreive_bill, get_all_policy_areas
)

# -------------------------------
# 1️ Test get_bill
# -------------------------------
def test_get_bill_calls_session_get():
    mock_session = MagicMock()
    mock_bill = Bill(chamber="House", under="MO", session="2025", id="B001")
    mock_session.get.return_value = mock_bill

    result = get_bill(mock_session, "House", "MO", "2025", "B001")

    mock_session.get.assert_called_once_with(Bill, ("House", "MO", "2025", "B001"))
    assert result == mock_bill

# -------------------------------
# 2️ Test get_version
# -------------------------------
def test_get_version_calls_session_get():
    mock_session = MagicMock()
    mock_version = Bill_Version(bill_chamber="House", under="MO", bill_session=2025, bill_id="B001", version=1)
    mock_session.get.return_value = mock_version

    result = get_version(mock_session, "House", "MO", 2025, "B001", 1)

    mock_session.get.assert_called_once_with(Bill_Version, ("House", "MO", 2025, "B001", 1))
    assert result == mock_version

# -------------------------------
# 3️ Test update_bill inserts new bill if not exists
# -------------------------------
def test_update_bill_inserts_new_if_not_exists():
    mock_session = MagicMock()
    mock_session.get.return_value = None  # Simulate bill not existing

    fields = {"chamber":"House", "under":"MO", "session":"2025", "id":"B001", "short_title":"Test Bill"}

    result = update_bill(mock_session, **fields)

    # Assert add and commit called
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    assert isinstance(result, Bill)
    assert result.short_title == "Test Bill"

# -------------------------------
# 4️ Test update_bill returns existing bill
# -------------------------------
def test_update_bill_returns_existing_bill():
    mock_session = MagicMock()
    existing_bill = Bill(chamber="House", under="MO", session="2025", id="B001")
    mock_session.get.return_value = existing_bill

    fields = {"chamber":"House", "under":"MO", "session":"2025", "id":"B001"}

    result = update_bill(mock_session, **fields)

    # Should NOT call add or commit
    mock_session.add.assert_not_called()
    mock_session.commit.assert_not_called()
    assert result == existing_bill

# -------------------------------
# 5️ Test retreive_bill calls execute correctly
# -------------------------------
def test_retreive_bill_calls_execute():
    mock_session = MagicMock()
    mock_bill = Bill(chamber="House", under="MO", session="2025", id="B001")
    mock_session.execute.return_value.scalars.return_value.first.return_value = mock_bill

    result = retreive_bill(mock_session, "House", "2025", "B001")

    mock_session.execute.assert_called_once()
    assert result == mock_bill

# -------------------------------
# 6️ Test print_bills prints bills and versions
# -------------------------------
def test_print_bills(capsys):
    mock_session = MagicMock()
    version1 = Bill_Version(version=1, summary="Summary1")
    version2 = Bill_Version(version=2, summary="Summary2")
    bill1 = Bill(chamber="House", under="MO", session="2025", id="B001", short_title="Bill1")
    bill1.versions = [version1, version2]
    mock_session.query.return_value.all.return_value = [bill1]

    print_bills(mock_session)

    captured = capsys.readouterr()
    assert "Printing Bills" in captured.out
    assert "B001 in the House under MO - 2025 : Bill1" in captured.out
    assert "Version 1 : Summary1" in captured.out
    assert "Version 2 : Summary2" in captured.out

# -------------------------------
# 7️ Test get_all_policy_areas calls execute and returns results
# -------------------------------
def test_get_all_policy_areas_returns_results():
    mock_session = MagicMock()
    area1 = Bill_Policy_Area(policy_area="Finance")
    area2 = Bill_Policy_Area(policy_area="Health")
    mock_session.execute.return_value.scalars.return_value.all.return_value = [area1, area2]

    result = get_all_policy_areas(mock_session)

    mock_session.execute.assert_called_once()
    assert result == [area1, area2]
