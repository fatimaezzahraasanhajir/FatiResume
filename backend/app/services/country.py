from __future__ import annotations

from dataclasses import dataclass

from app.api.schemas import Country


@dataclass(frozen=True)
class CountryWeights:
    similarity: float
    skills: float
    experience: float
    education: float


COUNTRY_WEIGHTS: dict[Country, CountryWeights] = {
    Country.US: CountryWeights(similarity=0.45, skills=0.35, experience=0.15, education=0.05),
    Country.FR: CountryWeights(similarity=0.40, skills=0.25, experience=0.15, education=0.20),
    Country.DE: CountryWeights(similarity=0.40, skills=0.25, experience=0.15, education=0.20),
    Country.UK: CountryWeights(similarity=0.42, skills=0.30, experience=0.18, education=0.10),
}


def get_country_weights(country: Country) -> CountryWeights:
    return COUNTRY_WEIGHTS.get(country, COUNTRY_WEIGHTS[Country.US])
