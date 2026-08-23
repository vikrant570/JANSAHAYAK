from app.services.query_analyzer import (
    QueryAnalyzer
)


def main():

    analyzer = QueryAnalyzer()

    queries = [

        "I am a 21 year old student from Punjab looking for scholarship",

        "I am a farmer from Punjab and need financial assistance",

        "I want a government loan to start a business",

        "I am looking for employment and skill training"

    ]

    for query in queries:

        print("\n" + "=" * 70)

        print("QUERY:")
        print(query)

        print("\nANALYSIS:")

        result = analyzer.analyze(
            query
        )

        for key, value in result.items():

            print(
                f"{key}: {value}"
            )


if __name__ == "__main__":
    main()