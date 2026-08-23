import re
from difflib import get_close_matches


class QueryProcessor:

    # Common words used in government-scheme queries
    VOCABULARY = {
        "farmer",
        "farmers",
        "agriculture",
        "agricultural",
        "student",
        "students",
        "scholarship",
        "education",
        "business",
        "entrepreneur",
        "employment",
        "job",
        "loan",
        "financial",
        "assistance",
        "support",
        "subsidy",
        "housing",
        "house",
        "health",
        "medical",
        "insurance",
        "pension",
        "women",
        "woman",
        "children",
        "child",
        "senior",
        "elderly",
        "disabled",
        "disability",
        "startup",
        "training",
        "skill",
        "skills",
        "agriculture",
        "crop",
        "farming",
        "irrigation",
        "equipment",
        "equipment",
        "business",
        "employment",
        "self",
        "employment",
        "financial",
        "help",
        "scheme",
        "schemes",
        "government",
        "benefit",
        "benefits",
        "money",
        "income",
        "credit",
        "pension",
        "widow",
        "widows",
        "minority",
        "sc",
        "st",
        "obc",
    }

    # Common spelling corrections
    COMMON_CORRECTIONS = {
        "frammer": "farmer",
        "farmar": "farmer",
        "farer": "farmer",
        "agricultre": "agriculture",
        "agricultral": "agricultural",
        "finacial": "financial",
        "financal": "financial",
        "assistnce": "assistance",
        "assisstance": "assistance",
        "scholrship": "scholarship",
        "scholorship": "scholarship",
        "studnt": "student",
        "studdent": "student",
        "busines": "business",
        "busness": "business",
        "entreprenuer": "entrepreneur",
        "enterpreneur": "entrepreneur",
        "employement": "employment",
        "emploiment": "employment",
        "subsidy": "subsidy",
        "goverment": "government",
        "govt": "government",
        "schem": "scheme",
        "schemes": "schemes",
        "punjab": "Punjab",
        "delhi": "Delhi",
        "haryana": "Haryana",
        "rajasthan": "Rajasthan",
        "gujrat": "Gujarat",
        "gujrat": "Gujarat",
        "maharastra": "Maharashtra",
        "maharashtra": "Maharashtra",
        "uttarpradesh": "Uttar Pradesh",
        "karnatka": "Karnataka",
        "kerela": "Kerala",
    }

    def normalize_text(self, text: str) -> str:

        if not text:
            return ""

        text = str(text).strip()

        # Normalize repeated spaces
        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text

    def correct_spelling(self, text: str) -> str:

        text = self.normalize_text(text)

        words = text.split()

        corrected = []

        for word in words:

            # Keep punctuation separate
            clean = re.sub(
                r"[^a-zA-Z]",
                "",
                word
            )

            lower = clean.lower()

            if not lower:
                corrected.append(word)
                continue

            # Exact known correction
            if lower in self.COMMON_CORRECTIONS:

                replacement = (
                    self.COMMON_CORRECTIONS[
                        lower
                    ]
                )

                if word[0].isupper():
                    replacement = replacement.capitalize()

                corrected.append(
                    replacement
                )

                continue

            # Fuzzy matching
            match = get_close_matches(
                lower,
                self.VOCABULARY,
                n=1,
                cutoff=0.82
            )

            if match:

                replacement = match[0]

                # Preserve normal capitalization
                if word[0].isupper():
                    replacement = (
                        replacement.capitalize()
                    )

                corrected.append(
                    replacement
                )

            else:

                corrected.append(
                    word
                )

        return " ".join(corrected)

    def process(self, query: str) -> dict:

        original = (
            query or ""
        ).strip()

        corrected = self.correct_spelling(
            original
        )

        return {

            "original_query":
                original,

            "corrected_query":
                corrected,

            "was_corrected":
                original != corrected
        }