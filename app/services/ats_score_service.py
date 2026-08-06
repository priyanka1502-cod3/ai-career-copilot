from typing import Any

from app.services.scoring_helpers import (
    clamp_score,
    get_first_available,
    has_meaningful_value,
    normalize_text,
)


def calculate_ats_score(candidate: dict[str, Any]) -> tuple[float, list[str], list[str]]:
    score = 0.0
    strengths: list[str] = []
    improvements: list[str] = []

    name = get_first_available(candidate, ["name", "full_name"])
    email = get_first_available(candidate, ["email", "email_address"])
    phone = get_first_available(candidate, ["phone", "phone_number"])
    location = get_first_available(candidate, ["location", "address"])

    summary = get_first_available(
        candidate,
        ["summary", "professional_summary", "profile"],
    )

    skills = get_first_available(
        candidate,
        ["skills", "technical_skills"],
        default=[],
    )

    experience = get_first_available(
        candidate,
        ["experience", "work_experience", "employment_history"],
        default=[],
    )

    projects = get_first_available(
        candidate,
        ["projects", "personal_projects"],
        default=[],
    )

    education = get_first_available(
        candidate,
        ["education", "academic_background"],
        default=[],
    )

    certifications = get_first_available(
        candidate,
        ["certifications", "certificates"],
        default=[],
    )

    # Contact information: 20 points
    contact_fields = [name, email, phone, location]
    completed_contact_fields = sum(
        has_meaningful_value(field) for field in contact_fields
    )

    score += completed_contact_fields * 5

    if completed_contact_fields == 4:
        strengths.append("Complete contact information")
    else:
        improvements.append("Add complete name, email, phone, and location details")

    # Summary: 10 points
    if has_meaningful_value(summary):
        summary_text = normalize_text(summary)

        if 40 <= len(summary_text.split()) <= 120:
            score += 10
            strengths.append("Professional summary has a suitable length")
        else:
            score += 6
            improvements.append(
                "Keep the professional summary between approximately 40 and 120 words"
            )
    else:
        improvements.append("Add a short professional summary")

    # Skills: 20 points
    skills_text = normalize_text(skills)
    skill_count = len(
        {
            skill.strip()
            for skill in skills_text.replace("•", ",").split(",")
            if skill.strip()
        }
    )

    if skill_count >= 8:
        score += 20
        strengths.append("Strong technical skills coverage")
    elif skill_count >= 4:
        score += 12
        improvements.append("Add more role-relevant technical skills")
    elif has_meaningful_value(skills):
        score += 6
        improvements.append("Expand and organize the technical skills section")
    else:
        improvements.append("Add a technical skills section")

    # Experience: 20 points
    if has_meaningful_value(experience):
        score += 20
        strengths.append("Professional experience is included")
    else:
        improvements.append("Add professional experience")

    # Projects: 15 points
    if has_meaningful_value(projects):
        score += 15
        strengths.append("Relevant projects are included")
    else:
        improvements.append("Add relevant technical or AI projects")

    # Education: 10 points
    if has_meaningful_value(education):
        score += 10
        strengths.append("Education details are included")
    else:
        improvements.append("Add education details")

    # Certifications: 5 points
    if has_meaningful_value(certifications):
        score += 5
    else:
        improvements.append("Add relevant certifications where applicable")

    return clamp_score(score), strengths, improvements