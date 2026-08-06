from fastapi import APIRouter, HTTPException

from app.models.analysis import (
    FullAnalysisRequest,
    FullAnalysisResult,
)
from app.services.analysis_service import run_full_analysis


router = APIRouter(
    prefix="/analysis",
    tags=["Full Analysis"],
)


@router.post(
    "/full",
    response_model=FullAnalysisResult,
    summary="Run Complete Job Analysis",
)
def full_analysis(
    request: FullAnalysisRequest,
) -> FullAnalysisResult:
    try:
        return run_full_analysis(
            candidate=request.candidate,
            job_description=request.job_description,
            market_profile=request.market_profile,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to complete analysis: {exc}",
        ) from exc