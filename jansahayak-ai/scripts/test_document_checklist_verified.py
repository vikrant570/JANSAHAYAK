from app.services.document_checklist import (
    DocumentChecklist
)


def main():

    print("=" * 70)
    print("VERIFIED DOCUMENT CHECKLIST TEST")
    print("=" * 70)

    # TEST DATA ONLY
    # This does NOT get saved into schemes.json.

    scheme = {

        "name":
            "Document Test Scheme",

        "documents": [
            "Aadhaar Card",
            "Income Certificate",
            "Bank Passbook"
        ],

        "documents_verified":
            True,

        "official_source":
            "https://example.gov.in/test"
    }

    user_documents = [
        "Aadhaar Card",
        "Bank Passbook"
    ]

    checklist = DocumentChecklist()

    result = checklist.generate(
        scheme=scheme,
        user_documents=user_documents
    )

    print(
        "\nRequired:"
    )

    for item in result[
        "required_documents"
    ]:

        print(
            "-",
            item
        )

    print(
        "\nAvailable:"
    )

    for item in result[
        "available_documents"
    ]:

        print(
            "✓",
            item
        )

    print(
        "\nMissing:"
    )

    for item in result[
        "missing_documents"
    ]:

        print(
            "✗",
            item
        )

    print(
        "\nVerified:",
        result[
            "documents_verified"
        ]
    )

    print(
        "Status:",
        result["status"]
    )


if __name__ == "__main__":
    main()