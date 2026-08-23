import json
from pathlib import Path

from app.connectors.india_gov import IndiaGovConnector
from app.connectors.myscheme import MySchemeConnector
from app.services.scheme_normalizer import SchemeNormalizer


OUTPUT_FILE = Path("data/schemes.json")

# =============================================================
# TARGET DATASET SIZE
# =============================================================

TARGET_SCHEMES = 100


# =============================================================
# SEARCH QUERIES
# =============================================================
#
# Multiple categories give JanSahayak a balanced knowledge base
# instead of getting only whatever schemes are returned by query=""
#

SEARCH_QUERIES = [
    "",

    # Agriculture
    "farmer",
    "agriculture",
    "kisan",
    "crop",
    "irrigation",

    # Education
    "student",
    "scholarship",
    "education",

    # Business
    "business",
    "entrepreneur",
    "startup",
    "self employment",

    # Women
    "women",
    "girl",
    "widow",

    # Employment
    "employment",
    "skill development",
    "unemployed",

    # Health
    "health",
    "medical",
    "insurance",

    # Housing
    "housing",
    "awas",

    # Pension / Senior citizens
    "pension",
    "senior citizen",

    # Disability
    "disability",
    "divyang",

    # General welfare
    "financial assistance",
    "social welfare",
]


def fetch_from_connector(
    connector,
    source_name: str
) -> list:

    """
    Run multiple category searches against one official
    connector and collect all returned records.
    """

    collected = []

    print(
        f"\n{'=' * 70}"
    )

    print(
        f"FETCHING FROM {source_name.upper()}"
    )

    print(
        f"{'=' * 70}"
    )

    for query in SEARCH_QUERIES:

        display_query = (
            query
            if query
            else "<general>"
        )

        print(
            f"\nSearching: {display_query}"
        )

        try:

            results = connector.search(
                query=query
            )

            if not isinstance(
                results,
                list
            ):
                results = []

            print(
                f"Received: {len(results)}"
            )

            collected.extend(
                results
            )

        except Exception as error:

            print(
                f"{source_name} search error "
                f"for '{display_query}':",
                error
            )

    print(
        f"\nTotal raw {source_name} records collected: "
        f"{len(collected)}"
    )

    return collected


def normalize_results(
    raw_results: list,
    normalizer: SchemeNormalizer,
    source_name: str
) -> list:

    """
    Normalize raw connector records into the common
    JanSahayak scheme structure.
    """

    normalized_results = []

    for raw in raw_results:

        try:

            normalized = normalizer.normalize(
                raw
            )

            if (
                isinstance(normalized, dict)
                and normalized.get("name")
            ):

                normalized_results.append(
                    normalized
                )

        except Exception as error:

            print(
                f"{source_name} normalization error:",
                error
            )

    return normalized_results


def information_score(
    scheme: dict
) -> int:

    """
    Used during deduplication.

    If the same scheme is returned from multiple searches,
    keep the version containing more useful information.
    """

    score = 0

    fields = [
        "description",
        "category",
        "benefits",
        "documents",
        "eligibility",
        "official_source",
    ]

    for field in fields:

        value = scheme.get(
            field
        )

        if isinstance(
            value,
            str
        ):

            score += len(
                value.strip()
            )

        elif isinstance(
            value,
            list
        ):

            score += (
                len(value) * 20
            )

        elif isinstance(
            value,
            dict
        ):

            score += (
                len(value) * 20
            )

    return score


def deduplicate_schemes(
    schemes: list
) -> list:

    """
    Remove duplicate scheme names.

    Example:
    a farmer scheme may appear in searches for:
    farmer, agriculture, kisan and financial assistance.

    It should still exist only once in schemes.json.
    """

    unique = {}

    for scheme in schemes:

        if not isinstance(
            scheme,
            dict
        ):
            continue

        name = str(
            scheme.get(
                "name",
                ""
            )
        ).strip()

        if not name:
            continue

        if (
            name.lower()
            == "example scheme"
        ):
            continue

        key = name.lower()

        if key not in unique:

            unique[key] = scheme

        else:

            existing = unique[
                key
            ]

            existing_score = (
                information_score(
                    existing
                )
            )

            new_score = (
                information_score(
                    scheme
                )
            )

            if new_score > existing_score:

                unique[key] = (
                    scheme
                )

    return list(
        unique.values()
    )


