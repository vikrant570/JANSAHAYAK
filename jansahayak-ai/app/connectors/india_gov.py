import requests

from app.connectors.base import BaseConnector


class IndiaGovConnector(BaseConnector):

    API_URL = (
        "https://www.india.gov.in/"
        "my-government/schemes/search/"
        "dataservices/getschemes"
    )

    def __init__(self):

        self.session = requests.Session()

        self.session.headers.update({

            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/151.0.0.0 "
                "Safari/537.36"
            ),

            "Accept":
                "application/json, text/plain, */*",

            "Content-Type":
                "application/json",

            "Referer":
                "https://www.india.gov.in/"
        })

    def fetch(
        self,
        url: str | None = None
    ) -> str:

        payload = {

            "categories": [],

            "mustFilter": [],

            "pageNumber": 1,

            "pageSize": 10
        }

        response = self.session.post(

            url or self.API_URL,

            json=payload,

            timeout=30
        )

        print(
            "INDIA.GOV HTTP STATUS:",
            response.status_code
        )

        print(
            "INDIA.GOV FINAL URL:",
            response.url
        )

        response.raise_for_status()

        return response.text

    def extract(
        self,
        content: str
    ) -> list[dict]:

        import json

        data = json.loads(content)

        schemes_response = (
            data.get(
                "schemesResponse",
                {}
            )
        )

        records = schemes_response.get(
            "results",
            []
        )

        return [
            self._normalize_record(
                record
            )
            for record in records
        ]

    def _normalize_record(
        self,
        record: dict
    ) -> dict:

        states = (
            record.get(
                "beneficiaryState"
            )
            or []
        )

        if isinstance(
            states,
            str
        ):

            states = [states]

        tags = (
            record.get("tags")
            or []
        )

        # Remove null tags
        tags = [
            tag
            for tag in tags
            if tag
        ]

        categories = (
            record.get(
                "schemeCategory"
            )
            or []
        )

        if isinstance(
            categories,
            list
        ):

            category = (
                categories[0]
                if categories
                else "general"
            )

        else:

            category = str(
                categories
            )

        title = (
            record.get("title")
            or ""
        )

        slug = (
            record.get("slug")
            or ""
        )

        # India.gov doesn't always provide
        # a direct scheme URL in this response.
        # The slug can be used to identify the
        # scheme on India.gov.in.
        source_url = (
            f"https://www.india.gov.in/"
            f"my-government/schemes/"
            f"{slug}"
            if slug
            else ""
        )

        return {

            "name": title,

            "description": (
                record.get(
                    "description"
                )
                or ""
            ),

            "category": category,

            "categories": categories,

            "states": states,

            "benefits": [],

            "documents": [],

            "application_steps": [],

            "eligibility": {},

            "official_source":
                source_url,

            "source_name":
                "India.gov.in",

            "authority":
                record.get(
                    "ministry"
                )
                or "Government of India",

            "nodal_ministry":
                record.get(
                    "ministry"
                ),

            "level":
                "State"
                if states
                and states != ["All"]
                else "Central",

            "tags": tags,

            "slug": slug,

            "raw_source":
                record
        }

    def search(
        self,
        query: str = "",
        page_size: int = 10
    ) -> list[dict]:

        payload = {

            "categories": [],

            "mustFilter": [],

            "pageNumber": 1,

            "pageSize": page_size
        }

        response = self.session.post(

            self.API_URL,

            json=payload,

            timeout=30
        )

        print(
            "INDIA.GOV HTTP STATUS:",
            response.status_code
        )

        response.raise_for_status()

        data = response.json()

        schemes_response = (
            data.get(
                "schemesResponse",
                {}
            )
        )

        records = schemes_response.get(
            "results",
            []
        )

        normalized = [
            self._normalize_record(
                record
            )
            for record in records
        ]

        if not query:

            return normalized

        query_lower = query.lower()

        results = []

        for scheme in normalized:

            searchable = " ".join([

                scheme.get(
                    "name",
                    ""
                ),

                scheme.get(
                    "description",
                    ""
                ),

                scheme.get(
                    "category",
                    ""
                ),

                " ".join(
                    scheme.get(
                        "tags",
                        []
                    )
                )
            ]).lower()

            if query_lower in searchable:

                results.append(
                    scheme
                )

        return results