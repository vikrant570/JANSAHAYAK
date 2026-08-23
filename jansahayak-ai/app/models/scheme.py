from pydantic import BaseModel, Field
from typing import Optional


class SchemeEligibility(BaseModel):

    age_min: Optional[int] = None

    age_max: Optional[int] = None

    income_max: Optional[float] = None

    occupation: list[str] = Field(
        default_factory=list
    )

    education: list[str] = Field(
        default_factory=list
    )

    other_conditions: list[str] = Field(
        default_factory=list
    )


class Scheme(BaseModel):

    id: str

    name: str

    category: str

    description: str

    target_users: list[str]

    states: list[str]

    eligibility: SchemeEligibility

    benefits: list[str]

    documents: list[str]

    application_steps: list[str]

    official_source: str

    source_name: str

    authority: str

    last_verified: str

    verification_status: str = "verified"

    confidence: float = 0.0