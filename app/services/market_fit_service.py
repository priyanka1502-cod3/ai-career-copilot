from app.models.job import ParsedJobDescription
from app.models.market import CandidateMarketProfile, MarketFitResult, TargetCountry


def _clamp(score: float) -> float:
    return max(0.0, min(score, 100.0))


def calculate_market_fit(
    candidate: CandidateMarketProfile,
    job: ParsedJobDescription,
) -> MarketFitResult:
    warnings: list[str] = []

    location_score = 50.0
    visa_score = 50.0
    availability_score = 50.0
    salary_score = None

    job_location = (job.location or "").lower()
    visa_text = (job.visa_information or "").lower()

    country_keywords = {
        TargetCountry.UAE: ["uae", "dubai", "abu dhabi", "sharjah"],
        TargetCountry.UK: ["uk", "united kingdom", "london", "manchester", "birmingham"],
        TargetCountry.SINGAPORE: ["singapore"],
        TargetCountry.INDIA: ["india", "bengaluru", "bangalore", "hyderabad", "pune"],
    }

    keywords = country_keywords[candidate.target_country]

    if any(keyword in job_location for keyword in keywords):
        location_score = 100.0
    elif candidate.willing_to_relocate:
        location_score = 75.0
        warnings.append("Relocation may be required.")
    else:
        location_score = 25.0
        warnings.append("Job location may not match the candidate's preferences.")

    if "no sponsorship" in visa_text or "cannot sponsor" in visa_text:
        if candidate.requires_sponsorship:
            visa_score = 0.0
            warnings.append("Employer appears not to provide visa sponsorship.")
        else:
            visa_score = 100.0

    elif "sponsorship" in visa_text:
        visa_score = 80.0 if candidate.requires_sponsorship else 100.0

    elif candidate.requires_sponsorship:
        visa_score = 40.0
        warnings.append("Visa sponsorship availability is unclear.")

    else:
        visa_score = 90.0

    if candidate.notice_period_days is None:
        availability_score = 60.0

    elif candidate.notice_period_days <= 30:
        availability_score = 100.0

    elif candidate.notice_period_days <= 60:
        availability_score = 70.0
        warnings.append("The notice period may be longer than the employer prefers.")

    else:
        availability_score = 40.0
        warnings.append("A long notice period may reduce interview chances.")

    return MarketFitResult(
        target_country=candidate.target_country,
        location_score=_clamp(location_score),
        visa_score=_clamp(visa_score),
        availability_score=_clamp(availability_score),
        salary_score=salary_score,
        warnings=warnings,
    )