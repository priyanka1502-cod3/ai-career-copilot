from pydantic import BaseModel, Field

from app.models.candidate import CandidateProfile


class ResumeScoreRequest(BaseModel):
    candidate: CandidateProfile


class ResumeScoreResult(BaseModel):
    overall_score: float = Field(ge=0, le=100)

    ats_score: float = Field(ge=0, le=100)
    technical_score: float = Field(ge=0, le=100)
    experience_score: float = Field(ge=0, le=100)
    project_score: float = Field(ge=0, le=100)

    strengths: list[str] = Field(default_factory=list)
    improvements: list[str] = Field(default_factory=list)

    recommendation: str