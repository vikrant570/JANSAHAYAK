from app.services.profile_extractor import ProfileExtractor
from app.services.scheme_rag import SchemeRAG


def main():

    print("=" * 80)
    print("JANSAHAYAK AI")
    print("=" * 80)

    print(
        "\nTell me about your problem and what kind of government assistance you need."
    )

    print(
        "\nExample:"
    )

    print(
        "I am a 21 year old farmer from Punjab with an annual income "
        "of 2.5 lakh and I need financial assistance for farming."
    )

    print("\n")

    user_query = input(
        "You: "
    )

    print(
        "\nUnderstanding your situation..."
    )

    extractor = ProfileExtractor()

    profile = extractor.extract(
        user_query
    )

    print(
        "\nUSER PROFILE"
    )

    print("-" * 80)

    for key, value in profile.items():

        print(
            f"{key}: {value}"
        )

    print(
        "\nSearching verified government schemes..."
    )

    # Your existing RAG object
    rag = SchemeRAG()

    results = rag.search(
        user_query,
        top_k=5
    )

    print(
        "\nRECOMMENDED GOVERNMENT SCHEMES"
    )

    print("=" * 80)

    for index, scheme in enumerate(
        results,
        start=1
    ):

        print(
            f"\n{index}. {scheme.get('name')}"
        )

        print(
            "-" * 60
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
            "Description:",
            scheme.get("description")
        )

        print(
            "Official Source:",
            scheme.get("official_source")
        )


if __name__ == "__main__":
    main()