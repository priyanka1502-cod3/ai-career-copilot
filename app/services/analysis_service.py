from app.models.analysis import FullAnalysisResult
from app.models.candidate import CandidateProfile
from app.models.job import JobDescription, ParsedJobDescription
from app.models.market import CandidateMarketProfile
from app.services.job_parser_service import parse_job_description
from app.services.market_fit_service import calculate_market_fit
from app.services.matching_service import calculate_match


def _clamp(score: float) -> float:
    return round(max(0.0, min(score, 100.0)), 2)


def _build_matching_job(
    parsed_job: ParsedJobDescription,
) -> JobDescription:
    """
    Converts the richer parsed-job model into the model currently
    expected by the skill-matching service.
    """
    return JobDescription(
        title=parsed_job.title,
        company=parsed_job.company,
        location=parsed_job.location,
        required_skills=parsed_job.required_skills,
        preferred_skills=parsed_job.preferred_skills,
    )


def _calculate_overall_score(
    match_score: float,
    location_score: float,
    visa_score: float,
    availability_score: float,
) -> float:
    """
    Weighted Phase 1 score.

    Technical matching receives the largest weight because it is the
    strongest indicator of role suitability. Visa, location and
    availability measure whether the opportunity is practical.
    """
    score = (
        match_score * 0.60
        + location_score * 0.15
        + visa_score * 0.15
        + availability_score * 0.10
    )

    return _clamp(score)


def _get_decision(
    overall_score: float,
    visa_score: float,
    match_score: float,
) -> str:
    # A hard visa conflict should prevent an "Apply" result even when
    # the technical score is high.
    if visa_score <= 10:
        return "Skip"

    if overall_score >= 80 and match_score >= 70:
        return "Priority Apply"

    if overall_score >= 65:
        return "Apply"

    if overall_score >= 50:
        return "Consider"

    return "Skip"


def _build_reasons(
    match_score: float,
    location_score: float,
    visa_score: float,
    availability_score: float,
) -> list[str]:
    reasons: list[str] = []

    if match_score >= 80:
        reasons.append("Strong technical and skill alignment.")
    elif match_score >= 65:
        reasons.append("Good technical alignment with some skill gaps.")
    elif match_score >= 50:
        reasons.append("Partial technical alignment.")
    else:
        reasons.append("The job has significant technical skill gaps.")

    if location_score >= 80:
        reasons.append("The job location matches the target market.")
    elif location_score >= 60:
        reasons.append("The location is viable because relocation is accepted.")
    else:
        reasons.append("The job location may not match the candidate's preferences.")

    if visa_score >= 80:
        reasons.append("No major work-authorisation conflict was identified.")
    elif visa_score >= 40:
        reasons.append("Visa sponsorship or work authorisation needs confirmation.")
    else:
        reasons.append("The stated visa conditions may make the role impractical.")

    if availability_score >= 80:
        reasons.append("The candidate's availability is competitive.")
    else:
        reasons.append("The notice period may affect the application.")

    return reasons


def run_full_analysis(
    candidate: CandidateProfile,
    job_description: str,
    market_profile: CandidateMarketProfile,
) -> FullAnalysisResult:
    parsed_job = parse_job_description(job_description)

    matching_job = _build_matching_job(parsed_job)

    matching_result = calculate_match(
        candidate=candidate,
        job=matching_job,
    )

    market_result = calculate_market_fit(
        candidate=market_profile,
        job=parsed_job,
    )

    overall_score = _calculate_overall_score(
        match_score=matching_result.match_score,
        location_score=market_result.location_score,
        visa_score=market_result.visa_score,
        availability_score=market_result.availability_score,
    )

    decision = _get_decision(
        overall_score=overall_score,
        visa_score=market_result.visa_score,
        match_score=matching_result.match_score,
    )

    reasons = _build_reasons(
        match_score=matching_result.match_score,
        location_score=market_result.location_score,
        visa_score=market_result.visa_score,
        availability_score=market_result.availability_score,
    )

    return FullAnalysisResult(
        candidate=candidate,
        job=parsed_job,
        matching=matching_result,
        market_fit=market_result,
        overall_score=overall_score,
        decision=decision,
        reasons=reasons,
        warnings=market_result.warnings,
    )