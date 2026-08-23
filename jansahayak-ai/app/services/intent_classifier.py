INTENTS = {
    "scheme_discovery": [
        "scheme",
        "government support",
        "yojana",
        "help",
        "benefit",
        "support"
    ],
    "eligibility_check": [
        "eligible",
        "eligibility",
        "qualify",
        "qualification"
    ],
    "scholarship_discovery": [
        "scholarship",
        "student scholarship",
        "education scholarship"
    ],
    "farmer_assistance": [
        "farmer",
        "farming",
        "kheti",
        "agriculture",
        "crop"
    ],
    "complaint_drafting": [
        "complaint",
        "complain",
        "grievance"
    ],
    "application_drafting": [
        "application",
        "apply",
        "application letter"
    ],
    "document_explanation": [
        "notice",
        "document",
        "letter",
        "certificate"
    ],
    "rights_information": [
        "right",
        "rights",
        "legal",
        "landlord",
        "deposit"
    ]
}


def classify_intent(query: str) -> tuple[str, float]:
    query_lower = query.lower()

    scores = {}

    for intent, keywords in INTENTS.items():
        score = sum(
            1 for keyword in keywords
            if keyword.lower() in query_lower
        )

        scores[intent] = score

    best_intent = max(scores, key=scores.get)
    best_score = scores[best_intent]

    if best_score == 0:
        return "general_civic_information", 0.35

    confidence = min(0.55 + best_score * 0.1, 0.95)

    return best_intent, confidence