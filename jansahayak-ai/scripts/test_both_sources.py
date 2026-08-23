from app.connectors.india_gov import IndiaGovConnector
from app.connectors.myscheme import MySchemeConnector


def print_scheme(
    scheme,
    number
):

    print(
        f"\n{number}. {scheme.get('name')}"
    )

    print(
        f"Category: {scheme.get('category')}"
    )

    print(
        f"State: {scheme.get('states')}"
    )

    print(
        f"Ministry: {scheme.get('nodal_ministry')}"
    )

    print(
        f"Level: {scheme.get('level')}"
    )

    print(
        f"Source: {scheme.get('official_source')}"
    )

    print(
        f"Authority: {scheme.get('authority')}"
    )

    print(
        f"Verification: "
        f"{scheme.get('verification_status')}"
    )


def main():

    print("=" * 70)
    print("JANSAHAYAK - MULTI-SOURCE TEST")
    print("=" * 70)

    # --------------------------------------------------
    # INDIA.GOV.IN
    # --------------------------------------------------

    india = IndiaGovConnector()

    india_schemes = india.search(
        "farmer"
    )

    print(
        "\n" + "=" * 70
    )
    print("INDIA.GOV.IN")
    print("=" * 70)

    print(
        f"Schemes received: "
        f"{len(india_schemes)}"
    )

    for i, scheme in enumerate(
        india_schemes[:5],
        start=1
    ):

        print_scheme(
            scheme,
            i
        )

    # --------------------------------------------------
    # MYSCHEME
    # --------------------------------------------------

    myscheme = MySchemeConnector()

    myscheme_schemes = myscheme.search(
        "farmer"
    )

    print(
        "\n" + "=" * 70
    )
    print("MYSCHEME.GOV.IN")
    print("=" * 70)

    print(
        f"Schemes received: "
        f"{len(myscheme_schemes)}"
    )

    for i, scheme in enumerate(
        myscheme_schemes[:5],
        start=1
    ):

        print_scheme(
            scheme,
            i
        )


if __name__ == "__main__":
    main()