class ResponseFormatter:
    """
    Converts JanSahayak recommendation results
    into a short Markdown response for the frontend.
    """

    def format_recommendations(
        self,
        query: str,
        results: list[dict]
    ) -> str:

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
            # SHORT DESCRIPTION
            # =================================================

            description = self._short_description(
                scheme.get(
                    "description",
                    ""
                )
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
                explanation,
                description
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

            if index < len(results):

                lines.append("---")
                lines.append("")

        # =====================================================
        # ONE COMMON DISCLAIMER
        # =====================================================

        lines.append(
            "> **Note:** Eligibility and exact document "
            "requirements should be confirmed on the official "
            "government scheme portal before applying."
        )

        return "\n".join(lines)

    # =========================================================
    # SHORT DESCRIPTION
    # =========================================================

    @staticmethod
    def _short_description(
        description: str,
        max_length: int = 180
    ) -> str:

        if not description:
            return ""

        description = (
            str(description)
            .replace("\n", " ")
            .strip()
        )

        description = " ".join(
            description.split()
        )

        if len(description) <= max_length:
            return description

        shortened = (
            description[:max_length]
            .rsplit(" ", 1)[0]
        )

        return shortened + "..."

    # =========================================================
    # SHORT REASON
    # =========================================================

    @staticmethod
    def _short_reason(
        explanation: str,
        description: str
    ) -> str:

        if not explanation:
            return ""

        explanation = (
            str(explanation)
            .replace("\n", " ")
            .strip()
        )

        explanation = " ".join(
            explanation.split()
        )

        # Remove repeated generic sentences
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
        ]

        for phrase in unwanted_phrases:
            explanation = explanation.replace(
                phrase,
                ""
            )

        # Remove repeated official description section
        marker = "Official description:"

        lower_explanation = (
            explanation.lower()
        )

        marker_position = (
            lower_explanation.find(
                marker.lower()
            )
        )

        if marker_position != -1:
            explanation = explanation[
                :marker_position
            ]

        explanation = explanation.strip(
            " ."
        )

        # =====================================================
        # IMPROVE GENERIC EXPLANATIONS
        # =====================================================

        generic_phrases = [
            "may be relevant to your request",
            "may be relevant based on your request",
            "may match your request",
        ]

        is_generic = any(
            phrase in explanation.lower()
            for phrase in generic_phrases
        )

        if is_generic and description:

            clean_description = (
                str(description)
                .replace("\n", " ")
                .strip()
            )

            clean_description = " ".join(
                clean_description.split()
            )

            if len(clean_description) > 150:

                clean_description = (
                    clean_description[:150]
                    .rsplit(" ", 1)[0]
                    + "..."
                )

            explanation = explanation.rstrip(
                "."
            )

            return (
                f"{explanation}. "
                f"This scheme provides support related to "
                f"{clean_description}"
            )

        # Allow around 1-2 lines of explanation
        if len(explanation) > 260:

            explanation = (
                explanation[:260]
                .rsplit(" ", 1)[0]
                + "..."
            )

        return explanation

    # =========================================================
    # SCORE TO PERCENTAGE
    # =========================================================

    @staticmethod
    def _score_to_percent(
        score
    ):

        try:
            value = float(score)

        except (TypeError, ValueError):
            return None

        if 0 <= value <= 1:
            value = value * 100

        return round(value)