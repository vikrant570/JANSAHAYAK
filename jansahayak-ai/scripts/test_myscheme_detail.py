import json

from app.services.detail_extractor import SchemeDetailExtractor


def main():

    print("=" * 70)
    print("JANSAHAYAK - MYSCHEME DETAIL TEST")
    print("=" * 70)

    with open(
        "data/schemes.json",
        "r",
        encoding="utf-8"
    ) as file:

        schemes = json.load(file)

    scheme = next(
        (
            x for x in schemes
            if x.get("source_name") == "myScheme"
        ),
        None
    )

    if not scheme:

        print("\nNo MyScheme record found.")

        return

    print("\nSCHEME")
    print("-" * 70)
    print("Name:", scheme.get("name"))
    print("Source:", scheme.get("source_name"))
    print("URL:", scheme.get("official_source"))

    extractor = SchemeDetailExtractor()

    result = extractor.extract(
        scheme
    )

    print("\nSTATUS")
    print("-" * 70)
    print("HTTP:", result.get("http_status"))
    print("Status:", result.get("status"))
    print("Final URL:", result.get("final_url"))
    print("Verified:", result.get("verified"))

    print("\nDOCUMENT INFORMATION")
    print("-" * 70)

    if result.get("document_text"):

        print(
            result["document_text"][:3000]
        )

    else:

        print(
            "No verified document section found."
        )

    print("\nELIGIBILITY")
    print("-" * 70)

    if result.get("eligibility_text"):

        print(
            result["eligibility_text"][:1000]
        )

    else:

        print(
            "No eligibility section found."
        )

    print("\nBENEFITS")
    print("-" * 70)

    if result.get("benefits_text"):

        print(
            result["benefits_text"][:1000]
        )

    else:

        print(
            "No benefits section found."
        )

    print("\nAPPLICATION")
    print("-" * 70)

    if result.get("application_text"):

        print(
            result["application_text"][:1000]
        )

    else:

        print(
            "No application section found."
        )

    print("\n" + "=" * 70)
    print("TEST COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()