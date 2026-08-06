from typing import Any

from app.services.scoring_helpers import clamp_score, normalize_text


AI_PLATFORM_SKILLS = {
    "python": 12,
    "fastapi": 10,
    "rest api": 7,
    "rest APIs": 7,
    "langchain": 9,
    "llamaindex": 6,
    "rag": 10,
    "retrieval-augmented generation": 10,
    "llm": 8,
    "large language model": 8,
    "ai agent": 8,
    "prompt engineering": 5,
    "docker": 6,
    "sql": 5,
    "git": 4,
}

BONUS_SKILLS = {
    "azure": 4,
    "azure ai foundry": 5,
    "azure openai": 5,
    "faiss": 4,
    "chromadb": 4,
    "hugging face": 3,
    "microservices": 4,
    "distributed systems": 4,
    "kubernetes": 4,
    "redis": 3,
    "kafka": 3,
    "testing": 3,
    "pytest": 3,
}


def calculate_technical_score(
    candidate: dict[str, Any],
) -> tuple[float, list[str], list[str]]:
    searchable_text = normalize_text(candidate)

    score = 0.0
    matched_core: list[str] = []
    matched_bonus: list[str] = []

    for skill, points in AI_PLATFORM_SKILLS.items():
        if skill.lower() in searchable_text:
            score += points
            matched_core.append(skill)

    for skill, points in BONUS_SKILLS.items():
        if skill.lower() in searchable_text:
            score += points
            matched_bonus.append(skill)

    score = clamp_score(score)

    strengths: list[str] = []
    improvements: list[str] = []

    if "python" in matched_core:
        strengths.append("Strong Python foundation")

    if "fastapi" in matched_core or "rest api" in matched_core:
        strengths.append("Relevant backend API experience")

    if any(
        skill in matched_core
        for skill in ["rag", "retrieval-augmented generation", "llm", "ai agent"]
    ):
        strengths.append("Relevant Generative AI and LLM experience")

    if len(matched_core) >= 8:
        strengths.append("Broad technical alignment with AI platform roles")
    elif len(matched_core) < 5:
        improvements.append(
            "Add more evidence of Python backend, LLM, RAG, and API development"
        )

    if "docker" not in searchable_text:
        improvements.append("Add containerization experience if you have used Docker")

    if not any(
        term in searchable_text
        for term in ["pytest", "unit testing", "integration testing", "testing"]
    ):
        improvements.append("Mention unit or integration testing experience")

    if not any(
        term in searchable_text
        for term in ["microservices", "distributed systems", "messaging", "kafka"]
    ):
        improvements.append(
            "Add distributed systems or microservices experience where accurate"
        )

    return score, strengths, improvements