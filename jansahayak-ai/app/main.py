from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv

from app.config import get_settings

from app.api.routes_analyze import (
    router as analyze_router
)

from app.api.routes_schemes import (
    router as schemes_router
)

from app.api.routes_documents import (
    router as documents_router
)

from app.api.routes_eligibility import (
    router as eligibility_router
)

from app.models.recommendation_models import (
    RecommendationRequest,
    ChatResponse
)

from app.services.jansahayak import (
    JanSahayak
)

from app.services.response_formatter import (
    ResponseFormatter
)
from app.services.intent_router import IntentRouter



# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# SETTINGS
# ============================================================

settings = get_settings()


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "AI service for JanSahayak - civic empowerment "
        "and public-good assistance."
    )
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=settings.cors_origins,

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ============================================================
# LOAD JANSAHAYAK AI
# ============================================================

# Load the AI only once when FastAPI starts.
# This avoids loading the RAG / embedding system again
# for every request.

assistant = JanSahayak()


# ============================================================
# RESPONSE FORMATTER
# ============================================================

# Converts JanSahayak's structured JSON results
# into one human-readable Markdown string.

response_formatter = ResponseFormatter()

intent_router = IntentRouter()
# ============================================================
# ROOT
# ============================================================

@app.get("/")
async def root():

    return {
        "service": "jansahayak-ai",
        "status": "running",
        "version": settings.app_version
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/api/v1/health")
async def health():

    return {
        "status": "healthy",
        "service": "jansahayak-ai",
        "version": settings.app_version
    }


# ============================================================
# STRUCTURED RECOMMENDATION ENDPOINT
# ============================================================
#
# This endpoint returns complete JSON.
#
# It can be useful for:
# - debugging
# - future mobile apps
# - admin dashboards
# - structured frontend cards
#
# Your teammate does NOT necessarily need to use this endpoint
# for the chat interface.
# ============================================================

@app.post("/api/v1/recommendations")
async def recommendations(
    request: RecommendationRequest
):

    try:

        # ----------------------------------------------------
        # Convert Pydantic profile into normal Python dict
        # ----------------------------------------------------

        profile = request.profile.model_dump(
            exclude_none=True
        )

        # ----------------------------------------------------
        # Run complete JanSahayak AI pipeline
        #
        # Includes:
        # - query understanding
        # - spelling / intent handling
        # - RAG retrieval
        # - eligibility
        # - ranking
        # - explanation
        # - document checklist
        # ----------------------------------------------------

        results = assistant.find_schemes(
            query=request.query,
            profile=profile,
            top_k=request.top_k
        )

        # ----------------------------------------------------
        # Structured JSON response
        # ----------------------------------------------------

        return {

            "status": "success",

            "query": request.query,

            "total_recommendations":
                len(results),

            "recommendations":
                results
        }

    except Exception as error:

        print(
            "JANSAHAYAK RECOMMENDATION ERROR:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to process the "
                "JanSahayak recommendation request."
            )
        ) from error


# ============================================================
# CHAT / MARKDOWN ENDPOINT
# ============================================================
#
# THIS is the endpoint your React / Next.js teammate
# should normally use.
#
# Instead of returning complicated nested JSON such as:
#
# recommendations
#   -> scheme
#   -> documents
#   -> eligibility
#   -> explanation
#
# this endpoint converts everything into ONE Markdown string.
#
# Frontend only needs:
#
# data.answer
#
# ============================================================

@app.post(
    "/api/v1/chat",
    response_model=ChatResponse
)
async def chat(
    request: RecommendationRequest
):

    try:

        # ----------------------------------------------------
        # Detect user intent first
        # ----------------------------------------------------

        intent = intent_router.detect_intent(
            request.query
        )

        print(
            "Detected intent:",
            intent
        )

        # ----------------------------------------------------
        # Handle greeting / gratitude / unrelated questions
        # WITHOUT running FAISS or JanSahayak AI
        # ----------------------------------------------------

        if intent != "scheme_query":

            answer = intent_router.get_response(
                intent
            )

            return {

                "status": "success",

                "answer": answer
            }

        # ----------------------------------------------------
        # Convert citizen profile into normal Python dictionary
        # ----------------------------------------------------

        profile = request.profile.model_dump(
            exclude_none=True
        )

        # ----------------------------------------------------
        # Run JanSahayak AI only for scheme-related queries
        # ----------------------------------------------------

        results = assistant.find_schemes(
            query=request.query,
            profile=profile,
            top_k=request.top_k
        )

        # ----------------------------------------------------
        # Convert structured result into Markdown
        # ----------------------------------------------------

        answer = (
            response_formatter
            .format_recommendations(
                query=request.query,
                results=results
            )
        )

        # ----------------------------------------------------
        # SIMPLE RESPONSE FOR FRONTEND
        # ----------------------------------------------------

        return {

            "status": "success",

            "answer": answer
        }

    except Exception as error:

        print(
            "JANSAHAYAK CHAT ERROR:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to process the "
                "JanSahayak chat request."
            )
        ) from error

# ============================================================
# EXISTING ROUTERS
# ============================================================

app.include_router(
    analyze_router
)

app.include_router(
    schemes_router
)

app.include_router(
    documents_router
)

app.include_router(
    eligibility_router
)