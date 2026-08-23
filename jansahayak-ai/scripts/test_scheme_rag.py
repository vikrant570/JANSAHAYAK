from app.services.scheme_rag import SchemeRAG


def main():

    rag = SchemeRAG()

    queries = [
        "farmer financial assistance",
        "student scholarship",
        "health insurance",
        "business loan"
    ]

    for query in queries:

        print("\n" + "=" * 70)
        print("QUERY:", query)
        print("=" * 70)

        results = rag.search(
            query,
            top_k=3
        )

        for i, scheme in enumerate(
            results,
            start=1
        ):

            print(
                f"\n{i}. {scheme['name']}"
            )

            print(
                "Category:",
                scheme.get("category")
            )

            print(
                "State:",
                scheme.get("states")
            )

            print(
                "Score:",
                round(
                    scheme["retrieval_score"],
                    4
                )
            )

            print(
                "Source:",
                scheme.get("official_source")
            )


if __name__ == "__main__":
    main()