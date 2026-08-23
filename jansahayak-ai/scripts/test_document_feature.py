import json

from app.services.document_checklist import (
    DocumentChecklist
)


def main():

    print("=" * 70)
    print("JANSAHAYAK - DOCUMENT FEATURE")
    print("=" * 70)

    with open(
        "data/schemes.json",
        "r",
        encoding="utf-8"
    ) as file:

        schemes = json.load(file)

    print(
        "\nTotal schemes:",
        len(schemes)
    )

    if not schemes:

        print(
            "No schemes found."
        )

        return

    checklist = (
        DocumentChecklist()
    )

    # =========================================================
    # TEST EACH SCHEME
    # =========================================================

    for index, scheme in enumerate(
        schemes,
        start=1
    ):

        print("\n" + "-" * 70)

        print(
            f"{index}.",
            scheme.get("name")
        )

        print(
            "Source:",
            scheme.get(
                "source_name"
            )
        )

        print(
            "Documents verified:",
            scheme.get(
                "documents_verified",
                False
            )
        )

        result = checklist.generate(
            scheme=scheme,
            user_documents=[]
        )

        print(
            "Status:",
            result.get("status")
        )

        documents = result.get(
            "required_documents",
            []
        )

        if documents:

            print("\nRequired documents:")

            for document in documents:

                print(
                    "  -",
                    document
                )

        else:

            print(
                "\n",
                result.get(
                    "message"
                ),
                sep=""
            )

        print(
            "\nOfficial source:",
            result.get(
                "official_source"
            )
        )

    print("\n" + "=" * 70)
    print("DOCUMENT FEATURE TEST COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()