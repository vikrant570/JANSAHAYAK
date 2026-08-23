from typing import Any


def _text(value: Any) -> str:
    """Convert a value to searchable lowercase text."""

    if value is None:
        return ""

    if isinstance(value, list):
        return " ".join(
            str(item)
            for item in value
        ).lower()

    return str(value).lower()


def rank_schemes(
    schemes: list[dict],
    query: str,
    user_type: str | None = None,
    state: str | None = None,
    category: str | None = None,
) -> list[dict]:

    query_text = _text(query)

    scored = []

    for scheme in schemes:

        score = 0.0

        name = _text(
            scheme.get("name")
        )

        description = _text(
            scheme.get("description")
        )

        scheme_category = _text(
            scheme.get("category")
        )

        states = [
            str(s).lower().strip()
            for s in scheme.get(
                "states",
                []
            )
        ]

        target_users = [
            str(u).lower().strip()
            for u in scheme.get(
                "target_users",
                []
            )
        ]

        tags = [
            str(tag).lower().strip()
            for tag in scheme.get(
                "tags",
                []
            )
        ]

        # --------------------------------------------------
        # 1. State relevance
        # --------------------------------------------------

        if state:

            requested_state = (
                state.lower().strip()
            )

            if requested_state in states:

                score += 50

            elif "all" in states:

                score += 35

            elif states:

                score -= 40

        # --------------------------------------------------
        # 2. User type relevance
        # --------------------------------------------------

        if user_type:

            user = user_type.lower().strip()

            if user in target_users:

                score += 30

            if user in name:

                score += 20

            if user in description:

                score += 15

            if user in tags:

                score += 15

        # --------------------------------------------------
        # 3. Category relevance
        # --------------------------------------------------

        if category:

            requested_category = (
                category.lower().strip()
            )

            if requested_category in scheme_category:

                score += 30

        # --------------------------------------------------
        # 4. Query relevance
        # --------------------------------------------------

        query_words = [
            word
            for word in query_text.split()
            if len(word) > 2
        ]

        for word in query_words:

            if word in name:

                score += 10

            if word in description:

                score += 5

            if word in tags:

                score += 7

            if word in scheme_category:

                score += 5

        # --------------------------------------------------
        # 5. Verification
        # --------------------------------------------------

        if (
            scheme.get(
                "verification_status"
            )
            == "verified"
        ):

            score += 5

        # --------------------------------------------------
        # Store score
        # --------------------------------------------------

        scheme_copy = dict(scheme)

        scheme_copy[
            "relevance_score"
        ] = round(score, 2)

        scored.append(
            scheme_copy
        )

    # Highest score first

    scored.sort(
        key=lambda item: item[
            "relevance_score"
        ],
        reverse=True
    )

    return scored