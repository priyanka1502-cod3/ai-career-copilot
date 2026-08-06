from fastapi import APIRouter, Form, HTTPException

from app.models.job import ParsedJobDescription
from app.services.job_parser_service import parse_job_description


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


@router.post(
    "/parse",
    response_model=ParsedJobDescription,
    summary="Parse pasted job description",
)
def parse_job(
    text: str = Form(..., min_length=30),
) -> ParsedJobDescription:
    try:
        return parse_job_description(text)

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to parse job description: {exc}",
        ) from exc