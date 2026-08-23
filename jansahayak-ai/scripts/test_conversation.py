from app.services.jansahayak import JanSahayak


def main():

    print("=" * 80)
    print("JANSAHAYAK AI - CONVERSATIONAL TEST")
    print("=" * 80)

    assistant = JanSahayak()

    message = (
        "I am a 21 year old farmer from Punjab. "
        "My annual income is 250000 rupees. "
        "I need government financial assistance "
        "for agriculture."
    )

    print("\nUSER")
    print("-" * 80)
    print(message)

    print("\nJANSAHAYAK")
    print("-" * 80)

    result = assistant.chat(
        message
    )

    print(
        result["message"]
    )

    print("\n")
    print("=" * 80)

    print("EXTRACTED USER PROFILE")
    print("=" * 80)

    for key, value in result["profile"].items():

        print(
            f"{key}: {value}"
        )

    print("\n")
    print("=" * 80)
    print("CONVERSATION TEST COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    main()