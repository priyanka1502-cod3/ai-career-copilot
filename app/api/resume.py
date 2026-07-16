from io import BytesIO

from fastapi import APIRouter, File, HTTPException, UploadFile
from pypdf import PdfReader

from app.models.candidate import CandidateProfile
from app.services.candidate_service import build_candidate_profile

router = APIRouter(
    prefix="/resume",
    tags=["Resume"],
)


class ResumeParseError(Exception):
    """Raised when a resume cannot be parsed."""


def extract_pdf_text(file_bytes: bytes) -> str:
    if not file_bytes:
        raise ResumeParseError("The uploaded file is empty.")

    try:
        reader = PdfReader(BytesIO(file_bytes))
    except Exception as exc:
        raise ResumeParseError("Invalid PDF file.") from exc

    pages = []

    for page in reader.pages:
        text = (page.extract_text() or "").strip()
        if text:
            pages.append(text)

    full_text = "\n\n".join(pages).strip()

    if not full_text:
        raise ResumeParseError(
            "No readable text found in the PDF."
        )

    return full_text


@router.post("/parse", response_model=CandidateProfile)
async def parse_resume(
    file: UploadFile = File(...)
):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF resumes are supported.",
        )

    file_bytes = await file.read()

    try:
        text = extract_pdf_text(file_bytes)
    except ResumeParseError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    return build_candidate_profile(text)