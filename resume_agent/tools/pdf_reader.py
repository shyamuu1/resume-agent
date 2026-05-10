# pdf_reader.py
"""PDF Reader module."""


import os

from pdf2image import convert_from_path
from pypdf import PdfReader
import pytesseract


pytesseract.pytesseract.tesseract_cmd = r"C:/Tesseract/tesseract.exe"


def has_meaningful_text(text: str, min_chars:int = 100) -> bool:
    """Check if the text has meaningful content."""
    cleaned = text.strip()
    return len(cleaned) >= min_chars

def extract_text_from_pdf(pdf_path: str) -> str:

    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_image_based_pdf(path: str) -> str:
    """
    Convert each PDF page to an image, then run OCR on it.
    Used as fallback for scanned PDFs.
    """
    print("   Text extraction failed, falling back to OCR...")
    pages = convert_from_path(path, dpi=300)
    text = ""
    for page_index, page in enumerate(pages):
        print(f"   Processing page {page_index + 1}/{len(pages)}...")
        text += pytesseract.image_to_string(page)
    return text

def extract_pdf_text(path:str) -> str:
    """
    Smart PDF reader — tries text extraction first,
    falls back to OCR if the PDF is image-based.
    """
    print(f">> Reading PDF: {os.path.basename(path)}")

    if not os.path.exists(path):
        raise FileNotFoundError(f"PDF file not found: {path}")
    
    text = extract_text_from_pdf(path)

    if has_meaningful_text(text):
        print(f"   Text-based PDF detected — extracted {len(text)} characters")
        return text
    
    text = extract_image_based_pdf(path)
    if has_meaningful_text(text):
        print(f"   Image-based PDF detected — extracted {len(text)} characters via OCR")
        return text
    raise ValueError("Failed to extract meaningful text from PDF, even with OCR.")