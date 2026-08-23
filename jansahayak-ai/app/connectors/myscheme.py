import os
import requests
from dotenv import load_dotenv

from app.connectors.base import BaseConnector


load_dotenv()


class MySchemeConnector(BaseConnector):

    def __init__(self):

        self.api_url = (
            "https://api.myscheme.gov.in/search/v6/schemes"
        )

        self.api_key = os.getenv(
            "MYSCHEME_API_KEY"
        )

        if not self.api_key:
            raise ValueError(
                "MYSCHEME_API_KEY is not configured in .env"
            )

    def fetch(
        self,
        url: str = None
    ) -> str:

        params = {
            "lang": "en",
            "q": "[]",
            "keyword": "",
            "sort": "",
            "from": 0,
            "size": 10
        }

        headers = {
            "accept": "application/json",
            "origin": "https://www.myscheme.gov.in",
            "x-api-key": self.api_key,
            "user-agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/151.0.0.0 Safari/537.36"
            )
        }

        response = requests.get(
            self.api_url,
            params=params,
            headers=headers,
            timeout=30
        )

        print(
            "MYSCHEME HTTP STATUS:",
            response.status_code
        )

        response.raise_for_status()

        return response.text

    def extract(
        self,
        content: str
    ) -> list[dict]:

        import json

        data = json.loads(content)

        items = (
            data
            .get("data", {})
            .get("hits", {})
            .get("items", [])
        )

        schemes = []

        for item in items:

            fields = item.get(
                "fields",
                {}
            )

            scheme_id = item.get(
                "id"
            )

            scheme_name = fields.get(
                "schemeName"
            )

            if not scheme_name:
                continue

            states = fields.get(
                "beneficiaryState",
                []
            )

            categories = fields.get(
                "schemeCategory",
                []
            )

            tags = fields.get(
                "tags",
                []
            )

            tags = [
                tag
                for tag in tags
                if tag
            ]

            slug = fields.get(
                "slug"
            )

            official_source = (
                f"https://www.myscheme.gov.in/"
                f"schemes/{slug}"
                if slug
                else "https://www.myscheme.gov.in/"
            )

            schemes.append({

                "id": scheme_id,

                "name": scheme_name,

                "category": (
                    categories[0]
                    if categories
                    else "general"
                ),

                "categories": categories,

                "description": (
                    fields.get(
                        "briefDescription"
                    )
                    or ""
                ),

                "target_users": [],

                "states": states,

                "eligibility": {},

                "benefits": [],

                "documents": [],

                "application_steps": [],

                "official_source":
                    official_source,

                "source_name":
                    "myScheme",

                "authority":
                    fields.get(
                        "nodalMinistryName"
                    )
                    or "Government of India",

                "nodal_ministry":
                    fields.get(
                        "nodalMinistryName"
                    ),

                "level":
                    fields.get(
                        "level"
                    ),

                "tags":
                    tags,

                "slug":
                    slug,

                "scheme_close_date":
                    fields.get(
                        "schemeCloseDate"
                    ),

                "last_verified":
                    None,

                "verification_status":
                    "verified",

                "confidence":
                    0.95
            })

        return schemes

    def search(
        self,
        query: str
    ) -> list[dict]:

        params = {
            "lang": "en",
            "q": "[]",
            "keyword": query,
            "sort": "",
            "from": 0,
            "size": 10
        }

        headers = {
            "accept": "application/json",
            "origin": "https://www.myscheme.gov.in",
            "x-api-key": self.api_key,
            "user-agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/151.0.0.0 Safari/537.36"
            )
        }

        response = requests.get(
            self.api_url,
            params=params,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        items = (
            data
            .get("data", {})
            .get("hits", {})
            .get("items", [])
        )

        results = []

        for item in items:

            fields = item.get(
                "fields",
                {}
            )

            results.append({

                "id":
                    item.get("id"),

                "name":
                    fields.get("schemeName"),

                "category":
                    (
                        fields.get(
                            "schemeCategory"
                        ) or ["general"]
                    )[0],

                "categories":
                    fields.get(
                        "schemeCategory"
                    ) or [],

                "description":
                    fields.get(
                        "briefDescription"
                    ) or "",

                "states":
                    fields.get(
                        "beneficiaryState"
                    ) or [],

                "official_source":
                    (
                        "https://www.myscheme.gov.in/"
                        "schemes/"
                        + fields.get("slug", "")
                    ),

                "source_name":
                    "myScheme",

                "authority":
                    fields.get(
                        "nodalMinistryName"
                    ) or "Government of India",

                "nodal_ministry":
                    fields.get(
                        "nodalMinistryName"
                    ),

                "level":
                    fields.get("level"),

                "tags":
                    [
                        x
                        for x in (
                            fields.get("tags")
                            or []
                        )
                        if x
                    ],

                "slug":
                    fields.get("slug"),

                "scheme_close_date":
                    fields.get(
                        "schemeCloseDate"
                    ),

                "verification_status":
                    "verified",

                "confidence":
                    0.95
            })

        return results