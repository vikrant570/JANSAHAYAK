from app.services.scheme_section_extractor import (
    SchemeSectionExtractor
)


def main():

    extractor = SchemeSectionExtractor()

    sample = """
    Tripura Government Scheme

    Eligibility

    Applicant should be a resident of the state.
    Annual income should be below the prescribed limit.

    Benefits

    Financial assistance is provided to eligible beneficiaries.

    Documents Required

    1. Aadhaar Card
    2. Income Certificate
    3. Bank Passbook

    How to Apply

    Visit the official portal.
    Submit the application form.
    Upload the required documents.

    Contact

    Contact the concerned department.
    """

    result = extractor.extract(
        sample
    )

    print("=" * 70)
    print("SECTION EXTRACTION TEST")
    print("=" * 70)

    print("\nELIGIBILITY")
    print("-" * 70)
    print(
        result["eligibility_text"]
    )

    print("\nBENEFITS")
    print("-" * 70)
    print(
        result["benefits_text"]
    )

    print("\nDOCUMENTS")
    print("-" * 70)
    print(
        result["documents_text"]
    )

    print("\nAPPLICATION")
    print("-" * 70)
    print(
        result["application_steps_text"]
    )


if __name__ == "__main__":
    main()