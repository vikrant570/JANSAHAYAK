import json
import requests
from bs4 import BeautifulSoup


def main():

    print("=" * 70)
    print("JANSAHAYAK - MYSCHEME DETAIL INSPECTION")
    print("=" * 70)

    with open(
        "data/schemes.json",
        "r",
        encoding="utf-8"
    ) as file:

        schemes = json.load(file)

    scheme = None

    for item in schemes:

        if (
            item.get("source_name") == "myScheme"
            and item.get("official_source")
        ):

            scheme = item
            break

    if not scheme:

        print(
            "No MyScheme record found."
        )
        return

    print("\nScheme:")
    print(scheme.get("name"))

    print("\nURL:")
    print(scheme.get("official_source"))

    url = scheme["official_source"]

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/151.0 Safari/537.36"
        )
    }

    print("\nFetching...")

    response = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    print(
        "HTTP Status:",
        response.status_code
    )

    print(
        "Final URL:",
        response.url
    )

    print(
        "HTML Length:",
        len(response.text)
    )

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    page_text = soup.get_text(
        "\n",
        strip=True
    )

    # ---------------------------------------------------------
    # SEARCH IMPORTANT SECTIONS
    # ---------------------------------------------------------

    sections = [
        "Documents Required",
        "Documents",
        "Eligibility",
        "Benefits",
        "Application Process",
        "How to Apply",
        "Application Procedure"
    ]

    print("\nSECTION CHECK")
    print("-" * 70)

    for section in sections:

        if section.lower() in page_text.lower():

            print(
                f"[FOUND] {section}"
            )

        else:

            print(
                f"[NOT FOUND] {section}"
            )

    # ---------------------------------------------------------
    # SAVE PAGE
    # ---------------------------------------------------------

    output = (
        "data/myscheme_detail_debug.html"
    )

    with open(
        output,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            response.text
        )

    print(
        "\nSaved HTML:",
        output
    )


if __name__ == "__main__":
    main()