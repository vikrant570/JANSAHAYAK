from fastapi import APIRouter

from app.services.eligibility import (
    EligibilityEngine
)


router = APIRouter(
    prefix="/api/v1",
    tags=["Eligibility"]
)


engine = EligibilityEngine()


@router.post(
    "/eligibility/check"
)
def check_eligibility(
    user: dict,
    scheme: dict
):

    result = engine.check(
        user,
        scheme
    )

    return {
        "eligibility": result
    }