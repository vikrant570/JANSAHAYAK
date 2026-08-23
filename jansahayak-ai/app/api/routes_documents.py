import os
import uuid

from fastapi import (
    APIRouter,
    File,
    HTTPException,
    UploadFile
)

from app.config import get_settings

from app.services.document_service import (
    validate_extension,
    extract_document_text,
    classify_document
)


router = APIRouter(
    prefix="/api/v1",
    tags=["Documents"]
)


@router.post(
    "/documents/analyze"
)
async def analyze_document(
    file: UploadFile = File(...)
):

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="Filename is required."
        )

    try:

        extension = validate_extension(
            file.filename
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    settings = get_settings()

    max_size = (
        settings.max_file_size_mb
        * 1024
        * 1024
    )

    content = await file.read()

    if len(content) > max_size:

        raise HTTPException(
            status_code=413,
            detail=(
                f"File exceeds the "
                f"{settings.max_file_size_mb}MB limit."
            )
        )

    file_id = str(
        uuid.uuid4()
    )

    upload_dir = "uploads"

    os.makedirs(
        upload_dir,
        exist_ok=True
    )

    file_path = os.path.join(
        upload_dir,
        f"{file_id}{extension}"
    )

    try:

        with open(
            file_path,
            "wb"
        ) as output_file:

            output_file.write(content)

        extracted_text = (
            extract_document_text(
                file_path,
                extension
            )
        )

        if not extracted_text:

            return {
                "document_type": "unknown",
                "summary": (
                    "No readable text could be "
                    "extracted from the document."
                ),
                "simple_explanation": (
                    "The document could not be "
                    "read automatically. "
                    "Please upload a clearer file."
                ),
                "important_dates": [],
                "required_actions": [],
                "warnings": [
                    "OCR or document extraction "
                    "did not produce readable text."
                ],
                "needs_verification": True
            }

        document_type = classify_document(
            extracted_text
        )

        return {
            "document_type": document_type,

            "summary": (
                "The document was successfully "
                "processed."
            ),

            "simple_explanation": (
                "The uploaded document appears "
                f"to be a {document_type.replace('_', ' ')}."
            ),

            "detailed_explanation": (
                "The text was extracted successfully. "
                "Further AI analysis can identify "
                "important dates, actions and warnings."
            ),

            "important_dates": [],

            "required_actions": [],

            "warnings": [
                "AI extraction may contain errors.",
                "Verify important dates and instructions "
                "against the original document."
            ],

            "extracted_text": extracted_text[:10000],

            "needs_verification": True
        }

    except Exception:

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to process the document."
            )
        )

    finally:

        try:

            if os.path.exists(
                file_path
            ):
                os.remove(file_path)

        except OSError:

            pass