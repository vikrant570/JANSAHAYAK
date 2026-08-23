from app.services.india_detail_extractor import IndiaDetailExtractor
from app.services.myscheme_detail_extractor import MySchemeDetailExtractor


class SchemeDetailExtractor:

    def __init__(self):

        self.india = IndiaDetailExtractor()
        self.myscheme = MySchemeDetailExtractor()

    def extract(self, scheme: dict) -> dict:

        source = (
            scheme.get("source_name")
            or ""
        ).lower()

        url = (
            scheme.get("official_source")
            or ""
        )

        if "myscheme" in source:

            return self.myscheme.extract(
                scheme
            )

        if "india.gov" in source:

            return self.india.extract(
                scheme
            )

        return {
            "status": "unsupported_source",
            "http_status": None,
            "final_url": url,
            "documents": [],
            "eligibility": [],
            "benefits": [],
            "application_steps": [],
            "verified": False
        }