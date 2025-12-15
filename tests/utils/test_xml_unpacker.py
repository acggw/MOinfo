from unittest.mock import patch, MagicMock
import xml.etree.ElementTree as ET

from utils.xml_unpacker import get_xml_data

@patch("utils.xml_unpacker.requests.get")
def test_get_xml_data_success(mock_get):
    xml = "<root><item>test</item></root>"

    response = MagicMock()
    response.text = xml
    response.__str__.return_value = "<Response [200]>"
    mock_get.return_value = response

    result = get_xml_data("http://example.com/data.xml")

    assert isinstance(result, ET.Element)
    assert result.tag == "root"

@patch("utils.xml_unpacker.requests.get")
def test_get_xml_data_failure(mock_get):
    response = MagicMock()
    response.__str__.return_value = "<Response [404]>"
    mock_get.return_value = response

    result = get_xml_data("http://example.com/data.xml")

    assert result is None

@patch("utils.xml_unpacker.requests.get")
def test_get_xml_data_calls_requests(mock_get):
    response = MagicMock()
    response.__str__.return_value = "<Response [200]>"
    response.text = "<root />"
    mock_get.return_value = response

    get_xml_data("http://example.com/data.xml")

    mock_get.assert_called_once_with("http://example.com/data.xml")

import pytest
from unittest.mock import patch, MagicMock

@patch("utils.xml_unpacker.requests.get")
def test_get_xml_data_invalid_xml(mock_get):
    response = MagicMock()
    response.__str__.return_value = "<Response [200]>"
    response.text = "<root><unclosed>"
    mock_get.return_value = response

    with pytest.raises(ET.ParseError):
        get_xml_data("http://example.com/data.xml")

@patch("utils.xml_unpacker.requests.get")
def test_get_xml_data_prints_error(mock_get, capsys):
    response = MagicMock()
    response.__str__.return_value = "<Response [500]>"
    mock_get.return_value = response

    get_xml_data("http://bad-url")

    captured = capsys.readouterr()
    assert "Error fetching data from http://bad-url" in captured.out
