import re
from pathlib import Path


def find_urls(text):

    patterns = [
        r'https?://[^\s"\']+',
        r'/api/[^\s"\']+',
        r'api/[^\s"\']+',
    ]

    found = set()

    for pattern in patterns:

        matches = re.findall(
            pattern,
            text
        )

        for match in matches:

            found.add(match)

    return sorted(found)


def inspect_file(path):

    print("\n" + "=" * 80)
    print(f"FILE: {path}")
    print("=" * 80)

    text = Path(path).read_text(
        encoding="utf-8"
    )

    print(
        f"File size: {len(text)} characters"
    )

    urls = find_urls(text)

    print(
        f"\nPossible URLs/endpoints found: {len(urls)}"
    )

    for url in urls:

        print(url)


def main():

    inspect_file(
        "data/raw/myscheme.html"
    )

    inspect_file(
        "data/raw/india_gov.html"
    )


if __name__ == "__main__":
    main()