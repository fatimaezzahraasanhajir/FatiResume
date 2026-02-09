from __future__ import annotations

from typing import Any, Dict, List, Optional

import requests

from app.services.scoring import cosine_sim, extract_skills, get_embedding_model


def _safe_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)


def _remotive_search(query: str, limit: int) -> List[Dict[str, Any]]:
    url = "https://remotive.com/api/remote-jobs"
    r = requests.get(url, params={"search": query}, timeout=30)
    r.raise_for_status()
    payload = r.json()
    jobs = payload.get("jobs", []) or []
    out: List[Dict[str, Any]] = []
    for j in jobs[: limit * 3]:
        out.append(
            {
                "source": "remotive",
                "title": _safe_text(j.get("title")),
                "company": _safe_text(j.get("company_name")),
                "location": _safe_text(j.get("candidate_required_location")),
                "url": _safe_text(j.get("url")),
                "description": _safe_text(j.get("description")),
            }
        )
    return out


def _arbeitnow_search(query: str, limit: int) -> List[Dict[str, Any]]:
    url = "https://www.arbeitnow.com/api/job-board-api"
    r = requests.get(url, params={"search": query}, timeout=30)
    r.raise_for_status()
    payload = r.json()
    jobs = payload.get("data", []) or []
    out: List[Dict[str, Any]] = []
    for j in jobs[: limit * 3]:
        out.append(
            {
                "source": "arbeitnow",
                "title": _safe_text(j.get("title")),
                "company": _safe_text(j.get("company_name")),
                "location": _safe_text(j.get("location")),
                "url": _safe_text(j.get("url")),
                "description": _safe_text(j.get("description")),
            }
        )
    return out


def build_job_query(resume_text: str, query: Optional[str]) -> str:
    if query and query.strip():
        return query.strip()
    skills = extract_skills(resume_text)
    if skills:
        return " ".join(skills[:5])
    return "machine learning"


def rank_jobs(resume_text: str, jobs: List[Dict[str, Any]], top_k: int) -> List[Dict[str, Any]]:
    model = get_embedding_model()
    resume_emb = model.encode([resume_text], normalize_embeddings=True)[0]

    texts = []
    for j in jobs:
        texts.append((j.get("title", "") + "\n" + j.get("description", ""))[:4000])

    if not texts:
        return []

    job_embs = model.encode(texts, normalize_embeddings=True)

    scored: List[Dict[str, Any]] = []
    for j, emb in zip(jobs, job_embs):
        score = cosine_sim(resume_emb, emb)
        j2 = dict(j)
        j2["score"] = float(max(0.0, min(1.0, score)))
        scored.append(j2)

    scored.sort(key=lambda x: x.get("score", 0.0), reverse=True)

    dedup: List[Dict[str, Any]] = []
    seen_urls = set()
    for j in scored:
        url = j.get("url")
        if not url or url in seen_urls:
            continue
        seen_urls.add(url)
        dedup.append(j)
        if len(dedup) >= top_k:
            break

    return dedup


def _backup_jobs(query: str, limit: int) -> List[Dict[str, Any]]:
    """Fallback job data with real working job search URLs"""
    backup_jobs = [
        {
            "source": "linkedin",
            "title": "Senior Data Scientist",
            "company": "Multiple Companies",
            "location": "United States / Remote",
            "url": "https://www.linkedin.com/jobs/search/?keywords=Senior%20Data%20Scientist&location=United%20States&f_TPR=r86400",
            "description": "Find real Senior Data Scientist positions on LinkedIn Jobs. Updated daily with thousands of listings."
        },
        {
            "source": "indeed",
            "title": "Machine Learning Engineer",
            "company": "Multiple Companies",
            "location": "United States / Remote",
            "url": "https://www.indeed.com/jobs?q=Machine+Learning+Engineer&l=United+States&fromage=1",
            "description": "Browse real Machine Learning Engineer jobs on Indeed. New positions posted hourly."
        },
        {
            "source": "glassdoor",
            "title": "Data Scientist",
            "company": "Multiple Companies",
            "location": "United States / Remote",
            "url": "https://www.glassdoor.com/Job/jobs.htm?sc.keyword=Data%20Scientist&locT=C&locId=1",
            "description": "Explore Data Scientist opportunities on Glassdoor with company reviews and salary insights."
        },
        {
            "source": "linkedin",
            "title": "AI Research Scientist",
            "company": "Multiple Companies",
            "location": "United States / Remote",
            "url": "https://www.linkedin.com/jobs/search/?keywords=AI%20Research%20Scientist&location=United%20States&f_TPR=r86400",
            "description": "Discover cutting-edge AI Research Scientist roles at top tech companies and research labs."
        },
        {
            "source": "indeed",
            "title": "Data Science Manager",
            "company": "Multiple Companies",
            "location": "United States / Remote",
            "url": "https://www.indeed.com/jobs?q=Data+Science+Manager&l=United+States&fromage=1",
            "description": "Find leadership positions in data science management with competitive salaries."
        },
        {
            "source": "built_in",
            "title": "Senior ML Engineer",
            "company": "Tech Startups",
            "location": "United States / Remote",
            "url": "https://www.builtinafrica.com/jobs?keywords=Senior%20ML%20Engineer",
            "description": "Explore ML Engineer positions at innovative tech startups and established companies."
        },
        {
            "source": "angel_list",
            "title": "Data Scientist - Remote",
            "company": "Startups & Remote Companies",
            "location": "Remote",
            "url": "https://angel.co/job-browser/data-scientist-remote-jobs",
            "description": "Find remote Data Scientist positions at startups and remote-first companies."
        },
        {
            "source": "hired",
            "title": "Data Analyst & Scientist",
            "company": "Top Tech Companies",
            "location": "United States / Remote",
            "url": "https://hired.com/jobs/data-scientist",
            "description": "Get matched with top companies looking for Data Analysts and Scientists."
        }
    ]
    return backup_jobs[:limit]


def find_jobs(resume_text: str, query: Optional[str], top_k: int = 10) -> List[Dict[str, Any]]:
    q = build_job_query(resume_text=resume_text, query=query)

    jobs: List[Dict[str, Any]] = []
    
    # Try external APIs but ensure we always have backup
    try:
        for fetch in (_remotive_search, _arbeitnow_search):
            try:
                external_jobs = fetch(q, limit=top_k)
                # Validate external jobs have required fields
                for job in external_jobs:
                    if all(key in job for key in ["title", "url", "description"]):
                        jobs.append(job)
            except Exception as e:
                print(f"External API failed: {e}")
                continue
    except Exception as e:
        print(f"All external APIs failed: {e}")

    # Always use backup data to ensure reliability
    if not jobs or len(jobs) < 3:
        print("Using backup job data for reliability")
        jobs = _backup_jobs(q, top_k)

    # Ensure all jobs have required fields
    valid_jobs = []
    for job in jobs:
        valid_job = {
            "title": job.get("title", "Data Scientist Position"),
            "company": job.get("company", "Tech Company"),
            "location": job.get("location", "Remote"),
            "url": job.get("url", "#"),
            "description": job.get("description", "Exciting opportunity in data science and machine learning."),
            "source": job.get("source", "job_board")
        }
        valid_jobs.append(valid_job)

    return rank_jobs(resume_text=resume_text, jobs=valid_jobs, top_k=top_k)
