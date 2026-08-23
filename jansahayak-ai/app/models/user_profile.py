from pydantic import BaseModel
from typing import Optional


class UserProfile(BaseModel):

    age: Optional[int] = None

    state: Optional[str] = None

    gender: Optional[str] = None

    occupation: Optional[str] = None

    education: Optional[str] = None

    annual_income: Optional[float] = None

    category: Optional[str] = None

    disability: Optional[bool] = None