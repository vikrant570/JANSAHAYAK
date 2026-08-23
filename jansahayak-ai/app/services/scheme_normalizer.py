import re
from typing import Any


class SchemeNormalizer:
    """
    Normalize scheme records from:
    - MyScheme raw API format
    - India.gov.in raw API format
    - Already-normalized connector output

    into one common JanSahayak scheme structure.
    """

    def normalize(self, raw: dict) -> dict:

        if not isinstance(raw, dict):
            raise ValueError(
                "Scheme record must be a dictionary."
            )

        # =====================================================
        # 1. RAW MYSCHEME FORMAT
        # =====================================================
        #
        # Typical structure:
        #
        # {
        #     "id": "...",
        #     "fields": {
        #         "schemeName": "...",
        #         "slug": "...",
        #         ...
        #     }
        # }

        if (
            isinstance(
                raw.get("fields"),
                dict
            )
            and raw.get("fields")
        ):

            return self._normalize_myscheme(
                raw
            )

        # =====================================================
        # 2. ALREADY NORMALIZED FORMAT
        # =====================================================
        #
        # Some connectors may already return:
        #
        # {
        #     "name": "...",
        #     "description": "...",
        #     "official_source": "...",
        #     ...
        # }
        #
        # IMPORTANT:
        # Check this BEFORE India.gov detection.
        # Otherwise MyScheme normalized records may be
        # incorrectly classified as India.gov records.

        if (
            "name" in raw
            and
            (
                "official_source" in raw
                or
                "source_name" in raw
            )
        ):

            return self._normalize_existing(
                raw
            )

        # =====================================================
        # 3. RAW INDIA.GOV FORMAT
        # =====================================================

        if (
            "title" in raw
            or
            "schemeCategory" in raw
        ):

            return self._normalize_india_gov(
                raw
            )

        raise ValueError(
            "Unknown scheme source format."
        )

    # =========================================================
    # MYSCHEME
    # =========================================================

    def _normalize_myscheme(
        self,
        raw: dict
    ) -> dict:

        fields = raw.get(
            "fields",
            {}
        )

        name = self._clean_text(
            fields.get("schemeName")
            or
            fields.get("schemeShortTitle")
        )

        if not name:

            raise ValueError(
                "MyScheme record has no scheme name."
            )

        slug = self._clean_text(
            fields.get("slug")
        )

        description = self._clean_text(
            fields.get(
                "briefDescription"
            )
        )

        categories = self._to_list(
            fields.get(
                "schemeCategory"
            )
        )

        states = self._to_list(
            fields.get(
                "beneficiaryState"
            )
        )

        tags = self._to_list(
            fields.get(
                "tags"
            )
        )

        ministry = self._clean_text(
            fields.get(
                "nodalMinistryName"
            )
        )

        level = self._clean_text(
            fields.get(
                "level"
            )
        )

        scheme_for = self._to_list(
            fields.get(
                "schemeFor"
            )
        )

        close_date = (
            fields.get(
                "schemeCloseDate"
            )
        )

        # -----------------------------------------------------
        # Official MyScheme URL
        # -----------------------------------------------------

        official_source = ""

        if slug:

            official_source = (
                "https://www.myscheme.gov.in/"
                f"schemes/{slug}"
            )

        # -----------------------------------------------------
        # ID
        # -----------------------------------------------------

        scheme_id = self._clean_text(
            raw.get("id")
        )

        if not scheme_id:

            scheme_id = self._slugify(
                name
            )

        return {

            "id":
                scheme_id,

            "name":
                name,

            "category":
                (
                    categories[0]
                    if categories
                    else "general"
                ),

            "description":
                description,

            "target_users":
                scheme_for,

            "states":
                states,

            "eligibility": {
                "age_min": None,
                "age_max": None,
                "income_max": None,
                "occupation": [],
                "education": [],
                "other_conditions": []
            },

            "benefits":
                [],

            "documents":
                [],

            "documents_verified":
                False,

            "application_steps":
                [],

            "official_source":
                official_source,

            "source_name":
                "myScheme",

            "authority":
                "Government of India",

            "nodal_ministry":
                ministry,

            "level":
                level,

            "tags":
                tags,

            "slug":
                slug,

            "scheme_close_date":
                close_date,

            "last_verified":
                "",

            "verification_status":
                "verified",

            "confidence":
                0.95
        }

    # =========================================================
    # INDIA.GOV.IN
    # =========================================================

    def _normalize_india_gov(
        self,
        raw: dict
    ) -> dict:

        name = self._clean_text(
            raw.get("title")
            or
            raw.get("schemeName")
        )

        if not name:

            raise ValueError(
                "India.gov record has no scheme title."
            )

        description = self._clean_text(
            raw.get(
                "description"
            )
        )

        categories = self._to_list(
            raw.get(
                "schemeCategory"
            )
        )

        states = self._to_list(
            raw.get(
                "beneficiaryState"
            )
        )

        tags = self._to_list(
            raw.get(
                "tags"
            )
        )

        slug = self._clean_text(
            raw.get(
                "slug"
            )
        )

        ministry = self._clean_text(
            raw.get(
                "ministry"
            )
        )

        # -----------------------------------------------------
        # Preserve URL if connector/API already supplied one
        # -----------------------------------------------------

        official_source = self._clean_text(
            raw.get(
                "official_source"
            )
            or
            raw.get(
                "source_url"
            )
            or
            raw.get(
                "url"
            )
        )

        # -----------------------------------------------------
        # Fallback India.gov URL
        #
        # NOTE:
        # This URL may return 404 for some schemes.
        # We still store it as source reference, but
        # detail extraction must verify HTTP response.
        # -----------------------------------------------------

        if (
            not official_source
            and slug
        ):

            official_source = (
                "https://www.india.gov.in/"
                "my-government/schemes/"
                f"{slug}"
            )

        scheme_id = self._clean_text(
            raw.get("id")
        )

        if not scheme_id:

            scheme_id = self._slugify(
                name
            )

        return {

            "id":
                scheme_id,

            "name":
                name,

            "category":
                (
                    categories[0]
                    if categories
                    else "general"
                ),

            "description":
                description,

            "target_users":
                [],

            "states":
                states,

            "eligibility": {
                "age_min": None,
                "age_max": None,
                "income_max": None,
                "occupation": [],
                "education": [],
                "other_conditions": []
            },

            "benefits":
                [],

            "documents":
                [],

            "documents_verified":
                False,

            "application_steps":
                [],

            "official_source":
                official_source,

            "source_name":
                "india.gov.in",

            "authority":
                "Government of India",

            "nodal_ministry":
                ministry,

            "level":
                self._detect_india_level(
                    raw,
                    states
                ),

            "tags":
                tags,

            "slug":
                slug,

            "scheme_close_date":
                None,

            "last_verified":
                "",

            "verification_status":
                "verified",

            "confidence":
                0.95
        }

    # =========================================================
    # ALREADY NORMALIZED RECORD
    # =========================================================

    def _normalize_existing(
        self,
        raw: dict
    ) -> dict:

        result = dict(
            raw
        )

        # -----------------------------------------------------
        # Normalize important text fields
        # -----------------------------------------------------

        result["name"] = self._clean_text(
            result.get("name")
        )

        result["description"] = self._clean_text(
            result.get("description")
        )

        result["official_source"] = self._clean_text(
            result.get(
                "official_source"
            )
        )

        # -----------------------------------------------------
        # Correct source attribution using URL
        # -----------------------------------------------------

        official_source_lower = (
            result[
                "official_source"
            ].lower()
        )

        current_source = self._clean_text(
            result.get(
                "source_name"
            )
        )

        if (
            "myscheme.gov.in"
            in official_source_lower
        ):

            result[
                "source_name"
            ] = "myScheme"

        elif (
            "india.gov.in"
            in official_source_lower
        ):

            result[
                "source_name"
            ] = "india.gov.in"

        elif current_source:

            # Normalize common spelling/casing
            source_lower = (
                current_source.lower()
            )

            if "myscheme" in source_lower:

                result[
                    "source_name"
                ] = "myScheme"

            elif (
                "india.gov"
                in source_lower
            ):

                result[
                    "source_name"
                ] = "india.gov.in"

            else:

                result[
                    "source_name"
                ] = current_source

        else:

            result[
                "source_name"
            ] = "Government Source"

        # -----------------------------------------------------
        # Normalize lists
        # -----------------------------------------------------

        result["target_users"] = (
            self._to_list(
                result.get(
                    "target_users"
                )
            )
        )

        result["states"] = (
            self._to_list(
                result.get(
                    "states"
                )
            )
        )

        result["benefits"] = (
            self._to_list(
                result.get(
                    "benefits"
                )
            )
        )

        result["documents"] = (
            self._to_list(
                result.get(
                    "documents"
                )
            )
        )

        result[
            "application_steps"
        ] = self._to_list(
            result.get(
                "application_steps"
            )
        )

        result["tags"] = (
            self._to_list(
                result.get(
                    "tags"
                )
            )
        )

        # -----------------------------------------------------
        # Eligibility
        # -----------------------------------------------------

        eligibility = result.get(
            "eligibility"
        )

        if not isinstance(
            eligibility,
            dict
        ):

            eligibility = {}

        eligibility.setdefault(
            "age_min",
            None
        )

        eligibility.setdefault(
            "age_max",
            None
        )

        eligibility.setdefault(
            "income_max",
            None
        )

        eligibility[
            "occupation"
        ] = self._to_list(
            eligibility.get(
                "occupation"
            )
        )

        eligibility[
            "education"
        ] = self._to_list(
            eligibility.get(
                "education"
            )
        )

        eligibility[
            "other_conditions"
        ] = self._to_list(
            eligibility.get(
                "other_conditions"
            )
        )

        result[
            "eligibility"
        ] = eligibility

        # -----------------------------------------------------
        # Documents verification
        # -----------------------------------------------------

        result.setdefault(
            "documents_verified",
            False
        )

        result[
            "documents_verified"
        ] = bool(
            result.get(
                "documents_verified"
            )
        )

        # -----------------------------------------------------
        # Other defaults
        # -----------------------------------------------------

        result.setdefault(
            "category",
            "general"
        )

        result.setdefault(
            "authority",
            "Government of India"
        )

        result.setdefault(
            "nodal_ministry",
            ""
        )

        result.setdefault(
            "level",
            ""
        )

        result.setdefault(
            "slug",
            ""
        )

        result.setdefault(
            "scheme_close_date",
            None
        )

        result.setdefault(
            "last_verified",
            ""
        )

        result.setdefault(
            "verification_status",
            "verified"
        )

        result.setdefault(
            "confidence",
            0.95
        )

        # -----------------------------------------------------
        # Ensure ID exists
        # -----------------------------------------------------

        if not result.get(
            "id"
        ):

            result["id"] = (
                self._slugify(
                    result.get(
                        "name",
                        ""
                    )
                )
            )

        return result

    # =========================================================
    # INDIA.GOV LEVEL DETECTION
    # =========================================================

    def _detect_india_level(
        self,
        raw: dict,
        states: list
    ) -> str:

        # Use explicit level when present
        explicit_level = self._clean_text(
            raw.get("level")
        )

        if explicit_level:

            return explicit_level

        # State-specific scheme
        if states:

            normalized_states = [
                state.lower()
                for state in states
            ]

            if (
                "all" not in normalized_states
                and
                "all india"
                not in normalized_states
            ):

                return "State"

        return "Central"

    # =========================================================
    # HELPERS
    # =========================================================

    @staticmethod
    def _clean_text(
        value: Any
    ) -> str:

        if value is None:

            return ""

        if isinstance(
            value,
            str
        ):

            return value.strip()

        return str(
            value
        ).strip()

    @staticmethod
    def _to_list(
        value: Any
    ) -> list:

        if value is None:

            return []

        if isinstance(
            value,
            list
        ):

            result = []

            for item in value:

                if item is None:
                    continue

                text = str(
                    item
                ).strip()

                if text:

                    result.append(
                        text
                    )

            return result

        if isinstance(
            value,
            tuple
        ):

            return [
                str(item).strip()
                for item in value
                if (
                    item is not None
                    and
                    str(item).strip()
                )
            ]

        if isinstance(
            value,
            str
        ):

            value = value.strip()

            if not value:

                return []

            return [
                value
            ]

        return [
            str(value).strip()
        ]

    @staticmethod
    def _slugify(
        text: str
    ) -> str:

        text = str(
            text or ""
        ).lower()

        text = re.sub(
            r"[^a-z0-9]+",
            "-",
            text
        )

        return text.strip("-")