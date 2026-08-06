from app.models.country_scoring import (
    CountryResumeScoreResult,
    ResumeMarket,
)
from app.models.candidate import CandidateProfile
from app.services.scoring_helpers import clamp_score, normalize_text


MARKET_SKILLS = {
    ResumeMarket.UAE: [
        "python",
        "fastapi",
        "azure",
        "azure ai foundry",
        "rag",
        "llm",
        "ai agent",
        "docker",
        "rest api",
        "enterprise",
    ],
    ResumeMarket.UK: [
        "python",
        "fastapi",
        "rag",
        "llm",
        "langchain",
        "machine learning",
        "testing",
        "docker",
        "sql",
        "cloud",
    ],
    ResumeMarket.SINGAPORE: [
        "python",
        "fastapi",
        "backend",
        "ai agent",
        "llm",
        "rag",
        "microservices",
        "distributed systems",
        "docker",
        "rest api",
    ],
}


def _calculate_profile_score(candidate: CandidateProfile) -> float:
    score = 0.0

    if candidate.name:
        score += 10

    if candidate.email:
        score += 10

    if candidate.phone:
        score += 10

    if candidate.location:
        score += 10

    if getattr(candidate, "summary", None):
        score += 15

    if len(candidate.skills) >= 8:
        score += 15
    elif candidate.skills:
        score += 8

    if candidate.experience:
        score += 15

    if candidate.projects:
        score += 10

    if candidate.education:
        score += 5

    return clamp_score(score)


def _calculate_technical_alignment(
    candidate: CandidateProfile,
    target_market: ResumeMarket,
) -> tuple[float, list[str], list[str]]:
    text = normalize_text(candidate.model_dump())
    expected_skills = MARKET_SKILLS[target_market]

    matched = [
        skill
        for skill in expected_skills
        if skill in text
    ]

    missing = [
        skill
        for skill in expected_skills
        if skill not in text
    ]

    score = (
        len(matched) / len(expected_skills) * 100
        if expected_skills
        else 0
    )

    return clamp_score(score), matched, missing


def _calculate_market_readiness(
    target_market: ResumeMarket,
    willing_to_relocate: bool,
    requires_sponsorship: bool | None,
    notice_period_days: int | None,
) -> tuple[float, list[str], list[str]]:
    score = 40.0
    strengths: list[str] = []
    improvements: list[str] = []

    if willing_to_relocate:
        score += 25
        strengths.append("Relocation willingness is clearly stated")
    else:
        improvements.append("State whether you are willing to relocate")

    if notice_period_days is not None:
        if notice_period_days <= 30:
            score += 20
            strengths.append("Availability is competitive")
        elif notice_period_days <= 60:
            score += 10
            improvements.append(
                "A notice period above 30 days may reduce some opportunities"
            )
        else:
            improvements.append(
                "A long notice period may affect international applications"
            )
    else:
        improvements.append("Add your notice period or availability")

    if target_market == ResumeMarket.UK:
        if requires_sponsorship is True:
            score += 5
            improvements.append(
                "State clearly that UK visa sponsorship is required"
            )
        elif requires_sponsorship is False:
            score += 15
            strengths.append("UK work-authorisation status is clear")
        else:
            improvements.append(
                "Clarify UK work-authorisation or sponsorship status"
            )

    elif target_market in {
        ResumeMarket.UAE,
        ResumeMarket.SINGAPORE,
    }:
        if requires_sponsorship is True:
            score += 8
            improvements.append(
                "Mention relocation readiness and employer-sponsored visa requirement"
            )
        elif requires_sponsorship is False:
            score += 15
        else:
            improvements.append(
                "Clarify whether employment visa sponsorship is required"
            )

    return clamp_score(score), strengths, improvements


def _market_specific_recommendations(
    target_market: ResumeMarket,
) -> tuple[list[str], list[str]]:
    required_statements: list[str] = []
    improvements: list[str] = []

    if target_market == ResumeMarket.UAE:
        required_statements.append(
            "Open to relocation to the UAE"
        )
        required_statements.append(
            "Available to join within [notice period]"
        )
        improvements.extend(
            [
                "Emphasise enterprise AI, Azure, backend APIs, and business impact",
                "Keep relocation readiness visible near the header",
            ]
        )

    elif target_market == ResumeMarket.UK:
        required_statements.append(
            "UK work authorisation: [status]"
        )
        required_statements.append(
            "Visa sponsorship: [required/not required]"
        )
        improvements.extend(
            [
                "Use British spelling consistently",
                "Highlight measurable outcomes and testing practices",
                "Keep the distinction between total software experience and recent AI experience clear",
            ]
        )

    elif target_market == ResumeMarket.SINGAPORE:
        required_statements.append(
            "Open to relocation to Singapore"
        )
        improvements.extend(
            [
                "Emphasise backend engineering, APIs, product development, and scalable systems",
                "Highlight AI Agents, LLM integration, and workflow automation",
                "Mention microservices or distributed systems only where you can defend the experience",
            ]
        )

    return required_statements, improvements


def evaluate_country_resume(
    candidate: CandidateProfile,
    target_market: ResumeMarket,
    willing_to_relocate: bool,
    requires_sponsorship: bool | None,
    notice_period_days: int | None,
) -> CountryResumeScoreResult:
    profile_score = _calculate_profile_score(candidate)

    technical_score, matched_skills, missing_skills = (
        _calculate_technical_alignment(
            candidate=candidate,
            target_market=target_market,
        )
    )

    market_score, market_strengths, market_improvements = (
        _calculate_market_readiness(
            target_market=target_market,
            willing_to_relocate=willing_to_relocate,
            requires_sponsorship=requires_sponsorship,
            notice_period_days=notice_period_days,
        )
    )

    required_statements, market_recommendations = (
        _market_specific_recommendations(target_market)
    )

    overall_score = clamp_score(
        profile_score * 0.35
        + technical_score * 0.40
        + market_score * 0.25
    )

    strengths: list[str] = []

    if profile_score >= 80:
        strengths.append("The resume contains the main recruiter-facing sections")

    if technical_score >= 75:
        strengths.append(
            f"Strong technical alignment for the {target_market.value} market"
        )

    if matched_skills:
        strengths.append(
            "Relevant skills found: "
            + ", ".join(matched_skills[:6])
        )

    strengths.extend(market_strengths)

    improvements: list[str] = []

    if missing_skills:
        improvements.append(
            "Consider adding evidence for: "
            + ", ".join(missing_skills[:6])
        )

    improvements.extend(market_improvements)
    improvements.extend(market_recommendations)

    if overall_score >= 85:
        recommendation = (
            f"Strong resume for {target_market.value}. "
            "Use targeted job-specific tailoring before applying."
        )
    elif overall_score >= 70:
        recommendation = (
            f"Good foundation for {target_market.value}, "
            "but several market-specific changes are recommended."
        )
    else:
        recommendation = (
            f"The resume needs further tailoring before being used "
            f"for {target_market.value} applications."
        )

    return CountryResumeScoreResult(
        target_market=target_market,
        overall_score=overall_score,
        profile_score=profile_score,
        market_readiness_score=market_score,
        technical_alignment_score=technical_score,
        strengths=list(dict.fromkeys(strengths))[:8],
        improvements=list(dict.fromkeys(improvements))[:10],
        required_statements=required_statements,
        recommendation=recommendation,
    )