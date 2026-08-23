import requests
from typing import Any


class OfficialSourceClient:

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

            "Accept": (
                "application/json, "
                "text/plain, */*"
            ),

            "Accept-Language":
                "en-GB,en-US;q=0.9,en;q=0.8"
        })

    def get(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None
    ):

        request_headers = {}

        if headers:
            request_headers.update(headers)

        response = self.session.get(
            url,
            params=params,
            headers=request_headers,
            timeout=30
        )

        response.raise_for_status()

        return response

    def post_json(
        self,
        url: str,
        payload: dict[str, Any],
        headers: dict[str, str] | None = None
    ):

        request_headers = {
            "Content-Type":
                "application/json"
        }

        if headers:
            request_headers.update(headers)

        response = self.session.post(
            url,
            json=payload,
            headers=request_headers,
            timeout=30
        )

        response.raise_for_status()

        return response