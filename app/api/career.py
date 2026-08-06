import json

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.api.resume import ResumeParseError, extract_pdf_text
from app.engines.career_engine import run_career_analysis
from app.models.career import CareerAnalysisResult
from app.models.country_scoring import ResumeMarket
from app.services.candidate_service import build_candidate_profile


router = APIRouter(
    prefix="/career",
    tags=["Career Analysis Engine"],
)


@router.post(
    "/analyze",
    response_model=CareerAnalysisResult,
    summary="Run complete resume and job analysis",
)
async def analyze_career_opportunity(
    resume: UploadFile = File(...),
    job_description: str = Form(..., min_length=30),
    target_market: ResumeMarket = Form(...),
    willing_to_relocate: bool = Form(True),
    requires_sponsorship: bool | None = Form(None),
    notice_period_days: int | None = Form(None),
) -> CareerAnalysisResult:
    if resume.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF resumes are supported.",
        )

    file_bytes = await resume.read()

    try:
        resume_text = extract_pdf_text(file_bytes)
        candidate = build_candidate_profile(resume_text)

        return run_career_analysis(
            candidate=candidate,
            job_description=job_description,
            target_market=target_market,
            willing_to_relocate=willing_to_relocate,
            requires_sponsorship=requires_sponsorship,
            notice_period_days=notice_period_days,
        )

    except ResumeParseError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to complete career analysis: {exc}",
        ) from exc