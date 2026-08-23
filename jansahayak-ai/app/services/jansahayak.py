from typing import Any

from app.services.analyzer import JanSahayakAnalyzer
from app.services.document_checklist import DocumentChecklist
from app.services.relevance_filter import SchemeRelevanceFilter


class JanSahayak:
    """
    Main JanSahayak AI service.

    Responsibilities:
    ----------------------------------------------------------
    1. Receive citizen query
    2. Send query/profile to JanSahayakAnalyzer
    3. Receive ranked scheme candidates
    4. Improve domain relevance
    5. Run document checklist for every relevant scheme
    6. Return frontend-friendly recommendation results

    Existing Analyzer continues handling:
    - RAG retrieval
    - eligibility
    - recommendation ranking
    - explanations

    This class adds:
    - verified document information
    - user's missing document information
    - domain relevance filtering
    """

    def __init__(self):

        # =====================================================
        # EXISTING MAIN AI ANALYZER
        # =====================================================

        self.analyzer = JanSahayakAnalyzer()

        # =====================================================
        # EXISTING DOCUMENT FEATURE
        # =====================================================

        self.document_checklist = DocumentChecklist()

        # =====================================================
        # NEW RELEVANCE FILTER
        # =====================================================

        self.relevance_filter = SchemeRelevanceFilter()

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
            Number of final scheme recommendations.

            Important:
            Internally JanSahayak retrieves more candidates
            than top_k so that irrelevant FAISS results can
            be removed before returning the best schemes.

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
        # SAFE TOP_K
        # -----------------------------------------------------

        try:
            top_k = int(top_k)

        except (
            TypeError,
            ValueError
        ):
            top_k = 5

        top_k = max(
            1,
            top_k
        )

        # =====================================================
        # NEW: RETRIEVE MORE CANDIDATES
        # =====================================================
        #
        # Previously:
        #
        #     frontend asks for 3
        #           ↓
        #     analyzer returns only 3
        #
        # If those 3 contained:
        # - accident insurance
        # - scholarship
        # - unrelated women scheme
        #
        # then there was no agriculture scheme available
        # for us to choose.
        #
        # Now:
        #
        #     frontend asks for 3
        #           ↓
        #     analyzer retrieves about 15
        #           ↓
        #     relevance filter removes poor matches
        #           ↓
        #     best 3 returned
        #

        candidate_k = max(
            top_k * 10,
            30
        )

        # -----------------------------------------------------
        # CALL EXISTING ANALYZER
        # -----------------------------------------------------

        analyzer_result = self._call_analyzer(
            query=query,
            profile=profile,
            top_k=candidate_k
        )

        # -----------------------------------------------------
        # GET RECOMMENDATION LIST
        # -----------------------------------------------------

        recommendations = (
            self._extract_recommendations(
                analyzer_result
            )
        )

        if not recommendations:
            return []

        # =====================================================
        # PREPARE STANDARDIZED CANDIDATES
        # =====================================================
        #
        # We first convert analyzer recommendations into the
        # same structure used by the relevance filter.
        #
        # We deliberately do this BEFORE document checklist
        # generation so document processing is only run for
        # relevant schemes.
        #

        relevance_candidates = []

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

            relevance_candidates.append(
                {
                    "scheme": scheme,
                    "score": score,
                    "eligibility": eligibility,
                    "explanation": explanation
                }
            )

        if not relevance_candidates:
            return []

        # =====================================================
        # NEW: DOMAIN RELEVANCE FILTER / RERANKING
        # =====================================================

        relevant_results = (
            self.relevance_filter.rerank(
                query=query,
                profile=profile,
                results=relevance_candidates,
                top_k=top_k
            )
        )

        if not relevant_results:
            return []

        # =====================================================
        # CITIZEN DOCUMENTS
        # =====================================================

        user_documents = profile.get(
            "documents",
            []
        )

        if not isinstance(
            user_documents,
            list
        ):
            user_documents = []

        final_results = []

        # =====================================================
        # PROCESS ONLY RELEVANT RECOMMENDATIONS
        # =====================================================

        for recommendation in relevant_results:

            if not isinstance(
                recommendation,
                dict
            ):
                continue

            # -------------------------------------------------
            # SCHEME
            # -------------------------------------------------

            scheme = recommendation.get(
                "scheme",
                {}
            )

            if not isinstance(
                scheme,
                dict
            ):
                continue

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

            score = recommendation.get(
                "score",
                0.0
            )

            try:

                score = float(
                    score
                )

            except (
                TypeError,
                ValueError
            ):

                score = 0.0

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
            # EXISTING DOCUMENT CHECKLIST
            # =================================================

            document_result = (
                self.document_checklist.generate(
                    scheme=scheme,
                    user_documents=user_documents
                )
            )

            # =================================================
            # FINAL FRONTEND RESULT
            # =================================================
            #
            # Keep exactly the same frontend structure:
            #
            # scheme
            # score
            # eligibility
            # documents
            # explanation
            #

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

        # =====================================================
        # FINAL LIMIT
        # =====================================================

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

        Useful for FastAPI/frontend and backwards compatibility.
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

        This keeps the existing analyzer compatibility.
        """

        # -----------------------------------------------------
        # PREFERRED SIGNATURE
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
        # OLDER SIGNATURE WITHOUT TOP_K
        # -----------------------------------------------------

        try:

            return self.analyzer.analyze(
                query=query,
                profile=profile
            )

        except TypeError:
            pass

        # -----------------------------------------------------
        # POSSIBLE USER= ALIAS
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
        # LAST FALLBACK
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
        # ANALYZER DIRECTLY RETURNED A LIST
        # -----------------------------------------------------

        if isinstance(
            analyzer_result,
            list
        ):

            return analyzer_result

        # -----------------------------------------------------
        # ANALYZER RETURNED DICTIONARY
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
        # RECOMMENDATION ITSELF MAY BE THE SCHEME
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