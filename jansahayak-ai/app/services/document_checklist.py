class DocumentChecklist:

    def generate(
        self,
        scheme: dict,
        user_documents: list[str] | None = None
    ) -> dict:

        user_documents = (
            user_documents
            or []
        )

        required = scheme.get(
            "documents",
            []
        ) or []

        verified = bool(
            scheme.get(
                "documents_verified",
                False
            )
        )

        official_source = (
            scheme.get(
                "official_source",
                ""
            )
            or ""
        )

        # =====================================================
        # DOCUMENT INFORMATION NOT VERIFIED
        # =====================================================

        if (
            not verified
            or
            not required
        ):

            return {
                "required_documents": [],
                "optional_documents": [],
                "missing_documents": [],

                "documents_verified": False,

                "status":
                    "verification_required",

                "message": (
                    "The required document list "
                    "could not be verified from "
                    "the available official scheme "
                    "data. Please confirm the "
                    "documents on the official "
                    "scheme page before applying."
                ),

                "official_source":
                    official_source,

                "preparation_instructions":
                    []
            }

        # =====================================================
        # NORMALIZE USER DOCUMENTS
        # =====================================================

        user_normalized = {
            self._normalize(document)
            for document
            in user_documents
        }

        missing = []

        available = []

        for document in required:

            normalized = self._normalize(
                document
            )

            if normalized in user_normalized:

                available.append(
                    document
                )

            else:

                missing.append(
                    document
                )

        return {
            "required_documents":
                required,

            "available_documents":
                available,

            "optional_documents":
                [],

            "missing_documents":
                missing,

            "documents_verified":
                True,

            "status":
                "verified",

            "message": (
                "Document requirements are "
                "based on verified scheme-detail "
                "data."
            ),

            "official_source":
                official_source,

            "preparation_instructions": [
                (
                    f"Keep a valid and readable "
                    f"copy of {document}."
                )
                for document
                in required
            ]
        }

    # =========================================================

    @staticmethod
    def _normalize(
        value: str
    ) -> str:

        return (
            str(value)
            .strip()
            .lower()
            .replace("-", " ")
            .replace("_", " ")
        )