from app.services.scheme_rag import SchemeRAG
from app.services.eligibility import check_eligibility


def main():

    rag = SchemeRAG()

    profile = {
        "age": 21,
        "state": "Punjab",
        "occupation": "student",
        "income": 200000
    }

    query = (
        "student scholarship government scheme"
    )

    schemes = rag.search(
        query,
        top_k=5
    )

    for scheme in schemes:

        result = check_eligibility(
            scheme,
            profile
        )

        print("\n" + "=" * 60)

        print(
            "SCHEME:",
            scheme["name"]
        )

        print(
            "STATUS:",
            result["status"]
        )

        print(
            "REASONS:"
        )

        for reason in result["reasons"]:
            print(
                " ✓",
                reason
            )

        print(
            "WARNINGS:"
        )

        for warning in result["warnings"]:
            print(
                " !",
                warning
            )


if __name__ == "__main__":
    main()