from app.services.jansahayak import JanSahayak


def main():

    print("=" * 70)
    print("JANSAHAYAK - COMPLETE AI + DOCUMENT TEST")
    print("=" * 70)

    # =========================================================
    # USER QUERY
    # =========================================================

    query = (
        "I am a farmer from Punjab looking for "
        "government financial assistance"
    )

    # =========================================================
    # USER PROFILE
    # =========================================================

    profile = {

        "age": 21,

        "state": "Punjab",

        "occupation": "farmer",

        "income": 250000,

        # User can tell JanSahayak which documents
        # they already have.
        "documents": [
            "Aadhaar Card",
            "Bank Passbook"
        ]
    }

    print("\nQUERY")
    print("-" * 70)

    print(query)

    print("\nPROFILE")
    print("-" * 70)

    for key, value in profile.items():

        print(
            f"{key}: {value}"
        )

    # =========================================================
    # JANSAHAYAK
    # =========================================================

    assistant = JanSahayak()

    results = assistant.find_schemes(
        query=query,
        profile=profile,
        top_k=5
    )

    print("\n")
    print("=" * 70)
    print("RECOMMENDATIONS")
    print("=" * 70)

    if not results:

        print(
            "\nNo recommendations found."
        )

        return

    # =========================================================
    # PRINT RESULTS
    # =========================================================

    for index, result in enumerate(
        results,
        start=1
    ):

        print("\n")
        print("=" * 70)

        print(
            f"RECOMMENDATION {index}"
        )

        print("=" * 70)

        scheme = result.get(
            "scheme",
            {}
        )

        eligibility = result.get(
            "eligibility",
            {}
        )

        documents = result.get(
            "documents",
            {}
        )

        score = result.get(
            "score",
            0
        )

        explanation = result.get(
            "explanation",
            ""
        )

        # -----------------------------------------------------
        # BASIC SCHEME
        # -----------------------------------------------------

        print(
            "\nScheme:",
            scheme.get(
                "name"
            )
        )

        print(
            "Score:",
            round(
                score,
                4
            )
        )

        print(
            "Category:",
            scheme.get(
                "category"
            )
        )

        print(
            "States:",
            scheme.get(
                "states"
            )
        )

        print(
            "Level:",
            scheme.get(
                "level"
            )
        )

        print(
            "Ministry:",
            scheme.get(
                "nodal_ministry"
            )
        )

        print(
            "Source:",
            scheme.get(
                "source_name"
            )
        )

        print(
            "Official URL:",
            scheme.get(
                "official_source"
            )
        )

        # -----------------------------------------------------
        # ELIGIBILITY
        # -----------------------------------------------------

        print("\nELIGIBILITY")
        print("-" * 70)

        if eligibility:

            for key, value in (
                eligibility.items()
            ):

                print(
                    f"{key}: {value}"
                )

        else:

            print(
                "Eligibility information "
                "not available."
            )

        # -----------------------------------------------------
        # DOCUMENTS
        # -----------------------------------------------------

        print("\nDOCUMENTS")
        print("-" * 70)

        print(
            "Status:",
            documents.get(
                "status"
            )
        )

        print(
            "Verified:",
            documents.get(
                "documents_verified",
                False
            )
        )

        required = documents.get(
            "required_documents",
            []
        )

        available = documents.get(
            "available_documents",
            []
        )

        missing = documents.get(
            "missing_documents",
            []
        )

        # Required
        if required:

            print(
                "\nRequired documents:"
            )

            for document in required:

                print(
                    "  -",
                    document
                )

        # Available
        if available:

            print(
                "\nAlready available:"
            )

            for document in available:

                print(
                    "  ✓",
                    document
                )

        # Missing
        if missing:

            print(
                "\nMissing documents:"
            )

            for document in missing:

                print(
                    "  ✗",
                    document
                )

        # Verification message
        message = documents.get(
            "message"
        )

        if message:

            print(
                "\nMessage:"
            )

            print(
                message
            )

        # Official source
        document_source = (
            documents.get(
                "official_source"
            )
        )

        if document_source:

            print(
                "\nDocument source:"
            )

            print(
                document_source
            )

        # -----------------------------------------------------
        # EXPLANATION
        # -----------------------------------------------------

        print("\nAI EXPLANATION")
        print("-" * 70)

        print(
            explanation
            or
            "No explanation available."
        )

    print("\n")
    print("=" * 70)
    print("COMPLETE AI + DOCUMENT TEST FINISHED")
    print("=" * 70)


if __name__ == "__main__":
    main()