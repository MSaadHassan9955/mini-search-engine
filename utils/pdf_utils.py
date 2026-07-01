"""
pdf_utils.py
------------
Helper functions to extract raw text from PDF files.
"""

from typing import List, Dict
from PyPDF2 import PdfReader


def extract_text_from_pdf(file) -> List[Dict]:
    """
    Extract text from a PDF file, page by page.

    Parameters
    ----------
    file : UploadedFile or file-like object
        A file object (e.g. from st.file_uploader) or a path string.

    Returns
    -------
    List[Dict]
        A list of dicts: [{"page": 1, "text": "..."}, {"page": 2, "text": "..."}, ...]
    """
    reader = PdfReader(file)
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = text.strip()
        if text:
            pages.append({"page": page_number, "text": text})

    return pages


def extract_text_from_path(path: str) -> List[Dict]:
    """Convenience wrapper to extract text directly from a file path on disk."""
    with open(path, "rb") as f:
        return extract_text_from_pdf(f)
