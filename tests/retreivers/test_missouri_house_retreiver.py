import pytest
from unittest.mock import MagicMock, patch
import xml.etree.ElementTree as ET

import retreivers.missouri_house_retreiver as mod 

def test_extract_part():
    url = "https://documents.house.mo.gov/xml/251-HB1234.xml"
    assert mod.extract_part(url) == "HB1234"

@patch("retreivers.missouri_house_retreiver.requests.get")
def test_fetch_bill_data_success(mock_get):
    xml = "<root><Bill><Title /></Bill></root>"
    response = MagicMock()
    response.text = xml
    response.__str__.return_value = "<Response [200]>"
    mock_get.return_value = response

    fake_bill = [None, None, None, None, MagicMock(text="http://example.com")]

    result = mod.fetch_bill_data(fake_bill)

    assert isinstance(result, ET.Element)

@patch("retreivers.missouri_house_retreiver.requests.get")
def test_fetch_bill_data_failure(mock_get):
    response = MagicMock()
    response.__str__.return_value = "<Response [404]>"
    mock_get.return_value = response

    fake_bill = [None, None, None, None, MagicMock(text="bad-url")]

    assert mod.fetch_bill_data(fake_bill) is None

@patch("retreivers.missouri_house_retreiver.get_action")
@patch("retreivers.missouri_house_retreiver.get_guid_prefix", return_value=100)
def test_update_actions_new_action(mock_prefix, mock_get_action):
    session = MagicMock()
    producer = MagicMock()

    mock_get_action.return_value = None

    sql_bill = MagicMock()
    sql_bill.chamber = "House"
    sql_bill.under = "MO"
    sql_bill.session = "2025"
    sql_bill.id = "HB1"

    action_xml = MagicMock()
    action_xml.find.side_effect = lambda tag: {
        "Guid": MagicMock(text="1"),
        "Description": MagicMock(text="Passed")
    }[tag]

    result = mod.update_actions(
        session,
        [action_xml],
        sql_bill,
        producer
    )

    session.add.assert_called_once()
    session.commit.assert_called_once()
    producer.send.assert_called_once_with(
        "bill_action_retreived",
        {"guid": 1001}
    )
    assert result is True

@patch("retreivers.missouri_house_retreiver.get_version", return_value=None)
@patch("retreivers.missouri_house_retreiver.extract_from_pdf", return_value="PDF TEXT")
@patch("retreivers.missouri_house_retreiver.classify_bill")
def test_update_versions_new_version(mock_classify, mock_extract, mock_get_version):
    session = MagicMock()
    producer = MagicMock()

    bill_sql = MagicMock()
    bill_sql.chamber = "House"
    bill_sql.under = "MO"
    bill_sql.session = "2025"
    bill_sql.id = "HB1"

    bill = MagicMock()
    bill.findall.side_effect = lambda tag: {
        "BillText": [MagicMock(find=lambda x: {
            "BillVersionSort": MagicMock(text="1"),
            "BillTextLink": MagicMock(text="text.pdf")
        }[x])],
        "BillSummary": []
    }[tag]

    result = mod.update_versions(session, bill, bill_sql, producer)

    session.add.assert_called_once()
    session.commit.assert_called_once()
    producer.send.assert_called_once()
    assert result is True

@patch("retreivers.missouri_house_retreiver.get_xml_data")
@patch("retreivers.missouri_house_retreiver.fetch_bill_data")
@patch("retreivers.missouri_house_retreiver.update_bill")
@patch("retreivers.missouri_house_retreiver.update_versions")
@patch("retreivers.missouri_house_retreiver.update_actions")
@patch("retreivers.missouri_house_retreiver.Session")
def test_get_house_bills(
    mock_session,
    mock_update_actions,
    mock_update_versions,
    mock_update_bill,
    mock_fetch,
    mock_get_xml
):
    producer = MagicMock()

    bill = [
        None,
        None,
        MagicMock(text="2025"),
        MagicMock(text="1"),
        MagicMock(text="https://x/251-HB1.xml")
    ]

    mock_get_xml.return_value = [bill]

    xml = ET.fromstring("""
        <Bill>
            <BillNumber>HB1</BillNumber>
            <Title>
                <ShortTitle>Short</ShortTitle>
                <LongTitle>Long</LongTitle>
            </Title>
        </Bill>
    """)
    mock_fetch.return_value = xml

    session = MagicMock()
    mock_session.return_value.__enter__.return_value = session
    mock_update_bill.return_value = MagicMock()

    mod.get_house_bills(producer)

    mock_update_versions.assert_called_once()
    mock_update_actions.assert_called_once()
