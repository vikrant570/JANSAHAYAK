import re


class QueryAnalyzer:

    def analyze(self, query: str) -> dict:

        text = query.lower().strip()

        profile = {
            "query": query,
            "intent": "general",
            "state": None,
            "occupation": None,
            "age": None,
            "gender": None,
            "category": None
        }

        # -----------------------------
        # AGE
        # -----------------------------

        age_patterns = [
            r"\b(\d{1,3})\s*(?:years?|yrs?)\s*old\b",
            r"\bage\s*(?:is|of)?\s*(\d{1,3})\b",
            r"\b(\d{1,3})\s*year\s*old\b"
        ]

        for pattern in age_patterns:

            match = re.search(
                pattern,
                text
            )

            if match:

                profile["age"] = int(
                    match.group(1)
                )

                break

        # -----------------------------
        # STATES
        # -----------------------------

        states = [
            "punjab",
            "haryana",
            "himachal pradesh",
            "uttarakhand",
            "uttar pradesh",
            "rajasthan",
            "gujarat",
            "maharashtra",
            "delhi",
            "bihar",
            "west bengal",
            "assam",
            "kerala",
            "tamil nadu",
            "karnataka",
            "telangana",
            "andhra pradesh",
            "odisha",
            "jharkhand",
            "chhattisgarh",
            "madhya pradesh",
            "goa"
        ]

        for state in states:

            if state in text:

                profile["state"] = state.title()

                break

        # -----------------------------
        # OCCUPATION
        # -----------------------------

        occupation_map = {

            "student": [
                "student",
                "college student",
                "university student"
            ],

            "farmer": [
                "farmer",
                "kisan",
                "agricultural worker"
            ],

            "entrepreneur": [
                "entrepreneur",
                "business owner",
                "businessman",
                "businesswoman"
            ],

            "worker": [
                "worker",
                "labourer",
                "laborer"
            ],

            "job seeker": [
                "job seeker",
                "looking for job",
                "unemployed"
            ]
        }

        for occupation, keywords in occupation_map.items():

            if any(
                keyword in text
                for keyword in keywords
            ):

                profile["occupation"] = occupation

                break

        # -----------------------------
        # GENDER
        # -----------------------------

        if any(
            word in text
            for word in [
                "female",
                "woman",
                "women",
                "girl"
            ]
        ):

            profile["gender"] = "Female"

        elif any(
            word in text
            for word in [
                "male",
                "man",
                "boy"
            ]
        ):

            profile["gender"] = "Male"

        # -----------------------------
        # INTENT
        # -----------------------------

        intent_keywords = {

            "scholarship": [
                "scholarship",
                "scholarships",
                "education",
                "student"
            ],

            "agriculture": [
                "farmer",
                "farming",
                "agriculture",
                "kisan",
                "crop"
            ],

            "business": [
                "business",
                "startup",
                "entrepreneur",
                "loan"
            ],

            "employment": [
                "job",
                "employment",
                "career",
                "skill",
                "training"
            ],

            "housing": [
                "house",
                "housing",
                "home"
            ],

            "health": [
                "health",
                "medical",
                "hospital",
                "treatment"
            ]
        }

        for intent, keywords in intent_keywords.items():

            if any(
                keyword in text
                for keyword in keywords
            ):

                profile["intent"] = intent

                break

        profile["category"] = (
            profile["intent"]
        )

        return profile