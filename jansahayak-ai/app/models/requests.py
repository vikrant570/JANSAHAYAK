from typing import Optional

from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    query: str = Field(..., min_length=2)
    language: Optional[str] = None

    age: Optional[int] = None
    location: Optional[str] = None
    occupation: Optional[str] = None
    income: Optional[float] = None
    education: Optional[str] = None

    user_type: Optional[str] = None


class EligibilityRequest(BaseModel):
    scheme_id: str

    age: Optional[int] = None
    location: Optional[str] = None
    occupation: Optional[str] = None
    income: Optional[float] = None
    education: Optional[str] = None


class DraftRequest(BaseModel):
    issue: str
    language: str = "en"
    user_information: dict = {}
    authority: Optional[str] = None
    document_context: Optional[str] = None


class ActionPlanRequest(BaseModel):
    issue: str
    recommendations: list = []
    documents: list = []
    language: str = "en"


class TranslateRequest(BaseModel):
    text: str
    target_language: str