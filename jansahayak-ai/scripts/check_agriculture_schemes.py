import json
from pathlib import Path


DATA_FILE = Path("data/schemes.json")

AGRICULTURE_KEYWORDS = [
    "farmer",
    "farmers",
    "farming",
    "agriculture",
    "agricultural",
    "kisan",
    "crop",
    "irrigation",
    "horticulture",
    "livestock",
    "dairy",
    "fisheries",
    "animal husbandry",
]


with open(
    DATA_FILE,
    "r",
    encoding="utf-8"
) as file:

    data = json.load(file)


# Support either:
# [scheme, scheme, ...]
#
# or:
# {"schemes": [...]}

if isinstance(data, dict):

    schemes = (
        data.get("schemes")
        or data.get("results")
        or data.get("data")
        or []
    )

elif isinstance(data, list):

    schemes = data

else:

    schemes = []


matches = []


for scheme in schemes:

    if not isinstance(
        scheme,
        dict
    ):
        continue

    searchable_text = " ".join(
        str(
            scheme.get(field, "")
        )
        for field in [
            "name",
            "description",
            "category",
            "categories",
            "benefits",
            "eligibility",
            "target_group",
            "tags",
        ]
    ).lower()

    found_keywords = [
        keyword
        for keyword in AGRICULTURE_KEYWORDS
        if keyword in searchable_text
    ]

    if found_keywords:

        matches.append(
            (
                scheme.get(
                    "name",
                    "Unnamed Scheme"
                ),
                found_keywords
            )
        )


print("\n============================================")
print("AGRICULTURE DATASET CHECK")
print("============================================")

print(
    f"\nTotal schemes in dataset: {len(schemes)}"
)

print(
    f"Agriculture-related schemes found: {len(matches)}"
)

print("\nMatching schemes:\n")


for index, (
    name,
    keywords
) in enumerate(
    matches,
    start=1
):

    print(
        f"{index}. {name}"
    )

    print(
        "   Keywords:",
        ", ".join(keywords)
    )

    print()


print("============================================")