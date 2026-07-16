from pydantic import BaseModel, Field


class JobDescription(BaseModel):
    title: str
    company: str | None = None
    location: str | None = None
    description: str
    required_skills: list[str] = Field(default_factory=list)


class MatchResult(BaseModel):
    match_score: float
    matched_skills: list[str]
    missing_skills: list[str]
    recommendation: str