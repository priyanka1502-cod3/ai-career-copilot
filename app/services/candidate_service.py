import re

from app.models.candidate import CandidateProfile


SKILL_KEYWORDS = [
    "Python",
    "SQL",
    "FastAPI",
    "LangChain",
    "LlamaIndex",
    "FAISS",
    "ChromaDB",
    "Docker",
    "Git",
    "Azure AI Foundry",
    "Azure OpenAI",
    "Hugging Face",
    "Groq API",
    "Llama 3",
    "RAG",
    "Prompt Engineering",
    "Semantic Search",
    "Vector Search",
    "AI Agents",
    "LLM Applications",
    "REST APIs",
    "Scikit-learn",
    "NumPy",
    "Power BI",
    "Tableau",
]


SECTION_NAMES = {
    "experience": ["experience", "professional experience", "work experience"],
    "education": ["education", "academic background"],
    "projects": ["projects", "selected projects", "key projects"],
    "certifications": [
        "certifications",
        "licenses & certifications",
        "licenses and certifications",
    ],
}


def extract_email(text: str) -> str | None:
    match = re.search(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        text,
    )
    return match.group(0) if match else None


def extract_phone(text: str) -> str | None:
    compact_text = re.sub(r"\s+", "", text)

    match = re.search(
        r"(?:\+91[-]?)?[6-9]\d{9}",
        compact_text,
    )

    return match.group(0) if match else None


def extract_name(text: str) -> str | None:
    for line in text.splitlines():
        cleaned = line.strip()

        if not cleaned:
            continue

        if (
            2 <= len(cleaned.split()) <= 4
            and "@" not in cleaned
            and not any(char.isdigit() for char in cleaned)
        ):
            return cleaned.title()

    return None


def extract_location(text: str) -> str | None:
    location_patterns = [
        r"Kolkata,\s*India",
        r"Bangalore,\s*India",
        r"Delhi,\s*India",
        r"Dubai,\s*UAE",
        r"Abu Dhabi,\s*UAE",
    ]

    for pattern in location_patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(0)

    return None


def extract_skills(text: str) -> list[str]:
    text_lower = text.lower()

    matches = [
        skill
        for skill in SKILL_KEYWORDS
        if skill.lower() in text_lower
    ]

    return sorted(set(matches))


def normalize_heading(line: str) -> str:
    return re.sub(r"[^a-z ]", "", line.lower()).strip()


def split_sections(text: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {
        "experience": [],
        "education": [],
        "projects": [],
        "certifications": [],
    }

    current_section: str | None = None

    for line in text.splitlines():
        cleaned = line.strip()

        if not cleaned:
            continue

        normalized = normalize_heading(cleaned)
        detected_section = None

        for section_name, headings in SECTION_NAMES.items():
            if normalized in headings:
                detected_section = section_name
                break

        if detected_section:
            current_section = detected_section
            continue

        if current_section:
            sections[current_section].append(cleaned)

    return sections


def build_candidate_profile(text: str) -> CandidateProfile:
    sections = split_sections(text)

    return CandidateProfile(
        name=extract_name(text),
        email=extract_email(text),
        phone=extract_phone(text),
        location=extract_location(text),
        skills=extract_skills(text),
        education=sections["education"],
        experience=sections["experience"],
        projects=sections["projects"],
        certifications=sections["certifications"],
        raw_text=text,
    )