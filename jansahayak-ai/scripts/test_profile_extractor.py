from app.services.profile_extractor import ProfileExtractor


def main():

    extractor = ProfileExtractor()

    queries = [

        "I am a 21 year old farmer from Punjab "
        "with an annual income of 2.5 lakh",

        "I am a student from Punjab looking "
        "for scholarship assistance",

        "I am a 35 year old woman entrepreneur "
        "from Haryana with an income of 3 lakh",

        "I am a farmer from Rajasthan looking "
        "for agricultural equipment assistance"
    ]

    for query in queries:

        print("=" * 70)

        print("USER QUERY:")
        print(query)

        print("\nEXTRACTED PROFILE:")

        profile = extractor.extract(
            query
        )

        for key, value in profile.items():

            print(
                f"{key}: {value}"
            )

        print()


if __name__ == "__main__":
    main()