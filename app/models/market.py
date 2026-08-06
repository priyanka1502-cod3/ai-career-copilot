from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

from app.models.job import ParsedJobDescription


class TargetCountry(str, Enum):
    UAE = "United Arab Emirates"
    UK = "United Kingdom"
    SINGAPORE = "Singapore"
    INDIA = "India"


class CandidateMarketProfile(BaseModel):
    target_country: TargetCountry
    current_country: Optional[str] = None
    willing_to_relocate: bool = False
    notice_period_days: Optional[int] = None
    work_authorization: Optional[str] = None
    requires_sponsorship: Optional[bool] = None
    preferred_cities: List[str] = Field(default_factory=list)
    minimum_salary: Optional[float] = None
    salary_currency: Optional[str] = None


class MarketFitResult(BaseModel):
    target_country: TargetCountry
    location_score: float
    visa_score: float
    availability_score: float
    salary_score: Optional[float] = None
    warnings: List[str] = Field(default_factory=list)


class MarketEvaluationRequest(BaseModel):
    candidate: CandidateMarketProfile
    job: ParsedJobDescription