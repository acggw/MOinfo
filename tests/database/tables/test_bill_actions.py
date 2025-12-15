import pytest
from unittest.mock import MagicMock, patch
from database.tables.bill_actions import Bill_Action, get_guid_prefix, get_action, print_actions
from database.tables.government_names import govt_names

# -------------------------------
# 1️ Test get_guid_prefix
# -------------------------------

@pytest.mark.parametrize(
    "name_1,name_2,name_3,name_4,expected",
    [
        (govt_names.US_GOVERNMENT_NAME, govt_names.MO_GOVERNMENT_NAME, govt_names.MO_GOVERNMENT_NAME, govt_names.MO_LOWER_HOUSE_NAME,  "1024001002"),
        (govt_names.US_GOVERNMENT_NAME, govt_names.MO_GOVERNMENT_NAME, govt_names.MO_GOVERNMENT_NAME, govt_names.MO_UPPER_HOUSE_NAME,  "1024001001"),
        (govt_names.US_GOVERNMENT_NAME, "Other", "Other", "Other",  "10000000"),
        ("Other", "Other", "Other", "Other",  "0")
    ]
)
def test_get_guid_prefix(name_1, name_2, name_3, name_4, expected):
    result = get_guid_prefix(name_1, name_2, name_3, name_4)
    print(name_1)
    assert str(result).startswith(str(expected))  # convert to str because function returns int

# -------------------------------
# 2️ Test Bill_Action instantiation and __str__
# -------------------------------

def test_bill_action_str():
    action = Bill_Action(
        guid=123,
        primary_link="link",
        description="Test description",
        bill_chamber="House",
        under="MO",
        bill_session="2025",
        bill_id="B001",
        type="bill_action"
    )

    assert str(action) == "B001 Test description"

# -------------------------------
# 3️ Test get_action
# -------------------------------

def test_get_action_returns_correct_object():
    mock_session = MagicMock()
    mock_action = Bill_Action(guid=1)
    mock_session.get.return_value = mock_action

    result = get_action(mock_session, 1)

    mock_session.get.assert_called_once_with(Bill_Action, 1)
    assert result == mock_action

# -------------------------------
# 4️ Test print_actions
# -------------------------------

def test_print_actions(capsys):
    mock_session = MagicMock()
    action1 = Bill_Action(guid=1, description="First", bill_id="B001")
    action2 = Bill_Action(guid=2, description="Second", bill_id="B002")
    mock_session.query.return_value.all.return_value = [action1, action2]

    print_actions(mock_session)

    captured = capsys.readouterr()
    assert "Printing Bill Actions" in captured.out
    assert "B001 First" in captured.out
    assert "B002 Second" in captured.out
