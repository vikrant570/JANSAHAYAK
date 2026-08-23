from pydantic import BaseModel
from typing import Optional


class SourceReference(BaseModel):

    source_name: str

    source_url: str

    authority: str

    last_verified: str

    confidence: float


class SourceRecord(BaseModel):

    id: str

    name: str

    base_url: str

    type: str

    authority: str

    trust_level: int

    enabled: bool = True