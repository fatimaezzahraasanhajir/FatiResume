from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.api.schemas import AnalyzeResponse, Country, EvidenceItem, JobsResponse, JobsResponseItem
from app.services.bias import build_bias_report
from app.services.jobs import build_job_query, find_jobs
from app.services.parsing import parse_resume
from app.services.scoring import analyze_resume

router = APIRouter()


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(
    job_description: str = Form(...),
    country: Country = Form(...),
    resume_text: Optional[str] = Form(None),
    resume_file: Optional[UploadFile] = File(None),
) -> AnalyzeResponse:
    file_bytes: Optional[bytes] = None
    filename: Optional[str] = None
    if resume_file is not None:
        filename = resume_file.filename
        file_bytes = await resume_file.read()

    try:
        parsed_resume = parse_resume(resume_text=resume_text, filename=filename, file_bytes=file_bytes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not parsed_resume.strip():
        raise HTTPException(
            status_code=400,
            detail="No resume content found. Paste resume text or upload a PDF/DOCX.",
        )

    result = analyze_resume(resume_text=parsed_resume, job_description=job_description, country=country)
    bias_report = build_bias_report(parsed_resume + "\n" + job_description)

    resume_source = "text" if (resume_text and resume_text.strip()) else "file" if resume_file else "none"

    return AnalyzeResponse(
        match_score=result["match_score"],
        confidence=result["confidence"],
        top_matches=result["top_matches"],
        missing_skills=result["missing_skills"],
        evidence=result["evidence"],
        bias_report=bias_report,
        country_breakdown=result["country_breakdown"],
    )


@router.post("/jobs", response_model=JobsResponse)
async def jobs(
    query: Optional[str] = Form(None),
    resume_text: Optional[str] = Form(None),
    resume_file: Optional[UploadFile] = File(None),
) -> JobsResponse:
    file_bytes: Optional[bytes] = None
    filename: Optional[str] = None
    if resume_file is not None:
        filename = resume_file.filename
        file_bytes = await resume_file.read()

    try:
        parsed_resume = parse_resume(resume_text=resume_text, filename=filename, file_bytes=file_bytes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not parsed_resume.strip():
        raise HTTPException(
            status_code=400,
            detail="No resume content found. Paste resume text or upload a PDF/DOCX.",
        )

    q = build_job_query(resume_text=parsed_resume, query=query)
    results = find_jobs(resume_text=parsed_resume, query=q, top_k=10)

    return JobsResponse(
        query=q,
        results=[
            JobsResponseItem(
                title=r.get("title", ""),
                company=r.get("company", ""),
                location=r.get("location", ""),
                url=r.get("url", ""),
                source=r.get("source", ""),
                score=r.get("score", 0.0),
            )
            for r in results
        ],
    )
