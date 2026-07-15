from io import BytesIO

from pypdf import PdfReader


class ResumeParseError(Exception):
    """Raised when a resume PDF cannot be parsed."""


def extract_pdf_text(file_bytes: bytes) -> str:
    """
    Extract readable text from a PDF supplied as bytes.

    Raises:
        ResumeParseError: If the file is empty, invalid, or has no readable text.
    """
    if not file_bytes:
        raise ResumeParseError("The uploaded file is empty.")

    try:
        reader = PdfReader(BytesIO(file_bytes))
    except Exception as exc:
        raise ResumeParseError("The uploaded file is not a valid PDF.") from exc

    pages: list[str] = []

    for page in reader.pages:
        page_text = (page.extract_text() or "").strip()

        if page_text:
            pages.append(page_text)

    full_text = "\n\n".join(pages).strip()

    if not full_text:
        raise ResumeParseError(
            "No readable text was found. The PDF may contain scanned images."
        )

    return full_text