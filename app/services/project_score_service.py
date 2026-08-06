from typing import Any

from app.services.scoring_helpers import clamp_score, normalize_text


PROJECT_SIGNALS = {
    "careercopilot": 15,
    "resume parsing": 8,
    "job parsing": 8,
    "job matching": 8,
    "market-fit": 5,
    "market fit": 5,
    "document intelligence": 12,
    "contract review": 10,
    "rag": 8,
    "ai agent": 8,
    "fastapi": 8,
    "rest api": 6,
    "faiss": 5,
    "chromadb": 5,
    "llm": 6,
    "semantic search": 6,
}


def calculate_project_score(
    candidate: dict[str, Any],
) -> tuple[float, list[str], list[str]]:
    text = normalize_text(candidate)

    score = 0.0
    matched_signals: list[str] = []

    for signal, points in PROJECT_SIGNALS.items():
        if signal in text:
            score += points
            matched_signals.append(signal)

    score = clamp_score(score)

    strengths: list[str] = []
    improvements: list[str] = []

    if "careercopilot" in matched_signals:
        strengths.append("CareerCopilot demonstrates end-to-end product development")

    if any(
        signal in matched_signals
        for signal in ["document intelligence", "contract review", "rag"]
    ):
        strengths.append("Projects demonstrate practical RAG and document AI experience")

    if "fastapi" in matched_signals or "rest api" in matched_signals:
        strengths.append("Projects include backend API development")

    if len(matched_signals) >= 7:
        strengths.append("Strong and relevant AI project portfolio")

    if not any(term in text for term in ["deployed", "deployment", "docker", "cloud"]):
        improvements.append("Mention how projects were deployed or hosted")

    if not any(term in text for term in ["users", "requests", "latency", "accuracy"]):
        improvements.append(
            "Add measurable project outcomes such as accuracy, users, or performance"
        )

    if not any(term in text for term in ["github", "huggingface.co", "demo"]):
        improvements.append("Add project repository or live demo links")

    return score, strengths, improvements