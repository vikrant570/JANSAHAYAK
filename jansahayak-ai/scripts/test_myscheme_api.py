import os

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

    print("=" * 70)
    print("MYSCHEME API TEST")
    print("=" * 70)

    if not url:
        print("ERROR: MYSCHEME_API_URL is missing")
        return

    if not api_key:
        print("ERROR: MYSCHEME_API_KEY is missing")
        return

    print("API:", url)
    print("API key loaded: YES")

    client = OfficialSourceClient()

    params = {
        "lang": "en",
        "q": "[]",
        "keyword": "",
        "sort": "",
        "from": 0,
        "size": 10
    }

    headers = {
        "Origin":
            "https://www.myscheme.gov.in",

        "Referer":
            "https://www.myscheme.gov.in/",

        "x-api-key":
            api_key
    }

    try:

        response = client.get(
            url,
            params=params,
            headers=headers
        )

        print(
            "\nHTTP STATUS:",
            response.status_code
        )

        print(
            "\nFINAL URL:",
            response.url
        )

        print(
            "\nResponse length:",
            len(response.text)
        )

        print("\nResponse:")
        print("-" * 70)

        print(
            response.text[:5000]
        )

        print("-" * 70)

    except Exception as error:

        print(
            "\nERROR:",
            type(error).__name__,
            str(error)
        )


if __name__ == "__main__":
    main()