from fastapi import APIRouter
from app.services.retrieval import load_schemes

router = APIRouter(
    prefix="/api/v1",
    tags=["Schemes"]
)


@router.get("/schemes")
def get_schemes():

    schemes = load_schemes()

    return {
        "count": len(schemes),
        "schemes": schemes
    }