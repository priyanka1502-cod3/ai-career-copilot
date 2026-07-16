from fastapi import APIRouter

from app.models.candidate import CandidateProfile
from app.models.job import JobDescription, MatchResult
from app.services.matching_service import calculate_match

router = APIRouter(
    prefix="/match",
    tags=["Matching"],
)


@router.post("/", response_model=MatchResult)
async def match_candidate_to_job(
    candidate: CandidateProfile,
    job: JobDescription,
) -> MatchResult:
    return calculate_match(candidate, job)