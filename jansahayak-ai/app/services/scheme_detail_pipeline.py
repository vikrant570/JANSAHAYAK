from app.services.scheme_detail_enricher import (
    SchemeDetailEnricher
)

from app.services.scheme_section_extractor import (
    SchemeSectionExtractor
)

from app.services.document_extractor import (
    DocumentExtractor
)


class SchemeDetailPipeline:

    def __init__(self):

        self.enricher = (
            SchemeDetailEnricher()
        )

        self.section_extractor = (
            SchemeSectionExtractor()
        )

        self.document_extractor = (
            DocumentExtractor()
        )

    def enrich(
        self,
        scheme: dict
    ) -> dict:

        result = self.enricher.enrich(
            scheme
        )

        text = result.get(
            "detail_text",
            ""
        )

        if not text:

            return result

        sections = (
            self.section_extractor.extract(
                text
            )
        )

        result[
            "eligibility_text"
        ] = sections[
            "eligibility_text"
        ]

        result[
            "benefits_text"
        ] = sections[
            "benefits_text"
        ]

        result[
            "documents_text"
        ] = sections[
            "documents_text"
        ]

        result[
            "application_steps_text"
        ] = sections[
            "application_steps_text"
        ]

        # -----------------------------------------------------
        # DOCUMENTS
        # -----------------------------------------------------

        documents = (
            self.document_extractor.extract(
                sections[
                    "documents_text"
                ]
            )
        )

        result["documents"] = documents

        return result