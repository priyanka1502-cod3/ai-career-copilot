from fastapi import FastAPI

from app.api.resume import router as resume_router
from app.api.matching import router as matching_router

app = FastAPI(
    title="CareerCopilot AI",
    description="Your AI-powered career operating system",
    version="0.3.0",
)

app.include_router(resume_router)
app.include_router(matching_router)


@app.get("/")
async def root():
    return {
        "project": "CareerCopilot AI",
        "status": "Running 🚀",
        "version": "0.3.0",
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}