from app.services.recommender import (
    SchemeRecommender
)


def main():

    print("=" * 70)
    print("JANSAHAYAK AI - RECOMMENDATION ENGINE")
    print("=" * 70)

    profile = {

        "age": 21,

        "state": "Punjab",

        "gender": "female",

        "occupation": "student",

        "education": "B.Tech",

        "annual_income": 300000,

        "category": "General"
    }

    query = "student scholarship"

    recommender = SchemeRecommender()

    results = recommender.recommend(
        query=query,
        profile=profile,
        limit=5
    )

    print(
        f"\nUser query: {query}"
    )

    print(
        f"User state: {profile['state']}"
    )

    print(
        f"\nRecommendations: "
        f"{len(results)}"
    )

    for i, scheme in enumerate(
        results,
        start=1
    ):

        print("\n" + "-" * 60)

        print(
            f"{i}. {scheme['name']}"
        )

        print(
            f"Category: "
            f"{scheme['category']}"
        )

        print(
            f"State: "
            f"{scheme['states']}"
        )

        print(
            f"Source: "
            f"{scheme['official_source']}"
        )

        print(
            f"Eligibility: "
            f"{scheme['eligibility_result']}"
        )


if __name__ == "__main__":
    main()