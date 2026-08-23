class EligibilityEngine:
    """
    Evaluates a user's profile against normalized
    government scheme eligibility information.
    """

    def __init__(self):
        pass

    def check(
        self,
        user: dict,
        scheme: dict
    ) -> dict:

        score = 0.0
        reasons = []
        warnings = []

        # ==================================================
        # STATE
        # ==================================================

        user_state = str(
            user.get("state", "")
        ).strip().lower()

        scheme_states = [
            str(x).strip().lower()
            for x in scheme.get(
                "states",
                []
            )
        ]

        if user_state and scheme_states:

            if "all" in scheme_states:

                score += 0.25

                reasons.append(
                    "Scheme is available across India."
                )

            elif user_state in scheme_states:

                score += 0.40

                reasons.append(
                    "Your state matches the scheme."
                )

            else:

                score -= 0.30

                warnings.append(
                    "The scheme appears to be for "
                    "another state."
                )

        # ==================================================
        # OCCUPATION
        # ==================================================

        user_occupation = str(
            user.get("occupation", "")
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

        if user_occupation and occupations:

            if user_occupation in occupations:

                score += 0.30

                reasons.append(
                    "Your occupation matches "
                    "the scheme eligibility."
                )

            else:

                score -= 0.20

                warnings.append(
                    "Your occupation does not clearly "
                    "match the listed occupation criteria."
                )

        # ==================================================
        # AGE
        # ==================================================

        age = user.get("age")

        age_min = eligibility.get(
            "age_min"
        )

        age_max = eligibility.get(
            "age_max"
        )

        if age is not None:

            try:
                age = float(age)

                if (
                    age_min is not None
                    and age < float(age_min)
                ):

                    score -= 0.30

                    warnings.append(
                        "Your age appears to be below "
                        "the minimum age requirement."
                    )

                elif (
                    age_max is not None
                    and age > float(age_max)
                ):

                    score -= 0.30

                    warnings.append(
                        "Your age appears to be above "
                        "the maximum age requirement."
                    )

                else:

                    score += 0.15

                    reasons.append(
                        "Age requirement appears compatible."
                    )

            except (
                ValueError,
                TypeError
            ):

                pass

        # ==================================================
        # INCOME
        # ==================================================

        user_income = user.get(
            "income"
        )

        income_max = eligibility.get(
            "income_max"
        )

        if (
            user_income is not None
            and income_max is not None
        ):

            try:

                if float(user_income) <= float(
                    income_max
                ):

                    score += 0.25

                    reasons.append(
                        "Your reported income appears "
                        "within the listed income limit."
                    )

                else:

                    score -= 0.30

                    warnings.append(
                        "Your reported income appears "
                        "above the listed income limit."
                    )

            except (
                ValueError,
                TypeError
            ):

                pass

        # ==================================================
        # FINAL SCORE
        # ==================================================

        score = max(
            0.0,
            min(1.0, score)
        )

        # Determine status

        if score >= 0.60:

            status = "likely_eligible"

        elif score >= 0.30:

            status = "possibly_eligible"

        else:

            status = "unlikely_eligible"

        return {
            "score": round(
                score,
                4
            ),

            "status": status,

            "reasons": reasons,

            "warnings": warnings
        }


# ==========================================================
# BACKWARD COMPATIBILITY
# ==========================================================

def calculate_eligibility_score(
    scheme: dict,
    profile: dict
) -> float:

    engine = EligibilityEngine()

    result = engine.check(
        profile,
        scheme
    )

    return result["score"]


def check_eligibility(
    scheme: dict,
    profile: dict
) -> dict:

    engine = EligibilityEngine()

    return engine.check(
        profile,
        scheme
    )