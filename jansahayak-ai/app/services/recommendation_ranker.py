class RecommendationRanker:
    """
    Ranks government schemes using:
    - semantic relevance
    - eligibility
    - state relevance
    - occupation relevance
    - source confidence
    """

    def __init__(self):
        pass

    def _state_score(self, scheme, profile):
        user_state = str(
            profile.get("state", "")
        ).strip().lower()

        if not user_state:
            return 0.0

        states = [
            str(x).strip().lower()
            for x in scheme.get("states", [])
        ]

        if not states:
            return 0.0

        if "all" in states:
            return 0.7

        if user_state in states:
            return 1.0

        return 0.0

    def _occupation_score(self, scheme, profile):
        occupation = str(
            profile.get("occupation", "")
        ).strip().lower()

        if not occupation:
            return 0.0

        eligibility = scheme.get(
            "eligibility",
            {}
        ) or {}

        occupations = [
            str(x).strip().lower()
            for x in eligibility.get(
                "occupation",
                []
            )
        ]

        target_users = [
            str(x).strip().lower()
            for x in scheme.get(
                "target_users",
                []
            )
        ]

        if occupation in occupations:
            return 1.0

        if occupation in target_users:
            return 1.0

        # Useful keyword matching
        if occupation == "farmer":
            agriculture_words = {
                "farmer",
                "agriculture",
                "agricultural",
                "cultivator"
            }

            scheme_text = " ".join([
                scheme.get("name", ""),
                scheme.get("description", ""),
                scheme.get("category", ""),
                " ".join(
                    scheme.get("tags", [])
                )
            ]).lower()

            if any(
                word in scheme_text
                for word in agriculture_words
            ):
                return 0.8

        return 0.0

    def calculate_score(
        self,
        scheme,
        eligibility_score=0.0,
        profile=None
    ):
        profile = profile or {}

        retrieval_score = float(
            scheme.get(
                "retrieval_score",
                0.0
            )
        )

        confidence = float(
            scheme.get(
                "confidence",
                0.0
            )
        )

        state_score = self._state_score(
            scheme,
            profile
        )

        occupation_score = self._occupation_score(
            scheme,
            profile
        )

        retrieval_component = max(
            0.0,
            min(1.0, retrieval_score)
        )

        eligibility_component = max(
            0.0,
            min(1.0, eligibility_score)
        )

        confidence_component = max(
            0.0,
            min(1.0, confidence)
        )

        # Stronger profile-aware ranking
        final_score = (
            retrieval_component * 0.30
            + eligibility_component * 0.30
            + state_score * 0.20
            + occupation_score * 0.15
            + confidence_component * 0.05
        )

        # Strong penalty for an explicitly incompatible state
        scheme_states = [
            str(x).strip().lower()
            for x in scheme.get(
                "states",
                []
            )
        ]

        user_state = str(
            profile.get("state", "")
        ).strip().lower()

        if (
            user_state
            and scheme_states
            and "all" not in scheme_states
            and user_state not in scheme_states
        ):
            final_score *= 0.45

        return round(
            max(
                0.0,
                min(
                    1.0,
                    final_score
                )
            ),
            4
        )

    def rank(
        self,
        schemes,
        eligibility_results,
        profile=None
    ):
        profile = profile or {}

        eligibility_map = {}

        for result in eligibility_results:
            scheme_id = result.get(
                "scheme_id"
            )

            eligibility_map[
                scheme_id
            ] = result

        ranked = []

        for scheme in schemes:

            scheme_id = scheme.get(
                "id"
            )

            eligibility = eligibility_map.get(
                scheme_id,
                {}
            )

            eligibility_score = float(
                eligibility.get(
                    "score",
                    0.0
                )
            )

            final_score = self.calculate_score(
                scheme,
                eligibility_score,
                profile
            )

            item = scheme.copy()

            item["eligibility_score"] = (
                eligibility_score
            )

            item["final_recommendation_score"] = (
                final_score
            )

            item["eligibility_status"] = (
                eligibility.get(
                    "status",
                    "unknown"
                )
            )

            ranked.append(item)

        ranked.sort(
            key=lambda x: x.get(
                "final_recommendation_score",
                0.0
            ),
            reverse=True
        )

        return ranked