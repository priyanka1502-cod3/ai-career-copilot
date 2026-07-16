from app.models.candidate import CandidateProfile
from app.models.job import JobDescription, MatchResult


def normalize_skills(skills: list[str]) -> set[str]:
    return {skill.strip().lower() for skill in skills if skill.strip()}


def calculate_match(
    candidate: CandidateProfile,
    job: JobDescription,
) -> MatchResult:
    candidate_skills = normalize_skills(candidate.skills)
    job_skills = normalize_skills(job.required_skills)

    if not job_skills:
        return MatchResult(
            match_score=0.0,
            matched_skills=[],
            missing_skills=[],
            recommendation="No required skills were provided.",
        )

    matched = sorted(candidate_skills.intersection(job_skills))
    missing = sorted(job_skills.difference(candidate_skills))

    score = round((len(matched) / len(job_skills)) * 100, 2)

    if score >= 85:
        recommendation = "Apply immediately"
    elif score >= 70:
        recommendation = "Apply after minor resume tailoring"
    elif score >= 50:
        recommendation = "Consider applying if the role is a priority"
    else:
        recommendation = "Low match — focus on stronger opportunities"

    return MatchResult(
        match_score=score,
        matched_skills=matched,
        missing_skills=missing,
        recommendation=recommendation,
    )