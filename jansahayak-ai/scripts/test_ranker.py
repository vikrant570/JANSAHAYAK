from app.connectors.myscheme import MySchemeConnector
from app.services.scheme_normalizer import SchemeNormalizer
from app.services.scheme_ranker import rank_schemes


def main():

    print("=" * 70)
    print("JANSAHAYAK - SCHEME RANKING TEST")
    print("=" * 70)

    connector = MySchemeConnector()

    normalizer = SchemeNormalizer()

    query = (
        "I am a small farmer from Punjab. "
        "What government support can I get?"
    )

    print("\nQUERY:")
    print(query)

    print("\nFetching schemes...")

    raw_results = connector.search(
        query="farmer",
        page_size=20
    )

    schemes = [
        normalizer.normalize(item)
        for item in raw_results
    ]

    print(
        f"Retrieved: {len(schemes)} schemes"
    )

    ranked = rank_schemes(
        schemes=schemes,
        query=query,
        user_type="farmer",
        state="Punjab",
        category="agriculture"
    )

    print("\n")
    print("=" * 70)
    print("TOP RANKED SCHEMES")
    print("=" * 70)

    for index, scheme in enumerate(
        ranked[:10],
        1
    ):

        print("\n" + "-" * 60)

        print(
            f"{index}. {scheme['name']}"
        )

        print(
            f"Score: "
            f"{scheme['relevance_score']}"
        )

        print(
            f"Category: "
            f"{scheme['category']}"
        )

        print(
            f"States: "
            f"{scheme['states']}"
        )

        print(
            f"Level: "
            f"{scheme.get('level', '')}"
        )

        print(
            f"Source: "
            f"{scheme['official_source']}"
        )


if __name__ == "__main__":
    main()