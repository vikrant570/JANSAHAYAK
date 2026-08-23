from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin


def extract_links(file_path, base_url):

    html = Path(file_path).read_text(
        encoding="utf-8"
    )

    soup = BeautifulSoup(
        html,
        "lxml"
    )

    links = []

    for anchor in soup.find_all("a"):

        href = anchor.get("href")

        text = anchor.get_text(
            " ",
            strip=True
        )

        if not href:
            continue

        full_url = urljoin(
            base_url,
            href
        )

        links.append({
            "text": text,
            "url": full_url
        })

    return links


def main():

    links = extract_links(
        "data/raw/india_gov.html",
        "https://www.india.gov.in/"
    )

    print(
        f"Total links found: {len(links)}"
    )

    print("\nPossible scheme links:\n")

    for link in links:

        text = link["text"].lower()
        url = link["url"].lower()

        if (
            "scheme" in text
            or "scheme" in url
            or "yojana" in text
            or "yojana" in url
        ):

            print(
                f"{link['text']} → {link['url']}"
            )


if __name__ == "__main__":
    main()