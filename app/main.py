from fastapi import FastAPI

app = FastAPI(
    title="CareerCopilot AI",
    description="Your AI-powered career operating system",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {
        "project": "CareerCopilot AI",
        "status": "Running 🚀",
        "version": "0.1.0"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }