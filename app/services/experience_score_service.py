import re
from datetime import datetime
from typing import Any

from app.services.scoring_helpers import clamp_score, normalize_text


def extract_stated_years(text: str) -> float:
    patterns = [
        r"(\d+(?:\.\d+)?)\+?\s*years?\s+of\s+(?:professional\s+)?experience",
        r"over\s+(\d+(?:\.\d+)?)\s*years?",
        r"more than\s+(\d+(?:\.\d+)?)\s*years?",
    ]

    years: list[float] = []

    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)

        for match in matches:
            try:
                years.append(float(match))
            except ValueError:
                continue

    return max(years, default=0.0)


def extract_date_ranges_years(text: str) -> float:
    pattern = (
        r"(\d{2})/(\d{4})\s*[-–]\s*"
        r"(?:(\d{2})/(\d{4})|present)"
    )

    total_months = 0
    now = datetime.now()

    for match in re.finditer(pattern, text, re.IGNORECASE):
        start_month = int(match.group(1))
        start_year = int(match.group(2))

        if match.group(3) and match.group(4):
            end_month = int(match.group(3))
            end_year = int(match.group(4))
        else:
            end_month = now.month
            end_year = now.year

        months = (
            (end_year - start_year) * 12
            + end_month
            - start_month
        )

        if months > 0:
            total_months += months

    return round(total_months / 12, 1)


def calculate_experience_score(
    candidate: dict[str, Any],
) -> tuple[float, list[str], list[str]]:
    text = normalize_text(candidate)

    stated_years = extract_stated_years(text)
    calculated_years = extract_date_ranges_years(text)
    years = max(stated_years, calculated_years)

    score = 0.0
    strengths: list[str] = []
    improvements: list[str] = []

    if years >= 6:
        score += 55
        strengths.append(
            f"Strong professional experience of approximately {years:g} years"
        )
    elif years >= 4:
        score += 45
    elif years >= 2:
        score += 30
    elif years > 0:
        score += 15
    else:
        improvements.append(
            "State total years of professional experience clearly"
        )

    if any(
        term in text
        for term in [
            "generative ai",
            "large language model",
            "llm",
            "rag",
            "ai agent",
        ]
    ):
        score += 20
        strengths.append("Hands-on Generative AI experience")

    if any(
        term in text
        for term in [
            "backend",
            "fastapi",
            "rest api",
            "php developer",
            "software engineer",
        ]
    ):
        score += 15
        strengths.append("Relevant backend engineering background")

    if re.search(r"\b\d+(?:\.\d+)?\s*%", text):
        score += 10
        strengths.append("Includes measurable achievements")
    else:
        improvements.append(
            "Add measurable outcomes to selected experience bullets"
        )

    return clamp_score(score), strengths, improvements