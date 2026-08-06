from fastapi import FastAPI

from app.api.analysis import router as analysis_router
from app.api.career import router as career_router
from app.api.country_scoring import router as country_scoring_router
from app.api.jobs import router as job_router
from app.api.market import router as market_router
from app.api.matching import router as matching_router
from app.api.resume import router as resume_router
from app.api.scoring import router as scoring_router


app = FastAPI(
    title="CareerCopilot AI",
    version="0.9.0",
    description=(
        "AI-powered resume parsing, job parsing, matching, market-fit analysis, "
        "resume scoring, country-specific evaluation, and unified career analysis."
    ),
)


app.include_router(resume_router)
app.include_router(job_router)
app.include_router(matching_router)
app.include_router(market_router)
app.include_router(analysis_router)
app.include_router(scoring_router)
app.include_router(country_scoring_router)
app.include_router(career_router)


@app.get("/", tags=["System"])
def root():
    return {
        "project": "CareerCopilot AI",
        "status": "Running",
        "version": "0.9.0",
    }


@app.get("/health", tags=["System"])
def health():
    return {
        "status": "healthy",
        "version": "0.9.0",
    }