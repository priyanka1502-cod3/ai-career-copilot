import re
from typing import List, Optional

from app.models.job import ParsedJobDescription


SKILLS = [
    "Python",
    "SQL",
    "FastAPI",
    "REST APIs",
    "Docker",
    "Git",
    "LangChain",
    "LlamaIndex",
    "RAG",
    "Large Language Models",
    "LLMs",
    "AI Agents",
    "Prompt Engineering",
    "Microservices",
    "Distributed Systems",
    "Databases",
    "Caching",
    "Kafka",
    "Redis",
    "MCP",
    "Azure AI Foundry",
    "Azure OpenAI",
    "AWS",
    "Azure",
    "Google Cloud",
    "FAISS",
    "ChromaDB",
    "Hugging Face",
    "Machine Learning",
    "Generative AI",
    "NLP",
    "Kubernetes",
]

def _find_first(
    patterns: list[str],
    text: str,
) -> str | None:
    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            re.IGNORECASE | re.MULTILINE,
        )

        if match:
            return match.group(1).strip()

    return None


def _extract_skills(text: str) -> List[str]:
    found_skills = []

    for skill in SKILLS:
        pattern = rf"\b{re.escape(skill)}\b"

        if re.search(pattern, text, re.IGNORECASE):
            found_skills.append(skill)

    return sorted(set(found_skills))


def _extract_salary(text: str) -> Optional[str]:
    salary_patterns = [
        r"((?:£|GBP)\s?[\d,]+(?:\s?[-–]\s?(?:£|GBP)?\s?[\d,]+)?(?:\s+per\s+year)?)",
        r"((?:AED)\s?[\d,]+(?:\s?[-–]\s?(?:AED)?\s?[\d,]+)?(?:\s+per\s+month)?)",
        r"((?:SGD|S\$)\s?[\d,]+(?:\s?[-–]\s?(?:SGD|S\$)?\s?[\d,]+)?)",
        r"((?:₹|INR)\s?[\d,.]+\s?(?:LPA|lakhs?)?)",
    ]

    return _find_first(salary_patterns, text)


def _extract_experience(text: str) -> Optional[str]:
    patterns = [
        r"(\d+\s*[-–]\s*\d+\s+years?(?:\s+of)?\s+experience)",
        r"(\d+\+?\s+years?(?:\s+of)?\s+experience)",
        r"(fresh graduates?(?:\s*/\s*\d+\s*[-–]\s*\d+\s+years?)?)",
        r"(0\s*[-–]\s*2\s+years?(?:\s+experience)?)",
    ]

    return _find_first(patterns, text)


def _extract_education(text: str) -> Optional[str]:
    education_patterns = [
        r"((?:master['’]?s|masters)\s+degree[^.\n]*)",
        r"((?:bachelor['’]?s|bachelors)\s+degree[^.\n]*)",
        r"((?:bachelor['’]?s|master['’]?s)\s+degree[^.\n]*)",
    ]

    return _find_first(education_patterns, text)


def _extract_visa_information(text: str) -> Optional[str]:
    visa_patterns = [
        r"([^.\n]*(?:visa sponsorship|sponsorship)[^.\n]*)",
        r"([^.\n]*(?:work authorisation|work authorization)[^.\n]*)",
        r"([^.\n]*(?:right to work)[^.\n]*)",
    ]

    return _find_first(visa_patterns, text)


def parse_job_description(text: str) -> ParsedJobDescription:
    title = _find_first(
        [
            r"^\s*job title\s*:\s*([^\r\n]+)",
            r"^\s*position\s*:\s*([^\r\n]+)",
        ],
        text,
    )

    company = _find_first(
        [
            r"^\s*company\s*:\s*([^\r\n]+)",
            r"^\s*company name\s*:\s*([^\r\n]+)",
        ],
        text,
    )

    location = _find_first(
        [
            r"^\s*location\s*:\s*([^\r\n]+)",
            r"\b(Singapore)\b",
            r"\b(London(?:,\s*United Kingdom)?)\b",
            r"\b(Dubai(?:,\s*UAE)?)\b",
        ],
        text,
    )

    employment_type = _find_first(
        [
            r"^\s*employment type\s*:\s*([^\r\n]+)",
            r"\b(full[- ]time|part[- ]time|contract|temporary|internship)\b",
        ],
        text,
    )

    return ParsedJobDescription(
        title=title,
        company=company,
        location=location,
        employment_type=employment_type,
        salary=_extract_salary(text),
        experience_requirement=_extract_experience(text),
        education_requirement=_extract_education(text),
        required_skills=_extract_skills(text),
        preferred_skills=[],
        visa_information=_extract_visa_information(text),
    )