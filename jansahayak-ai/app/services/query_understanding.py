class QueryUnderstanding:

    NEED_KEYWORDS = {

        "scholarship": [
            "scholarship",
            "education",
            "fees",
            "college fees",
            "tuition",
            "study"
        ],

        "agriculture": [
            "farmer",
            "farming",
            "agriculture",
            "crop",
            "tractor",
            "fertilizer",
            "irrigation",
            "agricultural equipment",
            "machinery"
        ],

        "business": [
            "business",
            "startup",
            "entrepreneur",
            "loan",
            "self employment",
            "shop"
        ],

        "housing": [
            "house",
            "housing",
            "home",
            "construction",
            "shelter"
        ],

        "health": [
            "hospital",
            "medical",
            "health",
            "treatment",
            "medicine"
        ],

        "employment": [
            "job",
            "employment",
            "work",
            "skill",
            "training"
        ],

        "women": [
            "woman",
            "women",
            "girl",
            "female"
        ]
    }

    def understand(self, text: str) -> dict:

        text_lower = text.lower()

        detected_categories = []

        for category, keywords in self.NEED_KEYWORDS.items():

            for keyword in keywords:

                if keyword in text_lower:

                    detected_categories.append(
                        category
                    )

                    break

        return {
            "original_query": text,
            "categories": list(
                dict.fromkeys(
                    detected_categories
                )
            )
        }