from enum import Enum

from pydantic import BaseModel, Field

from app.models.candidate import CandidateProfile


class ResumeMarket(str, Enum):
    UAE = "United Arab Emirates"
    UK = "United Kingdom"
    SINGAPORE = "Singapore"


class CountryResumeScoreRequest(BaseModel):
    candidate: CandidateProfile
    target_market: ResumeMarket
    willing_to_relocate: bool = False
    requires_sponsorship: bool | None = None
    notice_period_days: int | None = Field(default=None, ge=0)


class CountryResumeScoreResult(BaseModel):
    target_market: ResumeMarket
    overall_score: float = Field(ge=0, le=100)

    profile_score: float = Field(ge=0, le=100)
    market_readiness_score: float = Field(ge=0, le=100)
    technical_alignment_score: float = Field(ge=0, le=100)

    strengths: list[str] = Field(default_factory=list)
    improvements: list[str] = Field(default_factory=list)
    required_statements: list[str] = Field(default_factory=list)

    recommendation: str