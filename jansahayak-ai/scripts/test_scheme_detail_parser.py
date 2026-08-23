from app.services.scheme_detail_parser import (
    SchemeDetailParser
)


def main():

    # This is STRUCTURE TEST DATA,
    # not a real scheme record.

    sample = {

        "details": {

            "basicDetails": {
                "schemeName":
                    "Parser Test Scheme"
            },

            "schemeContent": {

                "benefits": [
                    {
                        "type": "ul_list",
                        "children": [
                            {
                                "type": "list_item",
                                "children": [
                                    {
                                        "text":
                                            "Financial assistance"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },

            "eligibilityCriteria": {

                "eligibilityDescription": [
                    {
                        "type": "paragraph",
                        "children": [
                            {
                                "text":
                                    "Applicant must satisfy "
                                    "the eligibility criteria."
                            }
                        ]
                    }
                ]
            },

            "documents": {

                "documents": [
                    {
                        "type": "ul_list",
                        "children": [
                            {
                                "type": "list_item",
                                "children": [
                                    {
                                        "text":
                                            "Identity Proof"
                                    }
                                ]
                            },
                            {
                                "type": "list_item",
                                "children": [
                                    {
                                        "text":
                                            "Income Certificate"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },

            "applicationProcess": [

                {
                    "mode":
                        "Online",

                    "url":
                        "https://example.gov.in/apply",

                    "process": [
                        {
                            "type":
                                "paragraph",

                            "children": [
                                {
                                    "text":
                                        "Open the official "
                                        "application portal."
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    }

    parser = (
        SchemeDetailParser()
    )

    result = parser.parse(
        sample
    )

    print("=" * 70)
    print("JANSAHAYAK DETAIL PARSER TEST")
    print("=" * 70)

    print(
        "\nName:",
        result["name"]
    )

    print(
        "\nDocuments:"
    )

    for item in result[
        "documents"
    ]:
        print("-", item)

    print(
        "\nDocuments verified:",
        result[
            "documents_verified"
        ]
    )

    print(
        "\nBenefits:",
        result["benefits"]
    )

    print(
        "\nEligibility:"
    )

    print(
        result[
            "eligibility_text"
        ]
    )

    print(
        "\nApplication:"
    )

    for step in result[
        "application_steps"
    ]:
        print("-", step)

    print(
        "\nDetail verified:",
        result[
            "detail_verified"
        ]
    )


if __name__ == "__main__":
    main()