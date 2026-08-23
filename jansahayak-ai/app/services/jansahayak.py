from typing import Any

from app.services.analyzer import JanSahayakAnalyzer
from app.services.document_checklist import DocumentChecklist


class JanSahayak:
    """
    Main JanSahayak AI service.

    Responsibilities:
    ----------------------------------------------------------
    1. Receive citizen query
    2. Send query/profile to JanSahayakAnalyzer
    3. Receive ranked schemes
    4. Run document checklist for every scheme
    5. Return frontend-friendly recommendation results

    The existing Analyzer continues handling:
    - RAG retrieval
    - eligibility
    - recommendation ranking
    - explanations

    This class adds:
    - verified document information
    - user's missing document information
    """

    def __init__(self):

        # Existing main AI analyzer
        self.analyzer = JanSahayakAnalyzer()

        # Document feature
        self.document_checklist = DocumentChecklist()

    # =========================================================
    # FIND SCHEMES
    # =========================================================

    def find_schemes(
        self,
        query: str,
        profile: dict | None = None,
        top_k: int = 5,
        user: dict | None = None
    ) -> list[dict]:

        """
        Returns frontend-friendly scheme recommendations.

        Parameters
        ----------
        query:
            Citizen's natural-language problem.

        profile:
            Citizen profile.

            Example:

            {
                "age": 21,
                "state": "Punjab",
                "occupation": "farmer",
                "income": 250000,

                "documents": [
                    "Aadhaar Card",
                    "Bank Passbook"
                ]
            }

        top_k:
            Number of scheme recommendations.

        user:
            Backward-compatible alias for profile.

        Returns
        -------
        list[dict]

        Example:

        [
            {
                "scheme": {...},
                "score": 0.75,
                "eligibility": {...},
                "documents": {...},
                "explanation": "..."
            }
        ]
        """

        # -----------------------------------------------------
        # PROFILE / USER COMPATIBILITY
        # -----------------------------------------------------

        if profile is None:

            profile = (
                user
                if isinstance(user, dict)
                else {}
            )

        if not isinstance(profile, dict):
            profile = {}

        query = str(
            query or ""
        ).strip()

        if not query:

            return []

        # -----------------------------------------------------
        # CALL EXISTING ANALYZER
        # -----------------------------------------------------

        analyzer_result = self._call_analyzer(
            query=query,
            profile=profile,
            top_k=top_k
        )

        # -----------------------------------------------------
        # GET RECOMMENDATION LIST
        # -----------------------------------------------------

        recommendations = (
            self._extract_recommendations(
                analyzer_result
            )
        )

        final_results = []

        # Citizen documents
        user_documents = profile.get(
            "documents",
            []
        )

        if not isinstance(
            user_documents,
            list
        ):
            user_documents = []

        # =====================================================
        # PROCESS EACH RECOMMENDATION
        # =====================================================

        for recommendation in recommendations:

            if not isinstance(
                recommendation,
                dict
            ):
                continue

            # -------------------------------------------------
            # SCHEME
            # -------------------------------------------------

            scheme = self._extract_scheme(
                recommendation
            )

            if not scheme:
                continue

            # -------------------------------------------------
            # ELIGIBILITY
            # -------------------------------------------------

            eligibility = recommendation.get(
                "eligibility",
                {}
            )

            if not isinstance(
                eligibility,
                dict
            ):
                eligibility = {}

            # -------------------------------------------------
            # SCORE
            # -------------------------------------------------

            score = self._extract_score(
                recommendation,
                scheme
            )

            # -------------------------------------------------
            # EXPLANATION
            # -------------------------------------------------

            explanation = recommendation.get(
                "explanation",
                ""
            )

            if explanation is None:
                explanation = ""

            # =================================================
            # DOCUMENT CHECKLIST
            # =================================================

            document_result = (
                self.document_checklist.generate(
                    scheme=scheme,
                    user_documents=user_documents
                )
            )

            # -------------------------------------------------
            # FINAL FRONTEND RESULT
            # -------------------------------------------------

            final_result = {

                "scheme":
                    scheme,

                "score":
                    score,

                "eligibility":
                    eligibility,

                "documents":
                    document_result,

                "explanation":
                    explanation
            }

            final_results.append(
                final_result
            )

        # -----------------------------------------------------
        # LIMIT RESULTS
        # -----------------------------------------------------

        return final_results[:top_k]

    # =========================================================
    # ANALYZE
    # =========================================================

    def analyze(
        self,
        query: str,
        profile: dict | None = None,
        top_k: int = 5,
        user: dict | None = None
    ) -> dict:

        """
        Returns a complete AI response.

        This method is useful later for FastAPI/frontend.
        """

        if profile is None:

            profile = (
                user
                if isinstance(user, dict)
                else {}
            )

        if not isinstance(profile, dict):
            profile = {}

        recommendations = self.find_schemes(
            query=query,
            profile=profile,
            top_k=top_k
        )

        return {

            "query":
                query,

            "profile":
                profile,

            "recommendations":
                recommendations,

            "total_recommendations":
                len(recommendations),

            "status":
                (
                    "success"
                    if recommendations
                    else "no_results"
                )
        }

    # =========================================================
    # CALL ANALYZER SAFELY
    # =========================================================

    def _call_analyzer(
        self,
        query: str,
        profile: dict,
        top_k: int
    ) -> Any:

        """
        Supports slightly different analyzer method signatures.

        This prevents the document integration from breaking
        your already-working analyzer.
        """

        # -----------------------------------------------------
        # Preferred signature
        # -----------------------------------------------------

        try:

            return self.analyzer.analyze(
                query=query,
                profile=profile,
                top_k=top_k
            )

        except TypeError:

            pass

        # -----------------------------------------------------
        # Older signature without top_k
        # -----------------------------------------------------

        try:

            return self.analyzer.analyze(
                query=query,
                profile=profile
            )

        except TypeError:

            pass

        # -----------------------------------------------------
        # Possible user= alias
        # -----------------------------------------------------

        try:

            return self.analyzer.analyze(
                query=query,
                user=profile,
                top_k=top_k
            )

        except TypeError:

            pass

        # -----------------------------------------------------
        # Last fallback
        # -----------------------------------------------------

        return self.analyzer.analyze(
            query,
            profile
        )

    # =========================================================
    # EXTRACT RECOMMENDATIONS
    # =========================================================

    @staticmethod
    def _extract_recommendations(
        analyzer_result: Any
    ) -> list:

        """
        Handles different analyzer output structures.
        """

        if analyzer_result is None:

            return []

        # -----------------------------------------------------
        # Analyzer directly returned a list
        # -----------------------------------------------------

        if isinstance(
            analyzer_result,
            list
        ):

            return analyzer_result

        # -----------------------------------------------------
        # Analyzer returned dictionary
        # -----------------------------------------------------

        if isinstance(
            analyzer_result,
            dict
        ):

            for key in [
                "recommendations",
                "results",
                "schemes",
                "matches"
            ]:

                value = analyzer_result.get(
                    key
                )

                if isinstance(
                    value,
                    list
                ):

                    return value

        return []

    # =========================================================
    # EXTRACT SCHEME
    # =========================================================

    @staticmethod
    def _extract_scheme(
        recommendation: dict
    ) -> dict:

        """
        Supports both:

        {
            "scheme": {...}
        }

        and recommendation objects where the scheme fields
        are directly inside the recommendation.
        """

        scheme = recommendation.get(
            "scheme"
        )

        if isinstance(
            scheme,
            dict
        ):

            return dict(
                scheme
            )

        # -----------------------------------------------------
        # Recommendation itself may be the scheme
        # -----------------------------------------------------

        if (
            "name" in recommendation
            and
            (
                "official_source"
                in recommendation
                or
                "description"
                in recommendation
            )
        ):

            return dict(
                recommendation
            )

        return {}

    # =========================================================
    # EXTRACT SCORE
    # =========================================================

    @staticmethod
    def _extract_score(
        recommendation: dict,
        scheme: dict
    ) -> float:

        """
        Supports score names used throughout JanSahayak.
        """

        candidates = [

            recommendation.get(
                "score"
            ),

            recommendation.get(
                "final_recommendation_score"
            ),

            recommendation.get(
                "recommendation_score"
            ),

            recommendation.get(
                "retrieval_score"
            ),

            scheme.get(
                "final_recommendation_score"
            ),

            scheme.get(
                "recommendation_score"
            ),

            scheme.get(
                "retrieval_score"
            )
        ]

        for value in candidates:

            if value is None:
                continue

            try:

                return float(
                    value
                )

            except (
                TypeError,
                ValueError
            ):

                continue

        return 0.0


# =============================================================
# BACKWARD-COMPATIBLE HELPER
# =============================================================

def ask_jansahayak(
    query: str,
    profile: dict | None = None,
    top_k: int = 5
):

    assistant = JanSahayak()

    return assistant.find_schemes(
        query=query,
        profile=profile,
        top_k=top_k
    )
# =============================================================
# BACKWARD COMPATIBILITY
# =============================================================

# Older API routes use the name JanSahayakService.
# The current implementation uses JanSahayak.
# Keep this alias so old routes continue to work.

JanSahayakService = JanSahayak