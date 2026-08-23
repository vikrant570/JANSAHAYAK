from app.services.scheme_detail_parser import (
    SchemeDetailParser
)


class MySchemeDetailExtractor:
    """
    Handles MyScheme structured detail data.

    IMPORTANT:
    HTML scraping is intentionally not used because
    MyScheme scheme pages load scheme content dynamically.

    The extractor accepts structured detail JSON whenever
    it is supplied by an authorised/available source.
    """

    def __init__(self):

        self.parser = (
            SchemeDetailParser()
        )

    def extract(
        self,
        scheme: dict,
        detail_data: dict | None = None
    ) -> dict:

        result = {
            "status":
                "detail_data_unavailable",

            "http_status":
                None,

            "final_url":
                scheme.get(
                    "official_source",
                    ""
                ),

            "documents":
                [],

            "documents_verified":
                False,

            "eligibility_text":
                "",

            "benefits":
                [],

            "application_steps":
                [],

            "application_urls":
                [],

            "verified":
                False
        }

        # -----------------------------------------------------
        # No structured detail data available
        # -----------------------------------------------------

        if not detail_data:

            return result

        # -----------------------------------------------------
        # Parse official structured data
        # -----------------------------------------------------

        parsed = self.parser.parse(
            detail_data
        )

        result.update(
            parsed
        )

        result["status"] = (
            "success"
            if parsed.get(
                "detail_verified"
            )
            else
            "no_detail_fields"
        )

        result["verified"] = bool(
            parsed.get(
                "detail_verified"
            )
        )

        return result