import os
import json

from dotenv import load_dotenv

load_dotenv()

from app.services.official_source_client import (
    OfficialSourceClient
)


def main():

    url = os.getenv(
        "MYSCHEME_API_URL"
    )

    api_key = os.getenv(
        "MYSCHEME_API_KEY"
    )

    if not url:
        print("ERROR: MYSCHEME_API_URL missing")
        return

    if not api_key:
        print("ERROR: MYSCHEME_API_KEY missing")
        return

    client = OfficialSourceClient()

    response = client.get(
        url,
        params={
            "lang": "en",
            "q": "[]",
            "keyword": "",
            "sort": "",
            "from": 0,
            "size": 10
        },
        headers={
            "Origin":
                "https://www.myscheme.gov.in",

            "Referer":
                "https://www.myscheme.gov.in/",

            "x-api-key":
                api_key
        }
    )

    response.raise_for_status()

    data = response.json()

    api_data = data.get(
        "data",
        {}
    )

    hits = api_data.get(
        "hits",
        {}
    )

    items = hits.get(
        "items",
        []
    )

    print("=" * 70)
    print("MYSCHEME SCHEME RECORD INSPECTION")
    print("=" * 70)

    print(
        "Number of items:",
        len(items)
    )

    if not items:

        print(
            "\nNo scheme items found."
        )

        print(
            "\nHITS OBJECT:"
        )

        print(
            json.dumps(
                hits,
                indent=2,
                ensure_ascii=False
            )[:10000]
        )

        return

    print(
        "\nFirst scheme record:"
    )

    print("-" * 70)

    print(
        json.dumps(
            items[0],
            indent=2,
            ensure_ascii=False
        )
    )

    print("-" * 70)

    print(
        "\nFirst record keys:"
    )

    print(
        list(items[0].keys())
    )


if __name__ == "__main__":
    main()