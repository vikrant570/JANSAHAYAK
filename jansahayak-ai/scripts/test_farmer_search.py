from dotenv import load_dotenv

load_dotenv()

from app.connectors.myscheme import MySchemeConnector
from app.services.scheme_normalizer import SchemeNormalizer


print("=" * 70)
print("JANSAHAYAK - PUNJAB FARMER SCHEME SEARCH")
print("=" * 70)

connector = MySchemeConnector()
normalizer = SchemeNormalizer()

print("\nSearching MyScheme...\n")

results = connector.search(
    query="farmer",
    page_size=10
)

print(
    "Raw schemes received:",
    len(results)
)

print("\n" + "=" * 70)

for index, raw in enumerate(results, start=1):

    scheme = normalizer.normalize(raw)

    print(f"\n{index}. {scheme['name']}")

    print(
        "Category:",
        scheme["category"]
    )

    print(
        "States:",
        ", ".join(scheme["states"])
    )

    print(
        "Ministry:",
        scheme["authority"]
    )

    print(
        "Description:",
        scheme["description"]
    )

    print(
        "Source:",
        scheme["official_source"]
    )

    print(
        "Confidence:",
        scheme["confidence"]
    )