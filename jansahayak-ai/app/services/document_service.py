from pathlib import Path
import os

import fitz
from PIL import Image
import pytesseract


ALLOWED_EXTENSIONS = {
    ".pdf",
    ".jpg",
    ".jpeg",
    ".png"
}


def validate_extension(
    filename: str
) -> str:

    extension = Path(
        filename
    ).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:

        raise ValueError(
            "Unsupported file type. "
            "Only PDF, JPG, JPEG and PNG are allowed."
        )

    return extension


def configure_tesseract():

    command = os.getenv(
        "TESSERACT_CMD",
        ""
    ).strip()

    if command:
        pytesseract.pytesseract.tesseract_cmd = command


def extract_pdf_text(
    file_path: str
) -> str:

    document = fitz.open(file_path)

    pages = []

    try:

        for page in document:

            text = page.get_text()

            if text:
                pages.append(text)

    finally:

        document.close()

    return "\n".join(pages).strip()


def ocr_image(
    file_path: str
) -> str:

    configure_tesseract()

    image = Image.open(file_path)

    text = pytesseract.image_to_string(
        image
    )

    return text.strip()


def extract_document_text(
    file_path: str,
    extension: str
) -> str:

    if extension == ".pdf":

        text = extract_pdf_text(
            file_path
        )

        return text

    if extension in {
        ".jpg",
        ".jpeg",
        ".png"
    }:

        return ocr_image(
            file_path
        )

    raise ValueError(
        "Unsupported document format."
    )


def classify_document(
    text: str
) -> str:

    lower_text = text.lower()

    if (
        "notice" in lower_text
        or "show cause" in lower_text
    ):
        return "government_notice"

    if (
        "scholarship" in lower_text
        or "student" in lower_text
    ):
        return "education_document"

    if (
        "farmer" in lower_text
        or "agriculture" in lower_text
        or "crop" in lower_text
    ):
        return "agriculture_document"

    if (
        "complaint" in lower_text
        or "grievance" in lower_text
    ):
        return "complaint_document"

    return "government_document"