from pydantic import BaseModel, Field

from app.models.candidate import CandidateProfile
from app.models.country_scoring import CountryResumeScoreResult, ResumeMarket
from app.models.job import MatchResult, ParsedJobDescription
from app.models.market import MarketFitResult
from app.models.scoring import ResumeScoreResult


class CareerAnalysisResult(BaseModel):
    candidate: CandidateProfile
    job: ParsedJobDescription

    resume_score: ResumeScoreResult
    job_match: MatchResult
    market_fit: MarketFitResult
    country_resume_fit: CountryResumeScoreResult

    final_score: float = Field(ge=0, le=100)
    decision: str

    strengths: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)