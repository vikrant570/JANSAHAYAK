from app.connectors.myscheme import MySchemeConnector
from app.services.scheme_normalizer import SchemeNormalizer


def main():

    print("=" * 70)
    print("JANSAHAYAK - REAL SCHEME PIPELINE TEST")
    print("=" * 70)

    connector = MySchemeConnector()
    normalizer = SchemeNormalizer()

    queries = [
        "farmer",
        "scholarship",
        "agriculture",
        "student",
        "business"
    ]

    for query in queries:

        print("\n" + "=" * 70)
        print(f"QUERY: {query}")
        print("=" * 70)

        try:

            results = connector.search(
                query=query,
                page_size=10
            )

            print(
                f"Raw schemes received: {len(results)}"
            )

            for index, raw in enumerate(results[:5], 1):

                scheme = normalizer.normalize(raw)

                print("\n" + "-" * 60)
                print(f"{index}. {scheme['name']}")
                print(f"Category: {scheme['category']}")
                print(f"State: {scheme['states']}")
                print(f"Ministry: {scheme.get('nodal_ministry')}")
                print(f"Level: {scheme.get('level')}")
                print(f"Source: {scheme['official_source']}")
                print(
                    f"Verification: "
                    f"{scheme['verification_status']}"
                )
                print(
                    f"Confidence: "
                    f"{scheme['confidence']}"
                )

        except Exception as error:

            print(
                f"ERROR: {type(error).__name__}: {error}"
            )


if __name__ == "__main__":
    main()