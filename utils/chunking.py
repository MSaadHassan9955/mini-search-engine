"""
chunking.py
-----------
Splits extracted PDF text into overlapping chunks suitable for embedding.
"""

from typing import List, Dict


def chunk_text(
    text: str,
    chunk_size: int = 800,
    chunk_overlap: int = 150,
) -> List[str]:
    """
    Split a long string into overlapping chunks based on character count,
    trying to break on sentence/paragraph boundaries where possible.

    Parameters
    ----------
    text : str
        The text to split.
    chunk_size : int
        Target maximum number of characters per chunk.
    chunk_overlap : int
        Number of overlapping characters between consecutive chunks
        (helps preserve context across chunk boundaries).

    Returns
    -------
    List[str]
        List of text chunks.
    """
    if not text:
        return []

    separators = ["\n\n", "\n", ". ", " "]
    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = min(start + chunk_size, text_len)

        if end < text_len:
            # Try to find a natural break point near the end of the window
            best_break = -1
            window = text[start:end]
            for sep in separators:
                idx = window.rfind(sep)
                if idx != -1:
                    best_break = idx + len(sep)
                    break
            if best_break != -1 and best_break > chunk_size * 0.5:
                end = start + best_break

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end >= text_len:
            break

        start = max(end - chunk_overlap, start + 1)

    return chunks


def chunk_document_pages(pages: List[Dict], chunk_size: int = 800, chunk_overlap: int = 150) -> List[Dict]:
    """
    Chunk a list of {"page": n, "text": "..."} dicts (as produced by
    pdf_utils.extract_text_from_pdf) into chunk-level records.

    Returns
    -------
    List[Dict]
        [{"page": 1, "chunk_id": 0, "text": "..."}, ...]
    """
    records = []
    for page in pages:
        chunks = chunk_text(page["text"], chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        for i, chunk in enumerate(chunks):
            records.append({"page": page["page"], "chunk_id": i, "text": chunk})
    return records
