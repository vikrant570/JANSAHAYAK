import re
from copy import deepcopy


class SchemeRelevanceFilter:
    """
    Filters and reranks schemes after FAISS retrieval.

    Goals:
    ----------------------------------------------------------
    1. Keep semantic search from FAISS.
    2. Detect the user's actual assistance domain.
    3. Remove schemes whose PRIMARY PURPOSE does not match.
    4. Avoid false positives caused by one keyword appearing
       somewhere in a long scheme description.
    5. Prefer "no result" over an obviously irrelevant result.
    """

    # =========================================================
    # USER DOMAIN KEYWORDS
    # =========================================================

    DOMAIN_KEYWORDS = {

        "agriculture": {
            "farmer",
            "farmers",
            "farming",
            "farm",
            "agriculture",
            "agricultural",
            "agri",
            "kisan",
            "crop",
            "crops",
            "irrigation",
            "tractor",
            "fertilizer",
            "fertiliser",
            "seed",
            "seeds",
            "dairy",
            "livestock",
            "horticulture",
            "fisheries",
            "animal husbandry",
        },

        "education": {
            "student",
            "students",
            "school",
            "college",
            "university",
            "education",
            "scholarship",
            "scholarships",
            "tuition",
            "fees",
            "matric",
            "fellowship",
            "study",
            "studies",
        },

        "business": {
            "business",
            "entrepreneur",
            "entrepreneurship",
            "startup",
            "start-up",
            "enterprise",
            "greenfield",
            "self employment",
            "self-employment",
            "vendor",
            "street vendor",
            "msme",
            "small business",
            "business loan",
        },

        "insurance": {
            "insurance",
            "insured",
            "bima",
            "accident insurance",
            "accidental insurance",
            "death cover",
            "disability cover",
        },

        "employment": {
            "job",
            "jobs",
            "employment",
            "unemployed",
            "unemployment",
            "jobless",
            "skill development",
            "vocational training",
        },

        "housing": {
            "house",
            "housing",
            "home",
            "awas",
            "shelter",
        },

        "health": {
            "health",
            "healthcare",
            "medical",
            "hospital",
            "treatment",
            "medicine",
        },

        "pension": {
            "pension",
            "retirement",
            "senior citizen",
            "elderly",
            "old age",
        },

        "disability": {
            "disabled",
            "disability",
            "divyang",
            "differently abled",
        },
    }

    # =========================================================
    # STRONG PURPOSE INDICATORS
    # =========================================================
    #
    # These are stronger than ordinary domain keywords.
    #
    # Example:
    # "activities allied to agriculture" should NOT convert
    # an entrepreneurship scheme into a farmer-support scheme.
    # =========================================================

    BUSINESS_PURPOSE_TERMS = {
        "entrepreneur",
        "entrepreneurs",
        "entrepreneurship",
        "greenfield",
        "green field",
        "enterprise",
        "enterprises",
        "startup",
        "start-up",
        "msme",
        "business loan",
        "setting up a business",
        "setting up an enterprise",
    }

    INSURANCE_PURPOSE_TERMS = {
        "insurance scheme",
        "accident insurance",
        "accidental death",
        "death cover",
        "disability cover",
        "suraksha bima",
        "bima yojana",
    }

    EDUCATION_PURPOSE_TERMS = {
        "scholarship",
        "post matric",
        "post-matric",
        "pre matric",
        "pre-matric",
        "fellowship",
        "students",
        "student scholarship",
    }

    PENSION_PURPOSE_TERMS = {
        "pension scheme",
        "old age pension",
        "senior citizen pension",
    }

    DISABILITY_PURPOSE_TERMS = {
        "disability scheme",
        "disabled persons",
        "persons with disabilities",
        "divyang",
    }

    # =========================================================
    # AGRICULTURE STRONG TERMS
    # =========================================================
    #
    # These indicate that agriculture is likely a main purpose,
    # rather than a casual mention.
    # =========================================================

    STRONG_AGRICULTURE_TERMS = {
        "farmer",
        "farmers",
        "kisan",
        "crop",
        "crops",
        "irrigation",
        "agriculture scheme",
        "agricultural scheme",
        "agricultural assistance",
        "farmer assistance",
        "farmers welfare",
        "farmer welfare",
        "agricultural subsidy",
        "crop insurance",
        "farm equipment",
        "agricultural equipment",
        "horticulture",
        "livestock",
        "animal husbandry",
        "fisheries",
        "dairy farmers",
    }

    # =========================================================
    # MAIN RERANK
    # =========================================================

    def rerank(
        self,
        query: str,
        profile: dict | None,
        results: list[dict],
        top_k: int = 3
    ) -> list[dict]:

        if not results:
            return []

        profile = profile or {}

        user_context = self._build_user_context(
            query=query,
            profile=profile
        )

        user_domains = self._detect_domains(
            user_context
        )

        # -----------------------------------------------------
        # Detect stronger user intents separately
        # -----------------------------------------------------

        wants_business = (
            "business" in user_domains
        )

        wants_insurance = (
            "insurance" in user_domains
        )

        wants_education = (
            "education" in user_domains
        )

        wants_agriculture = (
            "agriculture" in user_domains
        )

        wants_pension = (
            "pension" in user_domains
        )

        wants_disability = (
            "disability" in user_domains
        )

        occupation = self._clean_text(
            profile.get(
                "occupation",
                ""
            )
        )

        rescored_results = []

        # =====================================================
        # EACH FAISS CANDIDATE
        # =====================================================

        for result in results:

            if not isinstance(
                result,
                dict
            ):
                continue

            item = deepcopy(
                result
            )

            scheme = item.get(
                "scheme",
                {}
            )

            if not isinstance(
                scheme,
                dict
            ):
                continue

            scheme_name = self._clean_text(
                scheme.get(
                    "name",
                    ""
                )
            )

            scheme_text = self._scheme_text(
                scheme
            )

            base_score = self._normalize_score(
                item.get(
                    "score",
                    0
                )
            )

            # =================================================
            # PURPOSE CLASSIFICATION
            # =================================================

            business_scheme = self._contains_any(
                scheme_name + " " + scheme_text,
                self.BUSINESS_PURPOSE_TERMS
            )

            insurance_scheme = self._contains_any(
                scheme_name + " " + scheme_text,
                self.INSURANCE_PURPOSE_TERMS
            )

            education_scheme = self._contains_any(
                scheme_name + " " + scheme_text,
                self.EDUCATION_PURPOSE_TERMS
            )

            pension_scheme = self._contains_any(
                scheme_name + " " + scheme_text,
                self.PENSION_PURPOSE_TERMS
            )

            disability_scheme = self._contains_any(
                scheme_name + " " + scheme_text,
                self.DISABILITY_PURPOSE_TERMS
            )

            strong_agriculture_scheme = (
                self._contains_any(
                    scheme_name,
                    self.STRONG_AGRICULTURE_TERMS
                )
                or
                self._contains_any(
                    self._primary_scheme_text(
                        scheme
                    ),
                    self.STRONG_AGRICULTURE_TERMS
                )
            )

            # =================================================
            # HARD PURPOSE FILTER
            # =================================================

            # -------------------------------------------------
            # BUSINESS SCHEMES
            # -------------------------------------------------
            #
            # Stand-Up India should not be returned merely
            # because its description mentions activities
            # allied to agriculture.
            #
            # User must actually express business /
            # entrepreneurship intent.
            # -------------------------------------------------

            if (
                business_scheme
                and not wants_business
            ):
                continue

            # -------------------------------------------------
            # INSURANCE
            # -------------------------------------------------

            if (
                insurance_scheme
                and not wants_insurance
            ):
                farmer_specific_insurance = (
                    wants_agriculture
                    and strong_agriculture_scheme
                )

                if not farmer_specific_insurance:
                    continue

            # -------------------------------------------------
            # EDUCATION / SCHOLARSHIP
            # -------------------------------------------------

            if (
                education_scheme
                and not wants_education
            ):
                continue

            # -------------------------------------------------
            # PENSION
            # -------------------------------------------------

            if (
                pension_scheme
                and not wants_pension
            ):
                continue

            # -------------------------------------------------
            # DISABILITY
            # -------------------------------------------------

            if (
                disability_scheme
                and not wants_disability
            ):
                continue

            # =================================================
            # IMPROVED FARMER / AGRICULTURE RULE
            # =================================================

            full_scheme_domains = self._detect_domains(
                scheme_text
            )

            if wants_agriculture:

                agriculture_match = (
                    strong_agriculture_scheme
                    or "agriculture" in full_scheme_domains
                )

                # Reject only when there is genuinely no
                # agriculture evidence at all.
                if not agriculture_match:

                    # Allow only unusually strong semantic matches
                    # as a fallback.
                    if base_score < 0.60:
                        continue

            # =================================================
            # GENERAL DOMAIN DETECTION
            # =================================================

            scheme_domains = self._detect_domains(
                scheme_text
            )

            matching_domains = (
                user_domains
                & scheme_domains
            )

            # =================================================
            # SCORE
            # =================================================

            final_score = base_score

            # Strong agriculture match
            if wants_agriculture:

                if strong_agriculture_scheme:

                    # Very clear farmer/agriculture scheme
                    final_score += 0.20

                elif "agriculture" in full_scheme_domains:

                    # Agriculture is present in description/content,
                    # even if not strongly present in title/category.
                    final_score += 0.12

            # Other matching domains
            if matching_domains:
                final_score += 0.10

            # Occupation directly appears in scheme text
            if (
                occupation
                and len(occupation) > 2
                and self._contains_phrase(
                    scheme_text,
                    occupation
                )
            ):
                final_score += 0.08

            # Query ↔ scheme lexical overlap
            lexical_score = self._lexical_overlap(
                query=query,
                scheme_text=scheme_text
            )

            final_score += (
                lexical_score * 0.10
            )

            # =================================================
            # MINIMUM RELEVANCE
            # =================================================

            final_score = max(
                0.0,
                min(
                    final_score,
                    1.0
                )
            )

            # Don't show weak recommendations.
            if final_score < 0.42:
                continue

            item["score"] = (
                final_score
            )

            # Debug information.
            # This is not shown by ResponseFormatter,
            # but can be useful during development.

            item["_relevance"] = {

                "user_domains":
                    sorted(user_domains),

                "scheme_domains":
                    sorted(scheme_domains),

                "business_scheme":
                    business_scheme,

                "insurance_scheme":
                    insurance_scheme,

                "education_scheme":
                    education_scheme,

                "strong_agriculture_scheme":
                    strong_agriculture_scheme,

                "semantic_score":
                    round(
                        base_score,
                        3
                    ),

                "final_score":
                    round(
                        final_score,
                        3
                    ),
            }

            rescored_results.append(
                item
            )

        # =====================================================
        # SORT
        # =====================================================

        rescored_results.sort(
            key=lambda item: item.get(
                "score",
                0
            ),
            reverse=True
        )

        return rescored_results[
            :top_k
        ]

    # =========================================================
    # USER CONTEXT
    # =========================================================

    def _build_user_context(
        self,
        query: str,
        profile: dict
    ) -> str:

        values = [

            query,

            profile.get(
                "occupation",
                ""
            ),

            profile.get(
                "state",
                ""
            ),

            profile.get(
                "education",
                ""
            ),

            profile.get(
                "gender",
                ""
            ),
        ]

        return self._clean_text(
            " ".join(
                str(value or "")
                for value in values
            )
        )

    # =========================================================
    # PRIMARY SCHEME TEXT
    # =========================================================

    def _primary_scheme_text(
        self,
        scheme: dict
    ) -> str:
        """
        Text used to identify the MAIN domain of a scheme.

        We deliberately avoid relying too much on the full
        description because descriptions often mention many
        secondary areas.
        """

        values = [
            scheme.get(
                "name",
                ""
            ),
            scheme.get(
                "category",
                ""
            ),
            scheme.get(
                "categories",
                ""
            ),
            scheme.get(
                "target_group",
                ""
            ),
            scheme.get(
                "target_groups",
                ""
            ),
            scheme.get(
                "tags",
                ""
            ),
        ]

        return self._clean_text(
            " ".join(
                str(value or "")
                for value in values
            )
        )

    # =========================================================
    # FULL SCHEME TEXT
    # =========================================================

    def _scheme_text(
        self,
        scheme: dict
    ) -> str:

        fields = [
            "name",
            "description",
            "category",
            "categories",
            "benefits",
            "eligibility",
            "target_group",
            "target_groups",
            "tags",
        ]

        values = []

        for field in fields:

            value = scheme.get(
                field
            )

            if value:
                values.append(
                    str(value)
                )

        return self._clean_text(
            " ".join(values)
        )

    # =========================================================
    # DOMAIN DETECTION
    # =========================================================

    def _detect_domains(
        self,
        text: str
    ) -> set[str]:

        text = self._clean_text(
            text
        )

        domains = set()

        for domain, keywords in (
            self.DOMAIN_KEYWORDS.items()
        ):

            if self._contains_any(
                text,
                keywords
            ):

                domains.add(
                    domain
                )

        return domains

    # =========================================================
    # CONTAINS ANY
    # =========================================================

    def _contains_any(
        self,
        text: str,
        keywords: set[str]
    ) -> bool:

        for keyword in keywords:

            if self._contains_phrase(
                text,
                keyword
            ):
                return True

        return False

    # =========================================================
    # PHRASE MATCH
    # =========================================================

    @staticmethod
    def _contains_phrase(
        text: str,
        phrase: str
    ) -> bool:

        text = str(
            text or ""
        ).lower()

        phrase = str(
            phrase or ""
        ).lower().strip()

        if not phrase:
            return False

        # Multiword phrase
        if " " in phrase:
            return phrase in text

        return bool(
            re.search(
                rf"\b{re.escape(phrase)}\b",
                text
            )
        )

    # =========================================================
    # LEXICAL OVERLAP
    # =========================================================

    @staticmethod
    def _lexical_overlap(
        query: str,
        scheme_text: str
    ) -> float:

        query_words = set(
            re.findall(
                r"\b[a-zA-Z]{3,}\b",
                str(query).lower()
            )
        )

        scheme_words = set(
            re.findall(
                r"\b[a-zA-Z]{3,}\b",
                str(scheme_text).lower()
            )
        )

        stop_words = {
            "the",
            "and",
            "for",
            "from",
            "with",
            "this",
            "that",
            "looking",
            "need",
            "needs",
            "want",
            "wants",
            "help",
            "scheme",
            "schemes",
            "government",
            "support",
            "assistance",
            "financial",
        }

        query_words -= stop_words

        if not query_words:
            return 0.0

        common_words = (
            query_words
            & scheme_words
        )

        return (
            len(common_words)
            / len(query_words)
        )

    # =========================================================
    # SCORE NORMALIZATION
    # =========================================================

    @staticmethod
    def _normalize_score(
        score
    ) -> float:

        try:

            value = float(
                score
            )

        except (
            TypeError,
            ValueError
        ):

            return 0.0

        if 0 <= value <= 1:
            return value

        if 1 < value <= 100:
            return value / 100

        return 0.0

    # =========================================================
    # CLEAN TEXT
    # =========================================================

    @staticmethod
    def _clean_text(
        text
    ) -> str:

        text = str(
            text or ""
        ).lower()

        text = text.replace(
            "\n",
            " "
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()