def main():

    print(
        "=" * 70
    )

    print(
        "JANSAHAYAK - BUILD EXPANDED REAL SCHEME DATASET"
    )

    print(
        "=" * 70
    )

    print(
        f"\nTarget: approximately "
        f"{TARGET_SCHEMES} verified schemes"
    )

    normalizer = (
        SchemeNormalizer()
    )

    # =========================================================
    # CONNECTORS
    # =========================================================

    india = (
        IndiaGovConnector()
    )

    myscheme = (
        MySchemeConnector()
    )

    # =========================================================
    # FETCH INDIA.GOV.IN
    # =========================================================

    india_results = (
        fetch_from_connector(
            connector=india,
            source_name="India.gov.in"
        )
    )

    # =========================================================
    # FETCH MYSCHEME
    # =========================================================

    myscheme_results = (
        fetch_from_connector(
            connector=myscheme,
            source_name="MyScheme"
        )
    )

    # =========================================================
    # NORMALIZE INDIA
    # =========================================================

    print(
        "\nNormalizing India.gov.in records..."
    )

    normalized_india = (
        normalize_results(
            raw_results=india_results,
            normalizer=normalizer,
            source_name="India.gov.in"
        )
    )

    print(
        f"India normalized: "
        f"{len(normalized_india)}"
    )

    # =========================================================
    # NORMALIZE MYSCHEME
    # =========================================================

    print(
        "\nNormalizing MyScheme records..."
    )

    normalized_myscheme = (
        normalize_results(
            raw_results=myscheme_results,
            normalizer=normalizer,
            source_name="MyScheme"
        )
    )

    print(
        f"MyScheme normalized: "
        f"{len(normalized_myscheme)}"
    )

    # =========================================================
    # MERGE
    # =========================================================

    all_schemes = (
        normalized_india
        +
        normalized_myscheme
    )

    print(
        f"\nTotal normalized before deduplication: "
        f"{len(all_schemes)}"
    )

    # =========================================================
    # DEDUPLICATE
    # =========================================================

    final_schemes = (
        deduplicate_schemes(
            all_schemes
        )
    )

    print(
        f"Unique schemes after deduplication: "
        f"{len(final_schemes)}"
    )

    # =========================================================
    # VERIFIED SCHEMES
    # =========================================================
    #
    # Your SchemeRetriever only uses schemes where:
    #
    # verification_status == "verified"
    #
    # Therefore these are the schemes that actually become
    # available to FAISS.
    #

    verified_schemes = [
        scheme
        for scheme in final_schemes
        if (
            scheme.get(
                "verification_status"
            )
            == "verified"
        )
    ]

    print(
        f"Verified schemes available: "
        f"{len(verified_schemes)}"
    )

    # =========================================================
    # LIMIT TO TARGET
    # =========================================================

    if len(
        verified_schemes
    ) > TARGET_SCHEMES:

        verified_schemes = (
            verified_schemes[
                :TARGET_SCHEMES
            ]
        )

    # =========================================================
    # SAVE
    # =========================================================

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
            verified_schemes,
            file,
            indent=2,
            ensure_ascii=False
        )

    # =========================================================
    # FINAL REPORT
    # =========================================================

    print(
        "\n"
        + "=" * 70
    )

    print(
        "DATASET BUILD COMPLETE"
    )

    print(
        "=" * 70
    )

    print(
        "\nFinal schemes saved:",
        len(verified_schemes)
    )

    print(
        "Saved to:",
        OUTPUT_FILE
    )

    if (
        len(verified_schemes)
        < TARGET_SCHEMES
    ):

        print(
            "\nWARNING:"
        )

        print(
            f"Target was {TARGET_SCHEMES}, "
            f"but only {len(verified_schemes)} "
            "unique verified schemes were available."
        )

        print(
            "This usually means one or both connectors "
            "return a limited number of results per search."
        )

    # =========================================================
    # PREVIEW
    # =========================================================

    print(
        "\nFirst 10 schemes:"
    )

    for index, scheme in enumerate(
        verified_schemes[:10],
        start=1
    ):

        print(
            f"\n{index}. "
            f"{scheme.get('name')}"
        )

        print(
            "   Source:",
            scheme.get(
                "source_name"
            )
        )

        print(
            "   Verification:",
            scheme.get(
                "verification_status"
            )
        )

        print(
            "   URL:",
            scheme.get(
                "official_source"
            )
        )


if __name__ == "__main__":
    main()