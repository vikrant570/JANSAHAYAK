class RecommendationScorer:

    def score(
        self,
        scheme: dict,
        user: dict,
        retrieval_score: float
    ) -> float:

        score = float(retrieval_score)

        # ------------------------------------------------
        # 1. STATE MATCH
        # ------------------------------------------------

        user_state = (
            user.get("state") or ""
        ).strip().lower()

        scheme_states = [
            str(state).strip().lower()
            for state in scheme.get("states", [])
        ]

        if user_state:

            if user_state in scheme_states:
                score += 0.20

            elif "all" in scheme_states:
                score += 0.10

            elif scheme_states:
                score -= 0.20

        # ------------------------------------------------
        # 2. OCCUPATION MATCH
        # ------------------------------------------------

        user_occupation = (
            user.get("occupation") or ""
        ).strip().lower()

        eligibility = scheme.get(
            "eligibility",
            {}
        )

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

        if user_occupation:

            if user_occupation in occupations:
                score += 0.20

            elif user_occupation in target_users:
                score += 0.15

        # ------------------------------------------------
        # 3. CATEGORY MATCH
        # ------------------------------------------------

        query_category = (
            user.get("category") or ""
        ).strip().lower()

        scheme_category = str(
            scheme.get("category", "")
        ).lower()

        if (
            query_category
            and query_category in scheme_category
        ):
            score += 0.15

        # ------------------------------------------------
        # 4. VERIFICATION
        # ------------------------------------------------

        if (
            scheme.get(
                "verification_status"
            )
            == "verified"
        ):
            score += 0.05

        # ------------------------------------------------
        # 5. OFFICIAL SOURCE
        # ------------------------------------------------

        if scheme.get(
            "official_source"
        ):
            score += 0.05

        # ------------------------------------------------
        # NORMALIZE
        # ------------------------------------------------

        return round(
            min(score, 1.0),
            4
        )