from typing import Any, Optional

from pydantic import BaseModel


class Source(BaseModel):
    source_name: str
    source_url: str
    last_verified: str
    confidence: float


class EligibilityResult(BaseModel):
    scheme_id: str
    status: str
    reasons: list[str] = []
    missing_information: list[str] = []


class AnalyzeResponse(BaseModel):
    request_id: str
    language: str
    intent: str
    domain: str

    user_understanding: dict[str, Any]

    recommendations: list[dict[str, Any]] = []
    eligibility: list[EligibilityResult] = []
    documents: list[dict[str, Any]] = []

    draft: Optional[dict[str, Any]] = None

    action_plan: list[dict[str, Any]] = []

    simple_explanation: str

    sources: list[Source] = []

    confidence: float
    needs_verification: bool