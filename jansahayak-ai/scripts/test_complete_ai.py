from app.services.jansahayak import JanSahayak


def main():

    print("=" * 80)
    print("JANSAHAYAK AI - COMPLETE PIPELINE TEST")
    print("=" * 80)

    assistant = JanSahayak()

    # --------------------------------------------------
    # USER PROFILE
    # --------------------------------------------------

    profile = {
        "age": 21,
        "state": "Punjab",
        "occupation": "farmer",
        "income": 250000
    }

    # --------------------------------------------------
    # USER QUERY
    # --------------------------------------------------

    query = (
        "I am a farmer from Punjab "
        "looking for government financial assistance"
    )

    print("\nUSER PROFILE")
    print("-" * 80)

    for key, value in profile.items():
        print(f"{key}: {value}")

    print("\nUSER QUERY")
    print("-" * 80)
    print(query)

    # --------------------------------------------------
    # AI SEARCH
    # --------------------------------------------------

    print("\nSearching government schemes...")

    results = assistant.find_schemes(
        query=query,
        profile=profile,
        top_k=5
    )

    # --------------------------------------------------
    # RESULTS
    # --------------------------------------------------

    print("\n" + "=" * 80)
    print("AI RECOMMENDATIONS")
    print("=" * 80)

    if not results:

        print("\nNo relevant schemes found.")
        return

    for i, result in enumerate(
        results,
        start=1
    ):

        scheme = result["scheme"]

        eligibility = result["eligibility"]

        score = result["score"]

        explanation = result["explanation"]

        print("\n" + "-" * 80)

        print(
            f"{i}. {scheme.get('name')}"
        )

        print(
            f"Final Recommendation Score: "
            f"{score}"
        )

        print(
            f"Semantic Retrieval Score: "
            f"{round(scheme.get('retrieval_score', 0), 4)}"
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
            f"Ministry: "
            f"{scheme.get('nodal_ministry')}"
        )

        print(
            f"Level: "
            f"{scheme.get('level')}"
        )

        print(
            f"Verification: "
            f"{scheme.get('verification_status')}"
        )

        print(
            f"Official Source: "
            f"{scheme.get('official_source')}"
        )

        # --------------------------------------------------
        # ELIGIBILITY
        # --------------------------------------------------

        if eligibility:

            print(
                "\nEligibility:"
            )

            print(
                f"Status: "
                f"{eligibility.get('status')}"
            )

            if eligibility.get("reasons"):

                print(
                    "Reasons:"
                )

                for reason in eligibility["reasons"]:

                    print(
                        f"  ✓ {reason}"
                    )

            if eligibility.get("warnings"):

                print(
                    "Warnings:"
                )

                for warning in eligibility["warnings"]:

                    print(
                        f"  ! {warning}"
                    )

        # --------------------------------------------------
        # AI EXPLANATION
        # --------------------------------------------------

        print(
            "\nAI Explanation:"
        )

        print(
            explanation
        )

    print("\n" + "=" * 80)
    print("PIPELINE TEST COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    main()