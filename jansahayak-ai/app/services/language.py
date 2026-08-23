from langdetect import detect, LangDetectException


SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "pa": "Punjabi"
}


def detect_language(
    text: str
) -> str:

    # Devanagari
    if any(
        "\u0900" <= char <= "\u097F"
        for char in text
    ):
        return "hi"

    # Gurmukhi
    if any(
        "\u0A00" <= char <= "\u0A7F"
        for char in text
    ):
        return "pa"

    try:

        language = detect(text)

        if language in SUPPORTED_LANGUAGES:
            return language

    except LangDetectException:
        pass

    return "en"


def validate_language(
    language: str
) -> str:

    language = language.lower().strip()

    if language not in SUPPORTED_LANGUAGES:

        raise ValueError(
            "Supported languages are English, Hindi and Punjabi."
        )

    return language