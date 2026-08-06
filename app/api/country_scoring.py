from fastapi import APIRouter, HTTPException

from app.models.country_scoring import (
    CountryResumeScoreRequest,
    CountryResumeScoreResult,
)
from app.services.country_resume_service import (
    evaluate_country_resume,
)


router = APIRouter(
    prefix="/country-resume",
    tags=["Country Resume Evaluation"],
)


@router.post(
    "/evaluate",
    response_model=CountryResumeScoreResult,
    summary="Evaluate a resume for a target country",
)
def evaluate_resume_for_country(
    request: CountryResumeScoreRequest,
) -> CountryResumeScoreResult:
    try:
        return evaluate_country_resume(
            candidate=request.candidate,
            target_market=request.target_market,
            willing_to_relocate=request.willing_to_relocate,
            requires_sponsorship=request.requires_sponsorship,
            notice_period_days=request.notice_period_days,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to evaluate the resume: {exc}",
        ) from exc