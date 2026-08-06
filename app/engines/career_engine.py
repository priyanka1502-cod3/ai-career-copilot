from app.models.candidate import CandidateProfile
from app.models.career import CareerAnalysisResult
from app.models.country_scoring import ResumeMarket
from app.models.job import JobDescription
from app.models.market import CandidateMarketProfile, TargetCountry
from app.services.country_resume_service import evaluate_country_resume
from app.services.job_parser_service import parse_job_description
from app.services.market_fit_service import calculate_market_fit
from app.services.matching_service import calculate_match
from app.services.resume_score_service import calculate_resume_score


MARKET_TO_COUNTRY = {
    ResumeMarket.UAE: TargetCountry.UAE,
    ResumeMarket.UK: TargetCountry.UK,
    ResumeMarket.SINGAPORE: TargetCountry.SINGAPORE,
}


def clamp_score(score: float) -> float:
    return round(max(0.0, min(score, 100.0)), 2)


def get_decision(
    final_score: float,
    technical_score: float,
    visa_score: float,
) -> str:
    if visa_score <= 10:
        return "Skip"

    if final_score >= 85 and technical_score >= 75:
        return "Priority Apply"

    if final_score >= 70:
        return "Apply"

    if final_score >= 55:
        return "Consider"

    return "Skip"


def build_next_actions(
    missing_skills: list[str],
    country_improvements: list[str],
    resume_improvements: list[str],
) -> list[str]:
    actions: list[str] = []

    if missing_skills:
        actions.append(
            "Tailor the resume to address these job requirements: "
            + ", ".join(missing_skills[:5])
        )

    actions.extend(country_improvements[:3])
    actions.extend(resume_improvements[:3])

    return list(dict.fromkeys(actions))[:8]


def run_career_analysis(
    candidate: CandidateProfile,
    job_description: str,
    target_market: ResumeMarket,
    willing_to_relocate: bool,
    requires_sponsorship: bool | None,
    notice_period_days: int | None,
) -> CareerAnalysisResult:
    parsed_job = parse_job_description(job_description)

    matching_job = JobDescription(
        title=parsed_job.title,
        company=parsed_job.company,
        location=parsed_job.location,
        required_skills=parsed_job.required_skills,
        preferred_skills=parsed_job.preferred_skills,
    )

    job_match = calculate_match(
        candidate=candidate,
        job=matching_job,
    )

    resume_score = calculate_resume_score(candidate)

    country_resume_fit = evaluate_country_resume(
        candidate=candidate,
        target_market=target_market,
        willing_to_relocate=willing_to_relocate,
        requires_sponsorship=requires_sponsorship,
        notice_period_days=notice_period_days,
    )

    market_profile = CandidateMarketProfile(
        target_country=MARKET_TO_COUNTRY[target_market],
        current_country="India",
        willing_to_relocate=willing_to_relocate,
        notice_period_days=notice_period_days,
        work_authorization=(
            "Requires employer sponsorship"
            if requires_sponsorship
            else "Does not require sponsorship"
        ),
        requires_sponsorship=requires_sponsorship,
        preferred_cities=[],
    )

    market_fit = calculate_market_fit(
        candidate=market_profile,
        job=parsed_job,
    )

    market_average = (
        market_fit.location_score
        + market_fit.visa_score
        + market_fit.availability_score
    ) / 3

    final_score = clamp_score(
        job_match.match_score * 0.40
        + resume_score.overall_score * 0.25
        + country_resume_fit.overall_score * 0.20
        + market_average * 0.15
    )

    decision = get_decision(
        final_score=final_score,
        technical_score=job_match.match_score,
        visa_score=market_fit.visa_score,
    )

    strengths = list(
        dict.fromkeys(
            resume_score.strengths
            + country_resume_fit.strengths
        )
    )[:10]

    risks = list(
        dict.fromkeys(
            market_fit.warnings
            + country_resume_fit.improvements
        )
    )[:10]

    next_actions = build_next_actions(
        missing_skills=job_match.missing_skills,
        country_improvements=country_resume_fit.improvements,
        resume_improvements=resume_score.improvements,
    )

    return CareerAnalysisResult(
        candidate=candidate,
        job=parsed_job,
        resume_score=resume_score,
        job_match=job_match,
        market_fit=market_fit,
        country_resume_fit=country_resume_fit,
        final_score=final_score,
        decision=decision,
        strengths=strengths,
        risks=risks,
        next_actions=next_actions,
    )