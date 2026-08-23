from app.services.scheme_search import SchemeSearchService


def main():

    print("=" * 70)
    print("JANSAHAYAK - REAL SCHEME SEARCH")
    print("=" * 70)

    service = SchemeSearchService()

    queries = [
        "farmer",
        "scholarship",
        "student",
        "business"
    ]

    for query in queries:

        print("\n" + "=" * 70)
        print(f"QUERY: {query}")
        print("=" * 70)

        results = service.search(
            query=query,
            page_size=5
        )

        print(
            f"Schemes found: {len(results)}"
        )

        for i, scheme in enumerate(
            results,
            start=1
        ):

            print(
                f"\n{i}. {scheme['name']}"
            )

            print(
                f"Category: {scheme['category']}"
            )

            print(
                f"State: {scheme['states']}"
            )

            print(
                f"Source: {scheme['official_source']}"
            )

            print(
                f"Verification: "
                f"{scheme['verification_status']}"
            )


if __name__ == "__main__":
    main()