import json
from pathlib import Path

from app.connectors.india_gov import IndiaGovConnector
from app.connectors.myscheme import MySchemeConnector
from app.services.scheme_normalizer import SchemeNormalizer


OUTPUT_FILE = Path("data/schemes.json")


def main():
    print("=" * 70)
    print("JANSAHAYAK - BUILD REAL SCHEME DATASET")
    print("=" * 70)

    normalizer = SchemeNormalizer()

    # ---------------------------------------------------------
    # INDIA.GOV.IN
    # ---------------------------------------------------------
    print("\nFetching schemes from India.gov.in...")

    india = IndiaGovConnector()

    try:
        india_results = india.search(
            query=""
        )

        print(
            f"India.gov.in schemes received: "
            f"{len(india_results)}"
        )

    except Exception as error:
        print(
            "India.gov.in error:",
            error
        )
        india_results = []

    # ---------------------------------------------------------
    # MYSCHEME.GOV.IN
    # ---------------------------------------------------------
    print("\nFetching schemes from MyScheme...")

    myscheme = MySchemeConnector()

    try:
        myscheme_results = myscheme.search(
            query=""
        )

        print(
            f"MyScheme schemes received: "
            f"{len(myscheme_results)}"
        )

    except Exception as error:
        print(
            "MyScheme error:",
            error
        )
        myscheme_results = []

    # ---------------------------------------------------------
    # NORMALIZE
    # ---------------------------------------------------------
    all_schemes = []

    for raw in india_results:
        try:
            normalized = normalizer.normalize(raw)
            all_schemes.append(normalized)
        except Exception as error:
            print(
                "India normalization error:",
                error
            )

    for raw in myscheme_results:
        try:
            normalized = normalizer.normalize(raw)
            all_schemes.append(normalized)
        except Exception as error:
            print(
                "MyScheme normalization error:",
                error
            )

    print(
        f"\nTotal normalized schemes: "
        f"{len(all_schemes)}"
    )

    # ---------------------------------------------------------
    # DEDUPLICATION
    # ---------------------------------------------------------
    unique = {}

    for scheme in all_schemes:

        name = (
            scheme.get("name")
            or ""
        ).strip()

        if not name:
            continue

        key = name.lower()

        if key not in unique:
            unique[key] = scheme

        else:
            existing = unique[key]

            # Prefer the record with more information
            existing_score = len(
                existing.get("description", "")
            )

            new_score = len(
                scheme.get("description", "")
            )

            if new_score > existing_score:
                unique[key] = scheme

    final_schemes = list(
        unique.values()
    )

    # ---------------------------------------------------------
    # SAFETY CHECK
    # ---------------------------------------------------------
    final_schemes = [
        scheme
        for scheme in final_schemes
        if scheme.get("name")
        and scheme.get("name").lower()
        != "example scheme"
    ]

    # ---------------------------------------------------------
    # SAVE
    # ---------------------------------------------------------
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            final_schemes,
            file,
            indent=2,
            ensure_ascii=False
        )

    print(
        "\nFinal unique schemes:",
        len(final_schemes)
    )

    print(
        "\nSaved to:",
        OUTPUT_FILE
    )

    # ---------------------------------------------------------
    # PREVIEW
    # ---------------------------------------------------------
    print("\nFirst 5 schemes:")

    for index, scheme in enumerate(
        final_schemes[:5],
        start=1
    ):

        print(
            f"{index}. "
            f"{scheme['name']}"
        )

        print(
            f"   Source: "
            f"{scheme.get('source_name')}"
        )

        print(
            f"   URL: "
            f"{scheme.get('official_source')}"
        )


if __name__ == "__main__":
    main()