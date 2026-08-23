import re


class ProfileExtractor:

    STATES = [
        "Punjab",
        "Haryana",
        "Himachal Pradesh",
        "Rajasthan",
        "Uttar Pradesh",
        "Delhi",
        "Gujarat",
        "Maharashtra",
        "Bihar",
        "West Bengal",
        "Kerala",
        "Tamil Nadu",
        "Karnataka",
        "Telangana",
        "Andhra Pradesh",
        "Madhya Pradesh",
        "Odisha",
        "Assam",
        "Jharkhand",
        "Chhattisgarh",
        "Uttarakhand",
        "Goa",
        "Manipur",
        "Meghalaya",
        "Mizoram",
        "Nagaland",
        "Sikkim",
        "Tripura"
    ]

    OCCUPATIONS = [
        "farmer",
        "student",
        "entrepreneur",
        "business owner",
        "worker",
        "employee",
        "teacher",
        "artisan",
        "fisherman",
        "unemployed"
    ]

    def extract(self, text: str) -> dict:

        text_lower = text.lower()

        profile = {
            "age": None,
            "state": None,
            "occupation": None,
            "income": None,
            "gender": None,
            "education": None
        }

        # -----------------------------
        # AGE
        # -----------------------------

        age_patterns = [
            r"(\d{1,3})\s*(?:years?\s*old|year\s*old)",
            r"age\s*(?:is|:)?\s*(\d{1,3})"
        ]

        for pattern in age_patterns:

            match = re.search(
                pattern,
                text_lower
            )

            if match:

                profile["age"] = int(
                    match.group(1)
                )

                break

        # -----------------------------
        # STATE
        # -----------------------------

        for state in self.STATES:

            if state.lower() in text_lower:

                profile["state"] = state

                break

        # -----------------------------
        # OCCUPATION
        # -----------------------------

        for occupation in self.OCCUPATIONS:

            if occupation in text_lower:

                profile["occupation"] = occupation

                break

        # -----------------------------
        # INCOME
        # -----------------------------

        income_patterns = [
            r"income\s*(?:is|:)?\s*₹?\s*([\d,]+)",
            r"income\s*(?:is|:)?\s*rs\.?\s*([\d,]+)",
            r"₹\s*([\d,]+)",
            r"rs\.?\s*([\d,]+)"
        ]

        for pattern in income_patterns:

            match = re.search(
                pattern,
                text_lower
            )

            if match:

                value = match.group(1)

                value = value.replace(
                    ",",
                    ""
                )

                profile["income"] = float(
                    value
                )

                break

        # -----------------------------
        # LAKH INCOME
        # -----------------------------

        lakh_match = re.search(
            r"([\d.]+)\s*(?:lakh|lakhs)",
            text_lower
        )

        if lakh_match:

            lakh_value = float(
                lakh_match.group(1)
            )

            profile["income"] = (
                lakh_value * 100000
            )

        # -----------------------------
        # GENDER
        # -----------------------------

        female_words = [
            "female",
            "woman",
            "women",
            "girl"
        ]

        male_words = [
            "male",
            "man",
            "boy"
        ]

        if any(
            word in text_lower
            for word in female_words
        ):

            profile["gender"] = "female"

        elif any(
            word in text_lower
            for word in male_words
        ):

            profile["gender"] = "male"

        # -----------------------------
        # EDUCATION
        # -----------------------------

        education_keywords = [
            "school",
            "college",
            "undergraduate",
            "graduate",
            "postgraduate",
            "btech",
            "mtech",
            "diploma"
        ]

        for keyword in education_keywords:

            if keyword in text_lower:

                profile["education"] = keyword

                break

        return profile