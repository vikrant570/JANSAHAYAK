from app.services.scheme_search import SchemeSearchService
from app.services.scheme_filter import SchemeFilter


def main():

    print("=" * 70)
    print("JANSAHAYAK - STATE FILTER TEST")
    print("=" * 70)

    search = SchemeSearchService()
    filtering = SchemeFilter()

    schemes = search.search(
        "farmer",
        page_size=10
    )

    print(
        f"\nTotal schemes returned: "
        f"{len(schemes)}"
    )

    punjab_schemes = filtering.filter_by_state(
        schemes,
        "Punjab"
    )

    print(
        f"Punjab-compatible schemes: "
        f"{len(punjab_schemes)}"
    )

    for i, scheme in enumerate(
        punjab_schemes,
        start=1
    ):

        print(
            f"\n{i}. {scheme['name']}"
        )

        print(
            f"State: {scheme['states']}"
        )

        print(
            f"Source: "
            f"{scheme['official_source']}"
        )


if __name__ == "__main__":
    main()