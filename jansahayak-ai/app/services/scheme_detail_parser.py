import re
from typing import Any


class SchemeDetailParser:
    """
    Converts structured scheme-detail JSON into the
    common JanSahayak detail format.

    It never invents missing information.
    """

    # =========================================================
    # MAIN
    # =========================================================

    def parse(self, payload: dict) -> dict:

        if not isinstance(payload, dict):
            return self.empty_result()

        details = self._find_details_object(payload)

        if not details:
            details = payload

        basic = details.get("basicDetails", {})

        scheme_content = details.get(
            "schemeContent",
            {}
        )

        eligibility_data = details.get(
            "eligibilityCriteria",
            {}
        )

        documents_data = details.get(
            "documents",
            {}
        )

        application_data = details.get(
            "applicationProcess",
            []
        )

        # -----------------------------------------------------
        # DOCUMENTS
        # -----------------------------------------------------

        documents = self._extract_documents(
            documents_data
        )

        # -----------------------------------------------------
        # BENEFITS
        # -----------------------------------------------------

        benefits = self._extract_text_list(
            scheme_content.get("benefits", [])
        )

        # -----------------------------------------------------
        # ELIGIBILITY
        # -----------------------------------------------------

        eligibility_text = self._extract_eligibility(
            eligibility_data
        )

        # -----------------------------------------------------
        # APPLICATION
        # -----------------------------------------------------

        (
            application_steps,
            application_urls
        ) = self._extract_application(
            application_data
        )

        # -----------------------------------------------------
        # DESCRIPTION
        # -----------------------------------------------------

        description = (
            scheme_content.get(
                "briefDescription"
            )
            or
            details.get(
                "description"
            )
            or
            ""
        )

        name = self._label_value(
            basic.get(
                "schemeName"
            )
        )

        if not name:
            name = str(
                details.get(
                    "name",
                    ""
                )
            ).strip()

        return {
            "name": name,

            "description":
                self._clean(description),

            "documents":
                documents,

            "documents_verified":
                bool(documents),

            "benefits":
                benefits,

            "eligibility_text":
                eligibility_text,

            "application_steps":
                application_steps,

            "application_urls":
                application_urls,

            "detail_verified":
                any(
                    [
                        documents,
                        benefits,
                        eligibility_text,
                        application_steps,
                    ]
                )
        }

    # =========================================================
    # FIND DETAIL OBJECT
    # =========================================================

    def _find_details_object(
        self,
        payload: dict
    ) -> dict:

        # Direct structure
        if (
            "basicDetails" in payload
            or
            "schemeContent" in payload
            or
            "documents" in payload
            or
            "eligibilityCriteria" in payload
        ):
            return payload

        # Common wrappers
        for key in [
            "details",
            "data",
            "result",
            "scheme",
            "schemeDetails"
        ]:

            value = payload.get(key)

            if isinstance(value, dict):

                found = (
                    self._find_details_object(
                        value
                    )
                )

                if found:
                    return found

        # Recursive fallback
        for value in payload.values():

            if isinstance(value, dict):

                found = (
                    self._find_details_object(
                        value
                    )
                )

                if found:
                    return found

        return {}

    # =========================================================
    # DOCUMENTS
    # =========================================================

    def _extract_documents(
        self,
        data: Any
    ) -> list[str]:

        if not data:
            return []

        # Markdown version, when provided
        if isinstance(data, dict):

            markdown = data.get(
                "documents_md"
            )

            if markdown:

                return self._lines_to_items(
                    markdown
                )

            document_tree = data.get(
                "documents"
            )

            if document_tree:

                texts = self._extract_text_list(
                    document_tree
                )

                return self._deduplicate(
                    texts
                )

        texts = self._extract_text_list(
            data
        )

        return self._deduplicate(
            texts
        )

    # =========================================================
    # ELIGIBILITY
    # =========================================================

    def _extract_eligibility(
        self,
        data: Any
    ) -> str:

        if not data:
            return ""

        if isinstance(data, dict):

            markdown = data.get(
                "eligibilityDescription_md"
            )

            if markdown:

                return self._clean_markdown(
                    markdown
                )

            description = data.get(
                "eligibilityDescription"
            )

            if description:

                return "\n".join(
                    self._extract_text_list(
                        description
                    )
                )

        return "\n".join(
            self._extract_text_list(
                data
            )
        )

    # =========================================================
    # APPLICATION
    # =========================================================

    def _extract_application(
        self,
        data: Any
    ) -> tuple[list[str], list[str]]:

        steps = []
        urls = []

        if not isinstance(
            data,
            list
        ):
            return steps, urls

        for process in data:

            if not isinstance(
                process,
                dict
            ):
                continue

            mode = self._clean(
                process.get(
                    "mode"
                )
            )

            url = self._clean(
                process.get(
                    "url"
                )
            )

            if url:
                urls.append(url)

            process_steps = (
                self._extract_text_list(
                    process.get(
                        "process",
                        []
                    )
                )
            )

            for step in process_steps:

                if mode:

                    steps.append(
                        f"[{mode}] {step}"
                    )

                else:

                    steps.append(step)

        return (
            self._deduplicate(steps),
            self._deduplicate(urls)
        )

    # =========================================================
    # RECURSIVE TEXT EXTRACTOR
    # =========================================================

    def _extract_text_list(
        self,
        value: Any
    ) -> list[str]:

        result = []

        self._collect_text(
            value,
            result
        )

        cleaned = []

        for item in result:

            item = self._clean(item)

            if not item:
                continue

            # Ignore tiny formatting fragments
            if len(item) < 2:
                continue

            cleaned.append(item)

        return self._deduplicate(
            cleaned
        )

    def _collect_text(
        self,
        value: Any,
        output: list
    ):

        if value is None:
            return

        if isinstance(
            value,
            str
        ):

            text = value.strip()

            if text:
                output.append(text)

            return

        if isinstance(
            value,
            list
        ):

            for item in value:

                self._collect_text(
                    item,
                    output
                )

            return

        if isinstance(
            value,
            dict
        ):

            if (
                "text" in value
                and
                isinstance(
                    value["text"],
                    str
                )
            ):

                text = value[
                    "text"
                ].strip()

                if text:
                    output.append(text)

            # Only traverse content-bearing fields.
            for key in [
                "children",
                "content",
                "process",
                "documents",
                "benefits",
                "eligibilityDescription"
            ]:

                if key in value:

                    self._collect_text(
                        value[key],
                        output
                    )

    # =========================================================
    # HELPERS
    # =========================================================

    @staticmethod
    def _label_value(
        value: Any
    ) -> str:

        if isinstance(
            value,
            dict
        ):

            return str(
                value.get(
                    "label"
                )
                or
                value.get(
                    "value"
                )
                or
                ""
            ).strip()

        if value is None:
            return ""

        return str(value).strip()

    @staticmethod
    def _clean(
        value: Any
    ) -> str:

        if value is None:
            return ""

        text = str(value)

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    def _clean_markdown(
        self,
        text: str
    ) -> str:

        text = (
            text.replace(
                "<br>",
                "\n"
            )
            .replace(
                "<br/>",
                "\n"
            )
            .replace(
                "<br />",
                "\n"
            )
        )

        text = re.sub(
            r"\n{3,}",
            "\n\n",
            text
        )

        return text.strip()

    def _lines_to_items(
        self,
        text: str
    ) -> list[str]:

        text = self._clean_markdown(
            text
        )

        result = []

        for line in text.splitlines():

            line = line.strip()

            line = re.sub(
                r"^[\-\*\u2022]+\s*",
                "",
                line
            )

            line = re.sub(
                r"^\d+[\.\)]\s*",
                "",
                line
            )

            if line:

                result.append(line)

        return self._deduplicate(
            result
        )

    @staticmethod
    def _deduplicate(
        values: list
    ) -> list:

        result = []
        seen = set()

        for value in values:

            value = str(
                value
            ).strip()

            key = value.lower()

            if (
                not value
                or
                key in seen
            ):
                continue

            seen.add(key)

            result.append(value)

        return result

    # =========================================================
    # EMPTY
    # =========================================================

    @staticmethod
    def empty_result():

        return {
            "name": "",
            "description": "",
            "documents": [],
            "documents_verified": False,
            "benefits": [],
            "eligibility_text": "",
            "application_steps": [],
            "application_urls": [],
            "detail_verified": False
        }