import requests
from bs4 import BeautifulSoup


class SourceFetcher:

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
                "text/html,"
                "application/xhtml+xml,"
                "application/xml;q=0.9,"
                "image/avif,"
                "image/webp,"
                "*/*;q=0.8"
            ),

            "Accept-Language":
                "en-US,en;q=0.9",

            "Connection":
                "keep-alive"
        })

    def fetch(
        self,
        url: str
    ) -> str:

        response = self.session.get(
            url,
            timeout=30,
            allow_redirects=True
        )

        print(
            "HTTP STATUS:",
            response.status_code
        )

        print(
            "FINAL URL:",
            response.url
        )

        response.raise_for_status()

        return response.text

    def extract_text(
        self,
        html: str
    ) -> str:

        soup = BeautifulSoup(
            html,
            "lxml"
        )

        for tag in soup([
            "script",
            "style",
            "noscript",
            "header",
            "footer"
        ]):

            tag.decompose()

        return soup.get_text(
            separator=" ",
            strip=True
        )

    def fetch_text(
        self,
        url: str
    ) -> str:

        html = self.fetch(url)

        return self.extract_text(
            html
        )