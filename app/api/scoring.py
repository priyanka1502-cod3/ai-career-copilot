from fastapi import APIRouter, HTTPException

from app.models.scoring import ResumeScoreRequest, ResumeScoreResult
from app.services.resume_score_service import calculate_resume_score


router = APIRouter(
    prefix="/scoring",
    tags=["Resume Scoring"],
)


@router.post(
    "/resume",
    response_model=ResumeScoreResult,
    summary="Score a parsed resume",
)
def score_resume(request: ResumeScoreRequest) -> ResumeScoreResult:
    try:
        return calculate_resume_score(request.candidate)

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to calculate resume score: {exc}",
        ) from exc