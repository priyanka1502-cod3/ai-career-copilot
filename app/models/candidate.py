from pydantic import BaseModel, Field


class CandidateProfile(BaseModel):
    """
    Represents the structured profile extracted
    from a candidate's resume.
    """

    name: str | None = None
    email: str | None = None
    phone: str | None = None
    location: str | None = None

    skills: list[str] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)
    experience: list[str] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)

    raw_text: str = ""