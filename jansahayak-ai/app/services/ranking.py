def calculate_score(
    scheme: dict,
    eligibility: dict | None
) -> float:

    semantic = scheme.get(
        "retrieval_score",
        0
    )

    score = semantic * 0.60

    if scheme.get(
        "verification_status"
    ) == "verified":

        score += 0.15

    if eligibility:

        if eligibility["status"] == "likely_eligible":

            score += 0.25

        elif (
            eligibility["status"]
            == "possibly_eligible"
        ):

            score += 0.10

    return round(
        min(score, 1.0),
        4
    )