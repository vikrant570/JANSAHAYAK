class SchemeEnrichmentMerger:

    def merge(
        self,
        scheme: dict,
        details: dict
    ) -> dict:

        result = dict(
            scheme
        )

        if not isinstance(
            details,
            dict
        ):
            return result

        # =====================================================
        # DOCUMENTS
        # =====================================================

        documents = details.get(
            "documents",
            []
        )

        if (
            details.get(
                "documents_verified"
            )
            and documents
        ):

            result[
                "documents"
            ] = documents

            result[
                "documents_verified"
            ] = True

        # =====================================================
        # BENEFITS
        # =====================================================

        benefits = details.get(
            "benefits",
            []
        )

        if benefits:

            result[
                "benefits"
            ] = benefits

        # =====================================================
        # ELIGIBILITY
        # =====================================================

        eligibility_text = (
            details.get(
                "eligibility_text",
                ""
            )
        )

        if eligibility_text:

            result[
                "eligibility_text"
            ] = eligibility_text

        # =====================================================
        # APPLICATION
        # =====================================================

        application_steps = (
            details.get(
                "application_steps",
                []
            )
        )

        if application_steps:

            result[
                "application_steps"
            ] = application_steps

        application_urls = (
            details.get(
                "application_urls",
                []
            )
        )

        if application_urls:

            result[
                "application_urls"
            ] = application_urls

        # =====================================================
        # DETAIL VERIFICATION
        # =====================================================

        result[
            "detail_verified"
        ] = bool(
            details.get(
                "verified",
                False
            )
            or
            details.get(
                "detail_verified",
                False
            )
        )

        return result