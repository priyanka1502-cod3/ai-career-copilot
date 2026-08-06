from typing import List

from pydantic import BaseModel, Field

from app.models.candidate import CandidateProfile
from app.models.job import MatchResult, ParsedJobDescription
from app.models.market import (
    CandidateMarketProfile,
    MarketFitResult,
)


class FullAnalysisRequest(BaseModel):
    candidate: CandidateProfile
    job_description: str = Field(..., min_length=30)
    market_profile: CandidateMarketProfile


class FullAnalysisResult(BaseModel):
    candidate: CandidateProfile
    job: ParsedJobDescription
    matching: MatchResult
    market_fit: MarketFitResult

    overall_score: float
    decision: str
    reasons: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)