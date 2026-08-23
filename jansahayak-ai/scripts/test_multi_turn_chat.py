from app.services.jansahayak import JanSahayak


def main():

    print("=" * 80)
    print("JANSAHAYAK AI - MULTI TURN CONVERSATION TEST")
    print("=" * 80)

    assistant = JanSahayak()

    profile = {}

    messages = [

        "I am a 21 year old farmer from Punjab.",

        "My annual income is 250000 rupees.",

        "I need financial assistance for agriculture.",

    ]

    for index, message in enumerate(
        messages,
        start=1
    ):

        print("\n")
        print("-" * 80)

        print(
            f"USER MESSAGE {index}"
        )

        print("-" * 80)

        print(message)

        result = assistant.chat(
            message=message,
            profile=profile
        )

        profile = result["profile"]

        print("\nJANSAHAYAK:")

        print(
            result["message"]
        )

        print("\nCURRENT PROFILE:")

        for key, value in profile.items():

            print(
                f"{key}: {value}"
            )

    print("\n")
    print("=" * 80)
    print("MULTI TURN TEST COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    main()