from app.connectors.india_gov import IndiaGovConnector
from app.connectors.myscheme import MySchemeConnector

from app.services.scheme_pipeline import (
    SchemePipeline
)


def main():

    print("=" * 70)
    print("JANSAHAYAK - COMBINED REAL SCHEME PIPELINE")
    print("=" * 70)

    connectors = [
        IndiaGovConnector(),
        MySchemeConnector()
    ]

    pipeline = SchemePipeline(
        connectors
    )

    queries = [
        "farmer",
        "scholarship",
        "student",
        "agriculture",
        "business"
    ]

    for query in queries:

        print(
            "\n" + "=" * 70
        )

        print(
            f"QUERY: {query}"
        )

        print(
            "=" * 70
        )

        schemes = pipeline.search(
            query
        )

        print(
            f"Unique schemes: "
            f"{len(schemes)}"
        )

        for i, scheme in enumerate(
            schemes[:10],
            start=1
        ):

            print(
                f"\n{i}. "
                f"{scheme.get('name')}"
            )

            print(
                f"Category: "
                f"{scheme.get('category')}"
            )

            print(
                f"State: "
                f"{scheme.get('states')}"
            )

            print(
                f"Source: "
                f"{scheme.get('source_name')}"
            )

            print(
                f"Official URL: "
                f"{scheme.get('official_source')}"
            )

            print(
                f"Confidence: "
                f"{scheme.get('confidence')}"
            )


if __name__ == "__main__":
    main()