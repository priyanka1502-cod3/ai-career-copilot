from fastapi import APIRouter, File, HTTPException, UploadFile

from app.models.candidate import CandidateProfile
from app.parser.resume_parser import ResumeParseError, extract_pdf_text
from app.services.candidate_service import build_candidate_profile

router = APIRouter(prefix="/resume", tags=["Resume"])


@router.post("/parse", response_model=CandidateProfile)
async def parse_resume(
    file: UploadFile = File(...),
) -> CandidateProfile:
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