import logging

from fastapi import (
    APIRouter,
    HTTPException
)

from app.models.recommendation_models import (
    RecommendationRequest,
    RecommendationResponse
)

from app.services.jansahayak import (
    JanSahayak
)


logger = logging.getLogger(
    __name__
)


router = APIRouter(
    prefix="/api",
    tags=["JanSahayak"]
)


# Load AI once instead of for every request
assistant = JanSahayak()


@router.post(
    "/recommendations",
    response_model=RecommendationResponse
)
def get_recommendations(
    request: RecommendationRequest
):

    try:

        profile = (
            request.profile.model_dump(
                exclude_none=True
            )
        )

        results = assistant.find_schemes(
            query=request.query,
            profile=profile,
            top_k=request.top_k
        )

        return {
            "status": "success",

            "query": request.query,

            "total_recommendations":
                len(results),

            "recommendations":
                results
        }

    except Exception as error:

        logger.exception(
            "JanSahayak recommendation error"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to process the "
                "recommendation request."
            )
        ) from error