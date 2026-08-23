from app.services.query_understanding import QueryUnderstanding


def main():

    analyzer = QueryUnderstanding()

    queries = [

        "I need scholarship assistance for my college fees",

        "I am a farmer and need help buying agricultural machinery",

        "I want a government loan to start a small business",

        "I need financial help for medical treatment",

        "I am looking for a government job training scheme"
    ]

    for query in queries:

        print("=" * 70)

        print("QUERY:")
        print(query)

        result = analyzer.understand(
            query
        )

        print(
            "Detected categories:",
            result["categories"]
        )


if __name__ == "__main__":
    main()