import pytest
from unittest.mock import MagicMock, patch

from utils.pdf_util import read_pdf

@patch("utils.pdf_util.pdfplumber.open")
def test_read_pdf_text_extraction_success(mock_open):
    # Mock page with text
    page = MagicMock()
    page.extract_text.return_value = "Hello world"

    pdf = MagicMock()
    pdf.pages = [page]
    mock_open.return_value.__enter__.return_value = pdf

    result = read_pdf("fake.pdf")

    assert "Hello world" in result

@patch("utils.pdf_util.pytesseract.image_to_string")
@patch("utils.pdf_util.convert_from_path")
@patch("utils.pdf_util.pdfplumber.open")
def test_read_pdf_ocr_fallback(mock_open, mock_convert, mock_ocr):
    # pdfplumber returns empty text
    page = MagicMock()
    page.extract_text.return_value = ""

    pdf = MagicMock()
    pdf.pages = [page]
    mock_open.return_value.__enter__.return_value = pdf

    # OCR mocks
    mock_convert.return_value = ["image1"]
    mock_ocr.return_value = "OCR text"

    result = read_pdf("fake.pdf")

    assert "OCR text" in result
    mock_convert.assert_called_once()
    mock_ocr.assert_called_once()

@patch("utils.pdf_util.pdfplumber.open", side_effect=Exception("boom"))
@patch("utils.pdf_util.convert_from_path")
@patch("utils.pdf_util.pytesseract.image_to_string")
def test_read_pdf_pdfplumber_exception(mock_ocr, mock_convert, mock_open):
    mock_convert.return_value = ["img"]
    mock_ocr.return_value = "OCR fallback"

    result = read_pdf("fake.pdf")

    assert "OCR fallback" in result

from utils.pdf_util import extract_from_pdf

def test_extract_from_pdf_none_link():
    assert extract_from_pdf(None) is None

@patch("utils.pdf_util.requests.get")
@patch("utils.pdf_util.pdfplumber.open")
def test_extract_from_pdf_success(mock_open, mock_get):
    mock_get.return_value.content = b"%PDF-FAKE"

    page = MagicMock()
    page.extract_text.return_value = "PDF content"

    pdf = MagicMock()
    pdf.pages = [page]
    mock_open.return_value.__enter__.return_value = pdf

    result = extract_from_pdf("http://example.com/test.pdf")

    assert "PDF content" in result

@patch("utils.pdf_util.requests.get")
@patch("utils.pdf_util.pdfplumber.open")
def test_extract_from_pdf_empty_text(mock_open, mock_get):
    mock_get.return_value.content = b"%PDF-FAKE"

    page = MagicMock()
    page.extract_text.return_value = None

    pdf = MagicMock()
    pdf.pages = [page]
    mock_open.return_value.__enter__.return_value = pdf

    result = extract_from_pdf("http://example.com/test.pdf")

    assert result == ""
