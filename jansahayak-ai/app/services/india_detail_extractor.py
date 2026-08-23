import requests
from bs4 import BeautifulSoup


class IndiaDetailExtractor:

    def __init__(self):
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/151.0 Safari/537.36"
            )
        }

    def extract(
        self,
        scheme: dict
    ) -> dict:

        url = (
            scheme.get("official_source")
            or ""
        ).strip()

        result = {
            "status": "not_found",
            "http_status": None,
            "final_url": url,
            "documents": [],
            "eligibility": [],
            "benefits": [],
            "application_steps": [],
            "document_text": "",
            "eligibility_text": "",
            "benefits_text": "",
            "application_text": "",
            "verified": False
        }

        if not url:

            result["status"] = "missing_url"

            return result

        try:

            response = requests.get(
                url,
                headers=self.headers,
                timeout=20,
                allow_redirects=True
            )

            result["http_status"] = (
                response.status_code
            )

            result["final_url"] = (
                response.url
            )

            if response.status_code != 200:

                result["status"] = (
                    "http_error"
                )

                return result

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            for tag in soup([
                "script",
                "style",
                "noscript"
            ]):

                tag.decompose()

            text = soup.get_text(
                "\n",
                strip=True
            )

            lower_text = (
                text.lower()
            )

            result["status"] = "success"

            # --------------------------------------------
            # DOCUMENT INFORMATION
            # --------------------------------------------

            document_keywords = [
                "documents required",
                "required documents",
                "documents needed",
                "documents"
            ]

            if any(
                keyword in lower_text
                for keyword in document_keywords
            ):

                result["document_text"] = text

            # --------------------------------------------
            # ELIGIBILITY
            # --------------------------------------------

            eligibility_keywords = [
                "eligibility",
                "eligibility criteria",
                "eligible",
                "who can apply"
            ]

            if any(
                keyword in lower_text
                for keyword in eligibility_keywords
            ):

                result[
                    "eligibility_text"
                ] = text

            # --------------------------------------------
            # BENEFITS
            # --------------------------------------------

            benefit_keywords = [
                "benefits",
                "benefit",
                "financial assistance"
            ]

            if any(
                keyword in lower_text
                for keyword in benefit_keywords
            ):

                result[
                    "benefits_text"
                ] = text

            # --------------------------------------------
            # APPLICATION
            # --------------------------------------------

            application_keywords = [
                "how to apply",
                "application process",
                "application procedure",
                "apply online"
            ]

            if any(
                keyword in lower_text
                for keyword in application_keywords
            ):

                result[
                    "application_text"
                ] = text

            return result

        except requests.RequestException as error:

            result["status"] = (
                "request_error"
            )

            result["error"] = str(
                error
            )

            return result