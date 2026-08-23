from app.services.user_understanding import (
    UserUnderstanding
)


def main():

    ai = UserUnderstanding()

    user_input = (
        "I am a 21 year old farmer from Punjab "
        "with an annual income of 2.5 lakh. "
        "I need financial assistance to buy "
        "agricultural equipment."
    )

    print("=" * 80)
    print("JANSAHAYAK AI - USER UNDERSTANDING")
    print("=" * 80)

    print("\nUSER INPUT")
    print("-" * 80)
    print(user_input)

    result = ai.understand(
        user_input
    )

    print("\nPROFILE")
    print("-" * 80)

    for key, value in result[
        "profile"
    ].items():

        print(
            f"{key}: {value}"
        )

    print("\nUNDERSTOOD NEED")
    print("-" * 80)

    print(
        "Categories:",
        result["query"]["categories"]
    )


if __name__ == "__main__":
    main()