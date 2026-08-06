from app.models.candidate import CandidateProfile
from app.models.scoring import ResumeScoreResult
from app.services.ats_score_service import calculate_ats_score
from app.services.experience_score_service import calculate_experience_score
from app.services.project_score_service import calculate_project_score
from app.services.technical_score_service import calculate_technical_score


def remove_duplicates(items: list[str]) -> list[str]:
    return list(dict.fromkeys(items))


def build_recommendation(overall_score: float) -> str:
    if overall_score >= 90:
        return (
            "Excellent resume for AI Platform and Generative AI Engineer roles. "
            "Focus next on measurable project outcomes and production deployment."
        )

    if overall_score >= 80:
        return (
            "Strong resume for AI and backend engineering roles. "
            "A few targeted improvements could make it more competitive."
        )

    if overall_score >= 70:
        return (
            "Good technical foundation, but the resume needs stronger evidence "
            "of relevant projects, outcomes, and production engineering."
        )

    if overall_score >= 60:
        return (
            "The resume has relevant experience but requires clearer structure, "
            "better technical alignment, and stronger project evidence."
        )

    return (
        "The resume needs substantial improvement before applying. "
        "Strengthen its structure, technical keywords, experience details, and projects."
    )


def calculate_resume_score(
    candidate: CandidateProfile,
) -> ResumeScoreResult:
    candidate_data = candidate.model_dump()

    ats_score, ats_strengths, ats_improvements = calculate_ats_score(
        candidate_data
    )

    technical_score, technical_strengths, technical_improvements = (
        calculate_technical_score(candidate_data)
    )

    experience_score, experience_strengths, experience_improvements = (
        calculate_experience_score(candidate_data)
    )

    project_score, project_strengths, project_improvements = (
        calculate_project_score(candidate_data)
    )

    overall_score = round(
        ats_score * 0.30
        + technical_score * 0.30
        + experience_score * 0.20
        + project_score * 0.20,
        2,
    )

    strengths = remove_duplicates(
        ats_strengths
        + technical_strengths
        + experience_strengths
        + project_strengths
    )

    improvements = remove_duplicates(
        ats_improvements
        + technical_improvements
        + experience_improvements
        + project_improvements
    )

    return ResumeScoreResult(
        overall_score=overall_score,
        ats_score=ats_score,
        technical_score=technical_score,
        experience_score=experience_score,
        project_score=project_score,
        strengths=strengths[:8],
        improvements=improvements[:8],
        recommendation=build_recommendation(overall_score),
    )