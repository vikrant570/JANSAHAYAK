import re


class ResponseFormatter:
    """
    Converts JanSahayak recommendation results
    into a clean, concise, meaningful Markdown response
    for the frontend.

    The formatter avoids cutting descriptions or explanations
    in the middle of a sentence.
    """

    def format_recommendations(
        self,
        query: str,
        results: list[dict]
    ) -> str:

        # =====================================================
        # NO RESULTS
        # =====================================================

        if not results:
            return (
                "## No suitable schemes found\n\n"
                "I could not find a suitable government scheme "
                "from the available data.\n\n"
                "Try adding details such as your **state, age, "
                "occupation, income, or education**."
            )

        lines = []

        lines.append("## Recommended Schemes")
        lines.append("")

        lines.append(
            "Here are the most relevant government schemes "
            "I found for your request:"
        )

        lines.append("")

        # =====================================================
        # EACH RECOMMENDATION
        # =====================================================

        for index, result in enumerate(results, start=1):

            scheme = result.get("scheme", {})
            eligibility = result.get("eligibility", {})
            documents = result.get("documents", {})
            explanation = result.get("explanation", "")
            score = result.get("score", 0)

            # =================================================
            # SCHEME NAME
            # =================================================

            name = (
                scheme.get("name")
                or "Government Scheme"
            )

            lines.append(
                f"### {index}. {name}"
            )

            lines.append("")

            # =================================================
            # DESCRIPTION
            # =================================================

            raw_description = (
                scheme.get("description", "")
                or ""
            )

            description = self._short_description(
                raw_description
            )

            if description:

                lines.append(description)
                lines.append("")

            # =================================================
            # ELIGIBILITY
            # =================================================

            eligibility_status = (
                eligibility.get("status")
                or eligibility.get("eligibility_status")
                or "needs_verification"
            )

            readable_status = (
                str(eligibility_status)
                .replace("_", " ")
                .strip()
                .title()
            )

            lines.append(
                f"**Eligibility:** {readable_status}"
            )

            # =================================================
            # MATCH SCORE
            # =================================================

            score_percent = self._score_to_percent(
                score
            )

            if score_percent is not None:

                lines.append(
                    f"**Match Score:** {score_percent}%"
                )

            lines.append("")

            # =================================================
            # WHY IT MAY HELP
            # =================================================

            short_reason = self._short_reason(
                explanation=explanation,
                description=raw_description,
                scheme_name=name
            )

            if short_reason:

                lines.append(
                    f"**Why it may help:** {short_reason}"
                )

                lines.append("")

            # =================================================
            # VERIFIED DOCUMENTS
            # =================================================

            documents_verified = bool(
                documents.get(
                    "documents_verified",
                    False
                )
            )

            if documents_verified:

                required = documents.get(
                    "required_documents",
                    []
                )

                missing = documents.get(
                    "missing_documents",
                    []
                )

                if required:

                    lines.append(
                        "**Documents:**"
                    )

                    for document in required[:5]:

                        if document in missing:

                            lines.append(
                                f"- ⚠️ {document}"
                            )

                        else:

                            lines.append(
                                f"- ✅ {document}"
                            )

                    if len(required) > 5:

                        remaining = (
                            len(required) - 5
                        )

                        lines.append(
                            f"- ...and {remaining} more"
                        )

                    lines.append("")

            # =================================================
            # OFFICIAL SOURCE
            # =================================================

            official_source = (
                scheme.get("official_source")
                or documents.get("official_source")
            )

            if official_source:

                lines.append(
                    f"🔗 [View Official Scheme]"
                    f"({official_source})"
                )

                lines.append("")

            # =================================================
            # DIVIDER
            # =================================================

            if index < len(results):

                lines.append("---")
                lines.append("")

        # =====================================================
        # COMMON DISCLAIMER
        # =====================================================

        lines.append(
            "> **Note:** Eligibility and exact document "
            "requirements should be confirmed on the official "
            "government scheme portal before applying."
        )

        return "\n".join(lines)

    # =========================================================
    # TEXT CLEANING
    # =========================================================

    @staticmethod
    def _clean_text(text: str) -> str:
        """
        Remove unnecessary line breaks and extra spaces.
        """

        if not text:
            return ""

        text = str(text)

        text = text.replace(
            "\n",
            " "
        )

        text = " ".join(
            text.split()
        )

        return text.strip()

    # =========================================================
    # COMPLETE SENTENCE EXTRACTION
    # =========================================================

    @staticmethod
    def _complete_sentence_excerpt(
        text: str,
        preferred_length: int = 240,
        max_sentences: int = 2
    ) -> str:
        """
        Returns complete sentences instead of cutting text
        at an arbitrary character position.

        If the first sentence itself is long, it is kept complete
        rather than being cut midway.
        """

        if not text:
            return ""

        text = ResponseFormatter._clean_text(
            text
        )

        if not text:
            return ""

        # Split text into sentences.
        sentences = re.split(
            r"(?<=[.!?])\s+",
            text
        )

        sentences = [
            sentence.strip()
            for sentence in sentences
            if sentence.strip()
        ]

        if not sentences:
            return text

        selected = []
        current_length = 0

        for sentence in sentences:

            # Add punctuation when source text has no ending punctuation
            if sentence[-1] not in ".!?":
                sentence = sentence + "."

            candidate_length = (
                current_length
                + len(sentence)
                + 1
            )

            # Always allow the first complete sentence.
            if not selected:

                selected.append(
                    sentence
                )

                current_length = len(
                    sentence
                )

                continue

            # Maximum number of sentences reached.
            if len(selected) >= max_sentences:
                break

            # Add another sentence only when it remains concise.
            if candidate_length <= preferred_length:

                selected.append(
                    sentence
                )

                current_length = (
                    candidate_length
                )

            else:
                break

        return " ".join(
            selected
        ).strip()

    # =========================================================
    # SHORT DESCRIPTION
    # =========================================================

    @staticmethod
    def _short_description(
        description: str,
        max_length: int = 240
    ) -> str:
        """
        Keep one or two meaningful complete sentences.

        Unlike character slicing, this method will not produce
        descriptions such as:

        'The scheme provides financial support for...'

        Instead, it ends after a complete thought.
        """

        if not description:
            return ""

        description = (
            ResponseFormatter
            ._clean_text(
                description
            )
        )

        if not description:
            return ""

        return (
            ResponseFormatter
            ._complete_sentence_excerpt(
                text=description,
                preferred_length=max_length,
                max_sentences=2
            )
        )

    # =========================================================
    # SHORT REASON
    # =========================================================

    @staticmethod
    def _short_reason(
        explanation: str,
        description: str,
        scheme_name: str = ""
    ) -> str:
        """
        Produces a short and meaningful explanation.

        Generic recommendation sentences are improved using
        the official scheme description without cutting
        sentences midway.
        """

        explanation = (
            ResponseFormatter
            ._clean_text(
                explanation
            )
        )

        description = (
            ResponseFormatter
            ._clean_text(
                description
            )
        )

        # =====================================================
        # REMOVE REPETITIVE DISCLAIMERS
        # =====================================================

        unwanted_phrases = [
            (
                "Eligibility could not be fully determined "
                "from the available information."
            ),
            (
                "Always verify the latest eligibility and "
                "application requirements on the official "
                "government source."
            ),
            (
                "Eligibility and exact document requirements "
                "should be confirmed on the official government "
                "scheme portal before applying."
            ),
            (
                "Please verify eligibility on the official website."
            ),
        ]

        for phrase in unwanted_phrases:

            explanation = explanation.replace(
                phrase,
                ""
            )

        explanation = (
            ResponseFormatter
            ._clean_text(
                explanation
            )
        )

        # =====================================================
        # REMOVE "OFFICIAL DESCRIPTION:" DUPLICATION
        # =====================================================

        marker = "official description:"

        marker_position = (
            explanation
            .lower()
            .find(marker)
        )

        if marker_position != -1:

            explanation = explanation[
                :marker_position
            ]

        explanation = (
            explanation
            .strip(
                " .:-"
            )
        )

        # =====================================================
        # CHECK FOR GENERIC EXPLANATION
        # =====================================================

        generic_phrases = [
            "may be relevant to your request",
            "may be relevant based on your request",
            "may match your request",
            "may be useful for your request",
            "may be suitable for your request",
        ]

        is_generic = (
            not explanation
            or any(
                phrase
                in explanation.lower()
                for phrase
                in generic_phrases
            )
        )

        # =====================================================
        # GENERIC EXPLANATION + DESCRIPTION
        # =====================================================

        if is_generic and description:

            meaningful_description = (
                ResponseFormatter
                ._complete_sentence_excerpt(
                    text=description,
                    preferred_length=230,
                    max_sentences=1
                )
            )

            if meaningful_description:

                if scheme_name:

                    return (
                        f"{scheme_name} may be relevant to your needs. "
                        f"The official description indicates that "
                        f"{meaningful_description}"
                    )

                return (
                    "This scheme may be relevant to your needs. "
                    "The official description indicates that "
                    f"{meaningful_description}"
                )

        # =====================================================
        # MEANINGFUL EXISTING EXPLANATION
        # =====================================================

        if explanation:

            return (
                ResponseFormatter
                ._complete_sentence_excerpt(
                    text=explanation,
                    preferred_length=300,
                    max_sentences=2
                )
            )

        # =====================================================
        # FINAL SAFE FALLBACK
        # =====================================================

        if scheme_name:

            return (
                f"{scheme_name} may be relevant based on "
                "the information provided in your request."
            )

        return (
            "This scheme may be relevant based on "
            "the information provided in your request."
        )

    # =========================================================
    # SCORE TO PERCENTAGE
    # =========================================================

    @staticmethod
    def _score_to_percent(
        score
    ):

        try:

            value = float(
                score
            )

        except (
            TypeError,
            ValueError
        ):

            return None

        if 0 <= value <= 1:

            value = (
                value * 100
            )

        return round(
            value
        )