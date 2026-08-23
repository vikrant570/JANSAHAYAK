from app.services.query_processor import QueryProcessor


def main():

    print("=" * 70)
    print("JANSAHAYAK - QUERY PROCESSOR TEST")
    print("=" * 70)

    processor = QueryProcessor()

    queries = [

        "I am a frammer from punjab looking for finacial help",

        "I am a studnt looking for scholrship",

        "I need goverment assistnce for my busines",

        "I am a farmer from Punjab looking for financial assistance",

    ]

    for query in queries:

        result = processor.process(
            query
        )

        print("\n" + "-" * 70)

        print(
            "Original:",
            result["original_query"]
        )

        print(
            "Corrected:",
            result["corrected_query"]
        )

        print(
            "Changed:",
            result["was_corrected"]
        )


if __name__ == "__main__":
    main()