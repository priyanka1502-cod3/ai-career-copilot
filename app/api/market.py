from fastapi import APIRouter

from app.models.market import MarketEvaluationRequest, MarketFitResult
from app.services.market_fit_service import calculate_market_fit


router = APIRouter(
    prefix="/market",
    tags=["Market Fit"],
)


@router.post("/evaluate", response_model=MarketFitResult)
def evaluate_market_fit(
    request: MarketEvaluationRequest,
) -> MarketFitResult:
    return calculate_market_fit(
        candidate=request.candidate,
        job=request.job,
    )