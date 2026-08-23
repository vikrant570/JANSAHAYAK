from pathlib import Path

from app.services.source_fetcher import SourceFetcher


URLS = {
    "myscheme": "https://www.myscheme.gov.in/",
    "india_gov": "https://www.india.gov.in/my-government/schemes",
}


OUTPUT_DIR = Path("data/raw")


def main():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    fetcher = SourceFetcher()

    for name, url in URLS.items():

        print("\n" + "=" * 80)
        print(f"FETCHING: {name}")
        print("=" * 80)

        try:

            html = fetcher.fetch(url)

            output_file = (
                OUTPUT_DIR / f"{name}.html"
            )

            output_file.write_text(
                html,
                encoding="utf-8"
            )

            print(
                f"Saved to: {output_file}"
            )

            print(
                f"Characters: {len(html)}"
            )

        except Exception as error:

            print(
                f"ERROR: {repr(error)}"
            )


if __name__ == "__main__":
    main()