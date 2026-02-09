from __future__ import annotations

import re
from dataclasses import dataclass
from functools import lru_cache
from typing import List, Tuple

import numpy as np

from app.api.schemas import Country, EvidenceItem, BiasReport, BiasFlag
from app.services.country import CountryWeights, get_country_weights
from app.services.bias import build_bias_report


@lru_cache(maxsize=1)
def get_embedding_model():
    """Simple model that doesn't require downloads"""
    class SimpleModel:
        def encode(self, texts, normalize_embeddings=True):
            # Simple keyword-based embedding
            embeddings = []
            for text in texts:
                # Convert text to simple feature vector
                text_lower = text.lower()
                features = []
                
                # Common tech keywords
                keywords = ['python', 'java', 'javascript', 'sql', 'aws', 'azure', 'gcp', 
                           'docker', 'kubernetes', 'tensorflow', 'pytorch', 'sklearn',
                           'machine learning', 'deep learning', 'nlp', 'computer vision',
                           'data science', 'analytics', 'statistics', 'algorithms',
                           'react', 'nodejs', 'mongodb', 'postgresql', 'mysql']
                
                for keyword in keywords:
                    features.append(1.0 if keyword in text_lower else 0.0)
                
                # Add some text-based features
                features.extend([
                    len(text) / 1000.0,  # Text length
                    text_lower.count('experience') / 10.0,
                    text_lower.count('project') / 10.0,
                    text_lower.count('skill') / 10.0,
                ])
                
                # Pad to fixed size
                while len(features) < 64:
                    features.append(0.0)
                features = features[:64]
                
                embeddings.append(features)
            
            result = np.array(embeddings)
            if normalize_embeddings:
                norms = np.linalg.norm(result, axis=1, keepdims=True)
                result = result / (norms + 1e-8)
            return result
    
    return SimpleModel()


def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


def split_sentences(text: str) -> List[str]:
    parts = re.split(r"(?<=[.!?])\s+|\n+", text)
    parts = [p.strip() for p in parts if p and p.strip()]
    return parts


def extract_skills(text: str) -> List[str]:
    # Simple skill extraction based on common keywords
    text_lower = text.lower()
    skills = []
    
    skill_keywords = [
        'python', 'java', 'javascript', 'sql', 'aws', 'azure', 'gcp', 
        'docker', 'kubernetes', 'tensorflow', 'pytorch', 'sklearn',
        'machine learning', 'deep learning', 'nlp', 'computer vision',
        'data science', 'analytics', 'statistics', 'algorithms',
        'react', 'nodejs', 'mongodb', 'postgresql', 'mysql',
        'excel', 'tableau', 'power bi', 'git', 'linux', 'ci/cd'
    ]
    
    for skill in skill_keywords:
        if skill in text_lower:
            skills.append(skill)
    
    return skills[:10]  # Return top 10 skills


@dataclass
class ScoreResult:
    score: float
    confidence: float
    evidence: List[dict]
    top_matches: List[str]
    missing_skills: List[str]


def score_resume(resume_text: str, job_description: str, country: Country) -> ScoreResult:
    """Simple scoring without heavy ML models"""
    model = get_embedding_model()
    
    # Get embeddings
    resume_emb = model.encode([resume_text], normalize_embeddings=True)[0]
    job_emb = model.encode([job_description], normalize_embeddings=True)[0]
    
    # Calculate similarity
    similarity = cosine_sim(resume_emb, job_emb)
    
    # Extract skills
    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_description))
    
    # Calculate skill match
    if job_skills:
        skill_match = len(resume_skills & job_skills) / len(job_skills)
    else:
        skill_match = 0.0
    
    # Calculate experience match (simple heuristic)
    exp_match = min(1.0, resume_text.lower().count('experience') / 10.0)
    
    # Get country weights
    weights = get_country_weights(country)
    
    # Calculate final score
    final_score = (
        similarity * weights.similarity +
        skill_match * weights.skills +
        exp_match * weights.experience
    ) * 100
    
    # Generate evidence
    evidence = []
    resume_sentences = split_sentences(resume_text)[:5]
    job_sentences = split_sentences(job_description)[:5]
    
    for i, (r_sent, j_sent) in enumerate(zip(resume_sentences, job_sentences)):
        r_emb = model.encode([r_sent], normalize_embeddings=True)[0]
        j_emb = model.encode([j_sent], normalize_embeddings=True)[0]
        sent_sim = cosine_sim(r_emb, j_emb)
        
        if sent_sim > 0.3:  # Threshold for evidence
            evidence.append({
                "text": r_sent,
                "score": sent_sim
            })
    
    # Find top matches and missing skills
    top_matches = list(resume_skills & job_skills)[:5]
    missing_skills = list(job_skills - resume_skills)[:5]
    
    return ScoreResult(
        score=min(100.0, max(0.0, final_score)),
        confidence=similarity,
        evidence=evidence,
        top_matches=top_matches,
        missing_skills=missing_skills
    )


def analyze_resume(resume_text: str, job_description: str, country: Country) -> dict:
    """Main analysis function that matches the API expectations"""
    # Score the resume
    result = score_resume(resume_text, job_description, country)
    
    # Analyze bias
    bias_analysis = build_bias_report(resume_text)
    
    # Build response in expected format
    return {
        "match_score": result.score,
        "confidence": result.confidence,
        "top_matches": result.top_matches,
        "missing_skills": result.missing_skills,
        "evidence": [EvidenceItem(text=ev["text"], score=ev["score"]) for ev in result.evidence],
        "bias_report": bias_analysis,
        "country_breakdown": {
            "country": country.value,
            "weights": get_country_weights(country).__dict__,
            "similarity": result.confidence,
            "resume_source": "text"
        }
    }
