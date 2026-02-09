from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class Country(str, Enum):
    US = "US"
    FR = "FR"
    DE = "DE"
    UK = "UK"


class EvidenceItem(BaseModel):
    text: str
    score: float = Field(ge=0.0)


class BiasFlag(BaseModel):
    category: str
    term: str
    message: str


class BiasReport(BaseModel):
    risk_score: float = Field(ge=0.0, le=1.0)
    flags: List[BiasFlag] = Field(default_factory=list)


class AnalyzeResponse(BaseModel):
    match_score: float = Field(ge=0.0, le=100.0)
    confidence: float = Field(ge=0.0, le=1.0)
    top_matches: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    evidence: List[EvidenceItem] = Field(default_factory=list)
    bias_report: BiasReport
    country_breakdown: dict


class AnalyzeForm(BaseModel):
    resume_text: Optional[str] = None
    job_description: str
    country: Country


class JobsResponseItem(BaseModel):
    title: str
    company: str
    location: str
    url: str
    source: str
    score: float = Field(ge=0.0, le=1.0)


class JobsResponse(BaseModel):
    query: str
    results: List[JobsResponseItem] = Field(default_factory=list)
