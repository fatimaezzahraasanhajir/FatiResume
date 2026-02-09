from __future__ import annotations

import re
from typing import Iterable, List

from app.api.schemas import BiasFlag, BiasReport


_GENDER_CODED = {
    "aggressive": "Consider more neutral wording.",
    "ninja": "Consider more neutral wording.",
    "rockstar": "Consider more neutral wording.",
    "dominant": "Consider more neutral wording.",
}

_AGE_CODED = {
    "young": "Avoid age-related wording.",
    "energetic": "Avoid age-related wording.",
    "digital native": "Avoid age-related wording.",
}

_NATIONALITY_CODED = {
    "native": "Be careful with nationality/citizenship implications.",
    "citizenship": "Be careful with nationality/citizenship implications.",
}

_EDUCATION_PRESTIGE = {
    "ivy league": "Education prestige may introduce bias.",
    "oxford": "Education prestige may introduce bias.",
    "cambridge": "Education prestige may introduce bias.",
}


def _find_terms(text: str, terms: Iterable[str]) -> List[str]:
    found: List[str] = []
    lowered = text.lower()
    for term in terms:
        if re.search(r"\b" + re.escape(term) + r"\b", lowered):
            found.append(term)
    return found


def build_bias_report(text: str) -> BiasReport:
    flags: List[BiasFlag] = []

    for term in _find_terms(text, _GENDER_CODED.keys()):
        flags.append(BiasFlag(category="gendered_wording", term=term, message=_GENDER_CODED[term]))

    for term in _find_terms(text, _AGE_CODED.keys()):
        flags.append(BiasFlag(category="age_wording", term=term, message=_AGE_CODED[term]))

    for term in _find_terms(text, _NATIONALITY_CODED.keys()):
        flags.append(BiasFlag(category="nationality_wording", term=term, message=_NATIONALITY_CODED[term]))

    for term in _find_terms(text, _EDUCATION_PRESTIGE.keys()):
        flags.append(BiasFlag(category="education_prestige", term=term, message=_EDUCATION_PRESTIGE[term]))

    risk_score = min(1.0, 0.1 + 0.08 * len(flags)) if flags else 0.05

    return BiasReport(risk_score=risk_score, flags=flags)
