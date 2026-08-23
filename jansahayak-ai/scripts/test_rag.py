from app.services.scheme_rag import SchemeRAG


def main():

    rag = SchemeRAG()

    queries = [

        "I am a farmer. What government schemes can help me?",

        "I am a student looking for scholarship assistance.",

        "I need government support for agriculture.",

        "What government financial assistance is available?"
    ]

    for query in queries:

        print()
        print("=" * 70)

        print(
            f"QUERY: {query}"
        )

        print("=" * 70)

        results = rag.search(
            query,
            top_k=5
        )

        if not results:

            print(
                "No relevant verified schemes found."
            )

            continue

        for i, scheme in enumerate(
            results,
            start=1
        ):

            print()
            print(
                f"{i}. {scheme.get('name')}"
            )

            print(
                f"Category: "
                f"{scheme.get('category')}"
            )

            print(
                f"Score: "
                f"{scheme.get('retrieval_score')}"
            )

            print(
                f"Source: "
                f"{scheme.get('official_source')}"
            )


if __name__ == "__main__":

    main()