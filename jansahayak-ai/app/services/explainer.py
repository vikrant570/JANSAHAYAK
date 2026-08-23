class SchemeExplainer:

    def explain(
        self,
        scheme: dict,
        eligibility: dict | None,
        profile: dict | None
    ) -> str:

        name = scheme.get(
            "name",
            "this scheme"
        )

        description = scheme.get(
            "description",
            ""
        )

        if eligibility:

            if (
                eligibility["status"]
                == "likely_eligible"
            ):

                status_text = (
                    "Based on the information provided, "
                    "you appear to match the available "
                    "eligibility information."
                )

            else:

                status_text = (
                    "This scheme appears relevant, "
                    "but some eligibility conditions "
                    "could not be confirmed."
                )

        else:

            status_text = (
                "This scheme appears relevant "
                "to your request."
            )

        return (
            f"{name} may be relevant to your request. "
            f"{status_text} "
            f"Official description: {description} "
            f"Always verify the latest eligibility "
            f"and application requirements on the "
            f"official government source."
        )