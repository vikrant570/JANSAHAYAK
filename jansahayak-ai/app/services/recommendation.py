from app.services.query_analyzer import (
    QueryAnalyzer
)
from app.services.eligibility import (
    EligibilityEngine
)

class SchemeRecommendationEngine:

    def __init__(self, pipeline):

        self.pipeline = pipeline

        self.analyzer = (
            QueryAnalyzer()
        )
        self.eligibility = (
            EligibilityEngine()
        )

    def recommend(
        self,
        query: str
    ) -> dict:

        profile = (
            self.analyzer.analyze(
                query
            )
        )

        search_query = self._build_search_query(
            profile
        )

        schemes = self.pipeline.search(
            search_query
        )

        schemes = self._filter_by_state(
            schemes,
            profile.get("state")
        )

        schemes = self._rank(
            schemes,
            profile
        )
        for scheme in schemes:

            scheme[
                "eligibility_result"
            ] = self.eligibility.check(
                scheme,
                profile
            )

        return {
            "query": query,
            "profile": profile,
            "schemes": schemes
        }

    def _build_search_query(
        self,
        profile: dict
    ) -> str:

        parts = []

        if profile.get("intent"):
            parts.append(
                profile["intent"]
            )

        if profile.get("occupation"):
            parts.append(
                profile["occupation"]
            )

        return " ".join(parts)

    def _filter_by_state(
        self,
        schemes,
        state
    ):

        if not state:

            return schemes

        matching = []

        for scheme in schemes:

            states = scheme.get(
                "states",
                []
            )

            if not states:

                matching.append(
                    scheme
                )

                continue

            normalized_states = [
                str(s).lower()
                for s in states
            ]

            if (
                "all" in normalized_states
                or
                state.lower()
                in normalized_states
            ):

                matching.append(
                    scheme
                )

        return matching

    def _rank(
        self,
        schemes,
        profile
    ):

        scored = []

        for scheme in schemes:

            score = 0.0

            name = (
                scheme.get(
                    "name"
                ) or ""
            ).lower()

            description = (
                scheme.get(
                    "description"
                ) or ""
            ).lower()

            category = (
                scheme.get(
                    "category"
                ) or ""
            ).lower()

            intent = (
                profile.get(
                    "intent"
                ) or ""
            ).lower()

            occupation = (
                profile.get(
                    "occupation"
                ) or ""
            ).lower()

            # Intent match
            if intent in name:
                score += 0.40

            if intent in category:
                score += 0.25

            if intent in description:
                score += 0.15

            # Occupation match
            if occupation:

                if occupation in name:
                    score += 0.10

                if occupation in description:
                    score += 0.10

            # Source confidence
            score += (
                scheme.get(
                    "confidence",
                    0
                ) * 0.10
            )

            scheme_copy = dict(
                scheme
            )

            scheme_copy[
                "relevance_score"
            ] = round(
                score,
                4
            )

            scored.append(
                scheme_copy
            )

        scored.sort(
            key=lambda x:
                x.get(
                    "relevance_score",
                    0
                ),
            reverse=True
        )

        return scored