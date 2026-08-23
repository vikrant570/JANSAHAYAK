import os

from dotenv import load_dotenv

# Load .env BEFORE creating the connectors
load_dotenv()

from app.connectors.india_gov import IndiaGovConnector
from app.connectors.myscheme import MySchemeConnector


def test_connector(name, connector):

    print("\n" + "=" * 70)
    print(name)
    print("=" * 70)

    print("Configured URL:", connector.url)

    if not connector.url:

        print(
            "ERROR: URL is empty."
            " Check .env and load_dotenv()."
        )

        return

    try:

        content = connector.fetch(
            connector.url
        )

        print(
            "Downloaded characters:",
            len(content)
        )

        print("\nFirst 500 characters:")
        print("-" * 70)
        print(content[:500])
        print("-" * 70)

        results = connector.extract(
            content,
            query="farmer"
        )

        print(
            "\nExtracted records:",
            len(results)
        )

        for index, result in enumerate(
            results[:5],
            start=1
        ):

            print(
                f"\n--- Result {index} ---"
            )

            print(
                "Name:",
                result.get("name")
            )

            print(
                "Source:",
                result.get(
                    "official_source"
                )
            )

            print(
                "Description:",
                result.get(
                    "description",
                    ""
                )[:300]
            )

    except Exception as error:

        print(
            "ERROR:",
            type(error).__name__,
            str(error)
        )


if __name__ == "__main__":

    print(
        "INDIA_GOV_SCHEME_URL:",
        os.getenv(
            "INDIA_GOV_SCHEME_URL"
        )
    )

    print(
        "MYSCHEME_SCHEME_URL:",
        os.getenv(
            "MYSCHEME_SCHEME_URL"
        )
    )

    test_connector(
        "INDIA.GOV.IN",
        IndiaGovConnector()
    )

    test_connector(
        "MYSCHEME.GOV.IN",
        MySchemeConnector()
    )