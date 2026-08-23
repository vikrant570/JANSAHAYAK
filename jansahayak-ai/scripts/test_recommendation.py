from app.connectors.india_gov import (
    IndiaGovConnector
)

from app.connectors.myscheme import (
    MySchemeConnector
)

from app.services.scheme_pipeline import (
    SchemePipeline
)

from app.services.recommendation import (
    SchemeRecommendationEngine
)


def main():

    connectors = [
        IndiaGovConnector(),
        MySchemeConnector()
    ]

    pipeline = SchemePipeline(
        connectors
    )

    engine = (
        SchemeRecommendationEngine(
            pipeline
        )
    )

    queries = [

        "I am a farmer from Punjab and need government assistance",

        "I am a student from Punjab looking for scholarship",

        "I want government support for business"
    ]

    for query in queries:

        print("\n" + "=" * 70)

        print(
            "QUERY:",
            query
        )

        result = engine.recommend(
            query
        )

        print("\nPROFILE:")

        print(
            result["profile"]
        )

        print("\nRECOMMENDED SCHEMES:")

        for i, scheme in enumerate(
            result["schemes"][:5],
            start=1
        ):

            print(
                f"\n{i}. "
                f"{scheme['name']}"
            )

            print(
                "Source:",
                scheme[
                    "source_name"
                ]
            )

            print(
                "State:",
                scheme[
                    "states"
                ]
            )

            print(
                "Score:",
                scheme[
                    "relevance_score"
                ]
            )

            print(
                "URL:",
                scheme[
                    "official_source"
                ]
            )


if __name__ == "__main__":
    main()