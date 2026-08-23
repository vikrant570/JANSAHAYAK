import re
from typing import List


class DocumentExtractor:
    """
    Extracts document-related information from official
    scheme detail text.

    Important:
    This class does NOT invent documents.
    If no reliable document section is found,
    it returns an empty list.
    """

    DOCUMENT_HEADINGS = [
        "documents required",
        "documents needed",
        "required documents",
        "documents",
        "supporting documents",
        "documents to be submitted",
        "list of documents",
        "documents required for application",
    ]

    STOP_HEADINGS = [
        "eligibility",
        "benefits",
        "application process",
        "how to apply",
        "application procedure",
        "application",
        "exclusions",
        "selection process",
        "contact",
        "references",
        "frequently asked questions",
        "faqs",
    ]

    def extract(
        self,
        text: str
    ) -> List[str]:

        if not text:
            return []

        text = self._clean_text(text)

        section = self._find_document_section(text)

        if not section:
            return []

        documents = self._extract_items(section)

        return self._deduplicate(documents)

    # ==========================================================
    # FIND DOCUMENT SECTION
    # ==========================================================

    def _find_document_section(
        self,
        text: str
    ) -> str:

        lower_text = text.lower()

        positions = []

        for heading in self.DOCUMENT_HEADINGS:

            position = lower_text.find(
                heading
            )

            if position != -1:

                positions.append(
                    (
                        position,
                        heading
                    )
                )

        if not positions:
            return ""

        start, heading = min(
            positions,
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

        for stop_heading in self.STOP_HEADINGS:

            position = lower_remaining.find(
                stop_heading
            )

            if position != -1:

                stop_positions.append(
                    position
                )

        if stop_positions:

            end = min(
                stop_positions
            )

            remaining = remaining[:end]

        return remaining.strip()

    # ==========================================================
    # EXTRACT ITEMS
    # ==========================================================

    def _extract_items(
        self,
        section: str
    ) -> List[str]:

        documents = []

        lines = section.splitlines()

        for line in lines:

            line = line.strip()

            if not line:
                continue

            # Remove bullets
            line = re.sub(
                r"^[•●▪◦\-*]+\s*",
                "",
                line
            )

            # Remove numbering
            line = re.sub(
                r"^\d+[\.\)]\s*",
                "",
                line
            )

            line = line.strip()

            if not line:
                continue

            # Ignore very long paragraphs.
            # They are usually descriptions rather
            # than document names.
            if len(line) > 180:
                continue

            if self._looks_like_document(line):

                documents.append(line)

        return documents

    # ==========================================================
    # DOCUMENT DETECTION
    # ==========================================================

    def _looks_like_document(
        self,
        text: str
    ) -> bool:

        lower = text.lower()

        keywords = [
            "aadhaar",
            "aadhar",
            "identity proof",
            "id proof",
            "pan card",
            "ration card",
            "income certificate",
            "caste certificate",
            "domicile certificate",
            "residence certificate",
            "disability certificate",
            "birth certificate",
            "death certificate",
            "marksheet",
            "mark sheet",
            "degree certificate",
            "educational certificate",
            "bank passbook",
            "bank account",
            "cancelled cheque",
            "photograph",
            "passport size",
            "address proof",
            "age proof",
            "land record",
            "land ownership",
            "ownership document",
            "farmer certificate",
            "farmer registration",
            "bonafide certificate",
            "school certificate",
            "college certificate",
            "undertaking",
            "affidavit",
            "application form",
            "registration certificate",
            "license",
            "permit",
        ]

        return any(
            keyword in lower
            for keyword in keywords
        )

    # ==========================================================
    # CLEAN TEXT
    # ==========================================================

    @staticmethod
    def _clean_text(
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

    # ==========================================================
    # DEDUPLICATION
    # ==========================================================

    @staticmethod
    def _deduplicate(
        documents: List[str]
    ) -> List[str]:

        result = []

        seen = set()

        for document in documents:

            key = document.lower().strip()

            if key in seen:
                continue

            seen.add(key)

            result.append(
                document
            )

        return result