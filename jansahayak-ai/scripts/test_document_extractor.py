from app.services.document_extractor import DocumentExtractor


def main():

    print("=" * 70)
    print("JANSAHAYAK - DOCUMENT EXTRACTOR TEST")
    print("=" * 70)

    extractor = DocumentExtractor()

    sample_text = """
    Documents Required

    1. Aadhaar Card
    2. Income Certificate
    3. Bank Passbook
    4. Passport Size Photograph

    Eligibility

    Applicant must be a resident of the state.

    Benefits

    Financial assistance will be provided to eligible beneficiaries.

    How to Apply

    Submit the application through the official portal.
    """

    documents = extractor.extract(
        sample_text
    )

    print("\nExtracted documents:")
    print("-" * 70)

    for index, document in enumerate(
        documents,
        start=1
    ):

        print(
            f"{index}. {document}"
        )

    print("\nTotal documents:", len(documents))

    print("\n" + "=" * 70)
    print("DOCUMENT EXTRACTOR TEST COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()