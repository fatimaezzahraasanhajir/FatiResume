from __future__ import annotations

from io import BytesIO
from typing import Optional

import pdfplumber
from docx import Document


def _clean_text(text: str) -> str:
    text = text.replace("\x00", " ")
    lines = [ln.strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln]
    return "\n".join(lines).strip()


def parse_pdf_bytes(data: bytes) -> str:
    with pdfplumber.open(BytesIO(data)) as pdf:
        pages = []
        for page in pdf.pages:
            extracted = page.extract_text() or ""
            if extracted:
                pages.append(extracted)
    return _clean_text("\n".join(pages))


def parse_docx_bytes(data: bytes) -> str:
    doc = Document(BytesIO(data))
    parts = [p.text for p in doc.paragraphs if p.text]
    return _clean_text("\n".join(parts))


def parse_resume(resume_text: Optional[str], filename: Optional[str], file_bytes: Optional[bytes]) -> str:
    if resume_text and resume_text.strip():
        return _clean_text(resume_text)

    if not file_bytes or not filename:
        return ""

    lower = filename.lower()
    if lower.endswith(".pdf"):
        return parse_pdf_bytes(file_bytes)

    if lower.endswith(".docx"):
        return parse_docx_bytes(file_bytes)

    raise ValueError("Unsupported file type. Please upload a .pdf or .docx")
