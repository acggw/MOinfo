import os
import PyPDF2
import pdfplumber
from pdf2image import convert_from_path
import pytesseract
import requests
from io import BytesIO

def read_pdf(file_path):
    text = ""

    # First try text extraction with pdfplumber
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Text extraction failed: {e}")

    # If no text found, fall back to OCR
    if not text.strip():
        print("No text found, using OCR...")
        try:
            pages = convert_from_path(file_path)
            for page in pages:
                text += pytesseract.image_to_string(page) + "\n"
        except Exception as e:
            print(f"OCR failed: {e}")

    return text

def extract_from_pdf(link):
    if(link == None):
        return None
    response = requests.get(link)
    pdf_file = BytesIO(response.content)
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

#print(extract_from_pdf("https://documents.house.mo.gov/billtracking/bills254/hlrbillspdf/3344H.01T.pdf"))