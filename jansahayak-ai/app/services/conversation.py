import re
from typing import Dict, Any, List


class ConversationEngine:

    def __init__(self):
        self.history = []

    # ---------------------------------------------------------
    # STORE MESSAGE
    # ---------------------------------------------------------

    def add_message(self, role: str, content: str):

        self.history.append({
            "role": role,
            "content": content
        })

    # ---------------------------------------------------------
    # EXTRACT BASIC USER INFORMATION
    # ---------------------------------------------------------

    def extract_profile(
        self,
        message: str,
        existing_profile: Dict[str, Any] | None = None
    ) -> Dict[str, Any]:

        profile = dict(existing_profile or {})

        text = message.lower()

        # AGE
        age_patterns = [
            r"(\d{1,3})\s*(?:years old|year old|yrs old|years)",
            r"age\s*(?:is|:)?\s*(\d{1,3})"
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

        # INCOME
        income_patterns = [
            r"income\s*(?:is|:)?\s*(?:rs\.?|₹)?\s*([\d,]+)",
            r"earn\s*(?:rs\.?|₹)?\s*([\d,]+)",
            r"earning\s*(?:rs\.?|₹)?\s*([\d,]+)"
        ]

        for pattern in income_patterns:

            match = re.search(
                pattern,
                text
            )

            if match:

                value = (
                    match.group(1)
                    .replace(",", "")
                )

                profile["income"] = float(value)

                break

        # OCCUPATION
        occupations = [
            "farmer",
            "student",
            "teacher",
            "worker",
            "entrepreneur",
            "business owner",
            "shopkeeper",
            "artisan",
            "fisherman",
            "unemployed"
        ]

        for occupation in occupations:

            if occupation in text:

                profile["occupation"] = occupation

                break

        # COMMON STATES
        states = [
            "punjab",
            "haryana",
            "rajasthan",
            "uttar pradesh",
            "uttarakhand",
            "himachal pradesh",
            "bihar",
            "gujarat",
            "maharashtra",
            "madhya pradesh",
            "west bengal",
            "odisha",
            "kerala",
            "tamil nadu",
            "karnataka",
            "telangana",
            "andhra pradesh",
            "assam",
            "jharkhand",
            "chhattisgarh",
            "goa",
            "delhi"
        ]

        for state in states:

            if state in text:

                profile["state"] = state.title()

                break

        return profile

    # ---------------------------------------------------------
    # GENERATE CONVERSATIONAL RESPONSE
    # ---------------------------------------------------------

    def generate_response(
        self,
        query: str,
        results: Dict[str, Any],
        profile: Dict[str, Any]
    ) -> str:

        recommendations = results.get(
            "recommendations",
            []
        )

        if not recommendations:

            return (
                "I couldn't find a sufficiently relevant "
                "verified government scheme for your request. "
                "Try telling me your state, occupation, age, "
                "income and what kind of financial assistance "
                "you need."
            )

        response = []

        response.append(
            "I understand your request. Based on your "
            "information, I found these government schemes "
            "that may be relevant:"
        )

        response.append("")

        for index, scheme in enumerate(
            recommendations[:5],
            start=1
        ):

            name = scheme.get(
                "name",
                "Government Scheme"
            )

            description = scheme.get(
                "description",
                ""
            )

            score = scheme.get(
                "final_score",
                scheme.get(
                    "retrieval_score",
                    0
                )
            )

            response.append(
                f"{index}. {name}"
            )

            if description:

                short_description = (
                    description[:300]
                    .strip()
                )

                response.append(
                    f"   {short_description}"
                )

            response.append(
                f"   Relevance score: "
                f"{score:.2f}"
            )

            response.append("")

        response.append(
            "Important: eligibility and scheme "
            "availability should be verified using "
            "the official government source before applying."
        )

        return "\n".join(response)

    # ---------------------------------------------------------
    # MAIN CHAT FUNCTION
    # ---------------------------------------------------------

    def chat(
        self,
        message: str,
        analyzer,
        profile: Dict[str, Any] | None = None
    ) -> Dict[str, Any]:

        profile = self.extract_profile(
            message,
            profile
        )

        self.add_message(
            "user",
            message
        )

        results = analyzer.analyze(
            query=message,
            user=profile
        )

        response = self.generate_response(
            message,
            results,
            profile
        )

        self.add_message(
            "assistant",
            response
        )

        return {
            "message": response,
            "profile": profile,
            "results": results,
            "history": self.history
        }