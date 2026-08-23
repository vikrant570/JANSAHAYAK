from app.connectors.myscheme import MySchemeConnector
from app.connectors.india_gov import IndiaGovConnector
from app.services.scheme_normalizer import SchemeNormalizer


def print_scheme(scheme: dict):

    print("-" * 70)

    print("ID:", scheme.get("id"))
    print("Name:", scheme.get("name"))
    print("Category:", scheme.get("category"))
    print("Description:", scheme.get("description"))

    print("States:", scheme.get("states"))

    print(
        "Ministry:",
        scheme.get("nodal_ministry")
    )

    print(
        "Level:",
        scheme.get("level")
    )

    print(
        "Source:",
        scheme.get("source_name")
    )

    print(
        "Official URL:",
        scheme.get("official_source")
    )

    print(
        "Verification:",
        scheme.get("verification_status")
    )

    print(
        "Confidence:",
        scheme.get("confidence")
    )


def main():

    print("=" * 70)
    print("JANSAHAYAK - NORMALIZER TEST")
    print("=" * 70)

    normalizer = SchemeNormalizer()

    # =========================================================
    # MYScheme
    # =========================================================

    print("\nFetching real schemes from MyScheme...")

    myscheme = MySchemeConnector()

    try:

        results = myscheme.search(
            query="farmer"
        )

        print(
            "Raw MyScheme records:",
            len(results)
        )

        if results:

            print("\nNORMALIZED MYSCHEME RECORD")

            normalized = normalizer.normalize(
                results[0]
            )

            print_scheme(normalized)

    except Exception as error:

        print(
            "MyScheme error:",
            error
        )

    # =========================================================
    # INDIA.GOV
    # =========================================================

    print("\n\nFetching real schemes from India.gov.in...")

    india = IndiaGovConnector()

    try:

        results = india.search(
            query="farmer"
        )

        print(
            "Raw India.gov records:",
            len(results)
        )

        if results:

            print("\nNORMALIZED INDIA.GOV RECORD")

            normalized = normalizer.normalize(
                results[0]
            )

            print_scheme(normalized)

    except Exception as error:

        print(
            "India.gov error:",
            error
        )

    print("\n" + "=" * 70)
    print("NORMALIZER TEST COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()