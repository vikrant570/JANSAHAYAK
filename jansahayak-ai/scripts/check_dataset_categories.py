import json
from pathlib import Path


DATA_FILE = Path("data/schemes.json")


CATEGORY_KEYWORDS = {

    "Agriculture": [
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
    ],

    "Education": [
        "student",
        "students",
        "education",
        "scholarship",
        "college",
        "school",
        "university",
        "matric",
        "fellowship",
    ],

    "Business": [
        "business",
        "entrepreneur",
        "entrepreneurship",
        "startup",
        "enterprise",
        "msme",
        "vendor",
        "self employment",
    ],

    "Women": [
        "women",
        "woman",
        "female",
        "girl",
        "mahila",
        "widow",
    ],

    "Employment": [
        "employment",
        "unemployed",
        "job",
        "skill",
        "training",
    ],

    "Health": [
        "health",
        "medical",
        "hospital",
        "treatment",
        "healthcare",
    ],

    "Insurance": [
        "insurance",
        "bima",
        "accident",
        "cover",
    ],

    "Housing": [
        "housing",
        "house",
        "home",
        "awas",
        "shelter",
    ],

    "Pension": [
        "pension",
        "senior citizen",
        "old age",
        "retirement",
    ],

    "Disability": [
        "disability",
        "disabled",
        "divyang",
    ],
}


with open(
    DATA_FILE,
    "r",
    encoding="utf-8"
) as file:

    schemes = json.load(file)


print("\n========================================")
print("JANSAHAYAK DATASET CATEGORY CHECK")
print("========================================")

print(f"\nTotal schemes: {len(schemes)}")


for category, keywords in CATEGORY_KEYWORDS.items():

    matches = []

    for scheme in schemes:

        if not isinstance(scheme, dict):
            continue

        text = " ".join(
            str(scheme.get(field, ""))
            for field in [
                "name",
                "description",
                "category",
                "categories",
                "benefits",
                "eligibility",
                "target_users",
                "target_group",
                "tags",
            ]
        ).lower()

        if any(
            keyword in text
            for keyword in keywords
        ):

            matches.append(
                scheme.get(
                    "name",
                    "Unnamed Scheme"
                )
            )

    print(
        f"{category:<15}: {len(matches)}"
    )


print("\n========================================")