from fastapi import APIRouter

from pydantic import BaseModel

from app.connectors.india_gov import (
    IndiaGovConnector
)

from app.connectors.myscheme import (
    MySchemeConnector
)

from app.services.scheme_pipeline import (
    SchemePipeline
)

from app.services.jansahayak import (
    JanSahayakService
)


router = APIRouter(
    prefix="/analyze",
    tags=["Analysis"]
)


class AnalyzeRequest(
    BaseModel
):

    query: str


def get_service():

    connectors = [

        IndiaGovConnector(),

        MySchemeConnector()

    ]

    pipeline = SchemePipeline(
        connectors
    )

    return JanSahayakService(
        pipeline
    )


@router.post("")
def analyze(
    request: AnalyzeRequest
):

    service = get_service()

    return service.process(
        request.query
    )