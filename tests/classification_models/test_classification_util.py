import pytest
from unittest.mock import MagicMock, patch

import classification_models.classification_util as classification_util

@pytest.fixture
def mock_bill_version():
    bill = MagicMock()
    bill.text = "Some bill text"
    bill.bill_chamber = "House"
    bill.under = "State"
    bill.bill_session = "2025"
    bill.bill_id = "HB123"
    bill.version = "v1"
    return bill

def test_classify_bill_adds_policy_areas(mock_bill_version):
    mock_session = MagicMock()
    policy_areas = ["Health", "Education"]

    with patch("classification_models.classification_util.predict_areas", return_value=policy_areas), \
         patch("classification_models.classification_util.Bill_Policy_Area") as mock_model:

        result = classification_util.classify_bill(mock_session, mock_bill_version)

        # Function returns True
        assert result is True

        # One DB insert per policy area
        assert mock_session.add.call_count == len(policy_areas)

        # Bill_Policy_Area constructed correctly
        mock_model.assert_any_call(
            bill_chamber="House",
            under="State",
            bill_session="2025",
            bill_id="HB123",
            bill_version="v1",
            policy_area="Health",
            version=mock_bill_version
        )

        mock_model.assert_any_call(
            bill_chamber="House",
            under="State",
            bill_session="2025",
            bill_id="HB123",
            bill_version="v1",
            policy_area="Education",
            version=mock_bill_version
        )

def test_classify_bill_no_policy_areas(mock_bill_version, capsys):
    mock_session = MagicMock()

    with patch("classification_models.classification_util.predict_areas", return_value=[]):
        result = classification_util.classify_bill(mock_session, mock_bill_version)

    captured = capsys.readouterr()

    assert "No policy areas identified" in captured.out
    mock_session.add.assert_not_called()
    assert result is True

def test_predict_areas_called_with_bill_text(mock_bill_version):
    mock_session = MagicMock()

    with patch("classification_models.classification_util.predict_areas", return_value=["Environment"]) as mock_predict:
        classification_util.classify_bill(mock_session, mock_bill_version)

    mock_predict.assert_called_once_with(mock_bill_version.text)




