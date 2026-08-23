from app.connectors.india_gov import (
    IndiaGovConnector
)


def main():

    print("=" * 70)
    print("JANSAHAYAK - INDIA.GOV.IN API TEST")
    print("=" * 70)

    connector = IndiaGovConnector()

    print("\nFetching schemes...")

    results = connector.search(
        query="",
        page_size=10
    )

    print(
        f"\nSchemes received: "
        f"{len(results)}"
    )

    for i, scheme in enumerate(
        results,
        start=1
    ):

        print("\n" + "-" * 60)

        print(
            f"{i}. {scheme['name']}"
        )

        print(
            f"Category: "
            f"{scheme['category']}"
        )

        print(
            f"State: "
            f"{scheme['states']}"
        )

        print(
            f"Description: "
            f"{scheme['description'][:200]}"
        )

        print(
            f"Source: "
            f"{scheme['official_source']}"
        )

        print(
            f"Source Name: "
            f"{scheme['source_name']}"
        )


if __name__ == "__main__":
    main()