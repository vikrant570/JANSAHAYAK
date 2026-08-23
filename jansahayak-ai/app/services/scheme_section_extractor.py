import re


class SchemeSectionExtractor:

    SECTION_ALIASES = {

        "eligibility": [
            "eligibility",
            "eligibility criteria",
            "who can apply",
            "eligibility conditions"
        ],

        "benefits": [
            "benefits",
            "benefit",
            "financial assistance",
            "scheme benefits"
        ],

        "documents": [
            "documents required",
            "required documents",
            "documents needed",
            "documents"
        ],

        "application_steps": [
            "how to apply",
            "application process",
            "application procedure",
            "how can i apply",
            "application"
        ]
    }

    STOP_WORDS = [

        "eligibility",
        "benefits",
        "documents required",
        "required documents",
        "documents",
        "how to apply",
        "application process",
        "application procedure",
        "contact",
        "faqs",
        "frequently asked questions",
        "references"
    ]

    def extract(
        self,
        text: str
    ) -> dict:

        if not text:

            return {
                "eligibility_text": "",
                "benefits_text": "",
                "documents_text": "",
                "application_steps_text": ""
            }

        clean_text = self._clean(
            text
        )

        return {

            "eligibility_text":
                self._extract_section(
                    clean_text,
                    self.SECTION_ALIASES[
                        "eligibility"
                    ]
                ),

            "benefits_text":
                self._extract_section(
                    clean_text,
                    self.SECTION_ALIASES[
                        "benefits"
                    ]
                ),

            "documents_text":
                self._extract_section(
                    clean_text,
                    self.SECTION_ALIASES[
                        "documents"
                    ]
                ),

            "application_steps_text":
                self._extract_section(
                    clean_text,
                    self.SECTION_ALIASES[
                        "application_steps"
                    ]
                )
        }

    # =========================================================
    # SECTION EXTRACTION
    # =========================================================

    def _extract_section(
        self,
        text: str,
        headings: list
    ) -> str:

        lower = text.lower()

        candidates = []

        for heading in headings:

            position = lower.find(
                heading.lower()
            )

            if position != -1:

                candidates.append(
                    (
                        position,
                        heading
                    )
                )

        if not candidates:

            return ""

        start, heading = min(
            candidates,
            key=lambda x: x[0]
        )

        content_start = (
            start + len(heading)
        )

        remaining = text[
            content_start:
        ]

        lower_remaining = (
            remaining.lower()
        )

        stop_positions = []

        for stop in self.STOP_WORDS:

            position = lower_remaining.find(
                stop.lower()
            )

            if position > 0:

                stop_positions.append(
                    position
                )

        if stop_positions:

            end = min(
                stop_positions
            )

            remaining = remaining[
                :end
            ]

        return remaining.strip()

    # =========================================================
    # CLEAN
    # =========================================================

    @staticmethod
    def _clean(
        text: str
    ) -> str:

        text = re.sub(
            r"\r\n?",
            "\n",
            text
        )

        text = re.sub(
            r"[ \t]+",
            " ",
            text
        )

        return text.strip()