import json
import requests
from bs4 import BeautifulSoup


def main():

    print("=" * 70)
    print("JANSAHAYAK - SCHEME DETAIL PAGE INSPECTION")
    print("=" * 70)

    # ---------------------------------------------------------
    # LOAD REAL DATASET
    # ---------------------------------------------------------

    with open(
        "data/schemes.json",
        "r",
        encoding="utf-8"
    ) as file:

        schemes = json.load(file)

    print(
        f"\nTotal schemes available: {len(schemes)}"
    )

    # ---------------------------------------------------------
    # SELECT FIRST SCHEME WITH OFFICIAL URL
    # ---------------------------------------------------------

    scheme = None

    for item in schemes:

        url = item.get("official_source")

        if url:

            scheme = item
            break

    if not scheme:

        print("No scheme with official URL found.")
        return

    print("\nSCHEME")
    print("-" * 70)
    print("Name:", scheme.get("name"))
    print("Source:", scheme.get("source_name"))
    print("URL:", scheme.get("official_source"))

    url = scheme["official_source"]

    # ---------------------------------------------------------
    # FETCH PAGE
    # ---------------------------------------------------------

    print("\nFetching official scheme page...")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/151.0 Safari/537.36"
        )
    }

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
        "Content Length:",
        len(response.text)
    )

    # ---------------------------------------------------------
    # PARSE HTML
    # ---------------------------------------------------------

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    title = soup.title

    print("\nPAGE TITLE")
    print("-" * 70)

    if title:

        print(
            title.get_text(
                " ",
                strip=True
            )
        )

    else:

        print("No title found.")

    # ---------------------------------------------------------
    # SEARCH FOR DOCUMENT-RELATED TEXT
    # ---------------------------------------------------------

    print("\nDOCUMENT-RELATED TEXT")
    print("-" * 70)

    text = soup.get_text(
        "\n",
        strip=True
    )

    keywords = [
        "Documents Required",
        "Documents required",
        "Required Documents",
        "documents required",
        "Documents"
    ]

    found = False

    for keyword in keywords:

        if keyword.lower() in text.lower():

            print(
                f"FOUND KEYWORD: {keyword}"
            )

            found = True

    if not found:

        print(
            "No document heading found in "
            "server-rendered HTML."
        )

    # ---------------------------------------------------------
    # SAVE HTML FOR INSPECTION
    # ---------------------------------------------------------

    output_file = (
        "data/scheme_detail_debug.html"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            response.text
        )

    print(
        "\nRaw HTML saved to:",
        output_file
    )


if __name__ == "__main__":
    main()