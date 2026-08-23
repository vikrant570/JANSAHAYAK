import json

from app.services.scheme_detail_pipeline import (
    SchemeDetailPipeline
)


def main():

    print("=" * 70)
    print("JANSAHAYAK - COMPLETE DETAIL PIPELINE TEST")
    print("=" * 70)

    with open(
        "data/schemes.json",
        "r",
        encoding="utf-8"
    ) as file:

        schemes = json.load(file)

    if not schemes:

        print(
            "No schemes found."
        )

        return

    pipeline = (
        SchemeDetailPipeline()
    )

    # Test first scheme
    scheme = schemes[0]

    print("\nScheme:")
    print(
        scheme.get("name")
    )

    print("\nSource:")
    print(
        scheme.get("official_source")
    )

    result = pipeline.enrich(
        scheme
    )

    print("\nSTATUS")
    print("-" * 70)

    print(
        "HTTP:",
        result.get(
            "detail_http_status"
        )
    )

    print(
        "Status:",
        result.get(
            "detail_status"
        )
    )

    print("\nDOCUMENTS")
    print("-" * 70)

    documents = result.get(
        "documents",
        []
    )

    if documents:

        for i, document in enumerate(
            documents,
            1
        ):

            print(
                f"{i}. {document}"
            )

    else:

        print(
            "No verified document information found."
        )

    print("\nELIGIBILITY TEXT")
    print("-" * 70)

    print(
        result.get(
            "eligibility_text",
            ""
        )[:1000]
    )

    print("\nBENEFITS TEXT")
    print("-" * 70)

    print(
        result.get(
            "benefits_text",
            ""
        )[:1000]
    )

    print("\nAPPLICATION TEXT")
    print("-" * 70)

    print(
        result.get(
            "application_steps_text",
            ""
        )[:1000]
    )

    print("\n" + "=" * 70)
    print("DETAIL PIPELINE TEST COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()