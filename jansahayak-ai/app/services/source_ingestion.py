import json
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup


BASE_DIR = Path(__file__).resolve().parents[2]

SOURCES_FILE = (
    BASE_DIR / "data" / "sources.json"
)


def load_sources():

    with open(
        SOURCES_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def fetch_page(url: str) -> str:

    response = requests.get(
        url,
        timeout=20,
        headers={
            "User-Agent": (
                "JanSahayakAI/1.0 "
                "(government information "
                "research service)"
            )
        }
    )

    response.raise_for_status()

    return response.text


def extract_text(
    html: str
) -> str:

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    # Remove unnecessary elements
    for element in soup([
        "script",
        "style",
        "noscript"
    ]):

        element.decompose()

    text = soup.get_text(
        separator=" ",
        strip=True
    )

    return text


def fetch_source(
    source: dict
) -> dict:

    url = source["base_url"]

    html = fetch_page(url)

    text = extract_text(
        html
    )

    return {
        "source_name": source["name"],
        "source_url": url,
        "authority": source["authority"],
        "content": text,
        "retrieved_at": datetime.now(
            timezone.utc
        ).isoformat()
    }


def ingest_sources():

    sources = load_sources()

    results = []

    for source in sources:

        if not source.get(
            "enabled",
            True
        ):
            continue

        try:

            result = fetch_source(
                source
            )

            results.append(
                result
            )

            print(
                f"[SUCCESS] "
                f"{source['name']}"
            )

        except Exception as error:

            print(
                f"[FAILED] "
                f"{source['name']}: "
                f"{error}"
            )

    return results