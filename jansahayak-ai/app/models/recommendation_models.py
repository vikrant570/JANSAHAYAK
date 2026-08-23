from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class CitizenProfile(BaseModel):

    age: int | None = None

    state: str | None = None

    occupation: str | None = None

    income: float | None = None

    documents: list[str] = Field(
        default_factory=list
    )

    # Allows future fields such as:
    # gender, category, education, disability, etc.
    model_config = ConfigDict(
        extra="allow"
    )


class RecommendationRequest(BaseModel):

    query: str = Field(
        ...,
        min_length=2
    )

    profile: CitizenProfile = Field(
        default_factory=CitizenProfile
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=10
    )


class RecommendationResponse(BaseModel):

    status: str

    query: str

    total_recommendations: int

    recommendations: list[
        dict[str, Any]
    ]
class ChatResponse(BaseModel):

    status: str

    answer: str