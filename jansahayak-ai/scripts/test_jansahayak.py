from app.services.jansahayak import JanSahayak


def main():

    assistant = JanSahayak()

    profile = {
        "age": 21,
        "state": "Punjab",
        "occupation": "farmer",
        "income": 250000
    }

    query = (
        "I am a farmer from Punjab "
        "looking for government financial assistance"
    )

    results = assistant.find_schemes(
        query=query,
        profile=profile,
        top_k=5
    )

    print("=" * 70)
    print("JANSAHAYAK AI")
    print("=" * 70)

    print("\nUser:")
    print(query)

    for i, result in enumerate(
        results,
        start=1
    ):

        scheme = result["scheme"]
        eligibility = result["eligibility"]

        print("\n" + "-" * 70)

        print(
            f"{i}. {scheme['name']}"
        )

        print(
            "Category:",
            scheme.get("category")
        )

        print(
            "Description:",
            scheme.get("description")
        )

        print(
            "Source:",
            scheme.get("official_source")
        )

        if eligibility:

            print(
                "Eligibility:",
                eligibility["status"]
            )

            for reason in eligibility["reasons"]:

                print(
                    " ✓",
                    reason
                )

            for warning in eligibility["warnings"]:

                print(
                    " !",
                    warning
                )


if __name__ == "__main__":
    main()