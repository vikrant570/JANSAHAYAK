from app.services.retrieval import SchemeRetriever
from app.services.eligibility import calculate_eligibility_score
from app.services.document_checklist import DocumentChecklist
from app.services.action_plan import ActionPlanGenerator
from app.services.recommendation_ranker import RecommendationRanker


class JanSahayakAnalyzer:
    """
    Main AI analysis pipeline for JanSahayak.

    Pipeline:

        User Query
             ↓
        Semantic Retrieval
             ↓
        Eligibility Analysis
             ↓
        Recommendation Ranking
             ↓
        Documents
             ↓
        Action Plan
             ↓
        AI Explanation
    """

    def __init__(self):

        # --------------------------------------------------
        # CORE SERVICES
        # --------------------------------------------------

        self.retriever = SchemeRetriever()

        self.document_checklist = DocumentChecklist()

        self.action_plan_generator = ActionPlanGenerator()

        self.rank = RecommendationRanker()

    # ======================================================
    # AI EXPLANATION
    # ======================================================

    def _generate_explanation(
        self,
        scheme: dict,
        eligibility: dict,
        user: dict
    ) -> str:

        name = scheme.get(
            "name",
            "This scheme"
        )

        description = scheme.get(
            "description",
            ""
        )

        status = eligibility.get(
            "status",
            "unknown"
        )

        # --------------------------------------------------
        # ELIGIBILITY MESSAGE
        # --------------------------------------------------

        if status == "likely_eligible":

            eligibility_text = (
                "Based on the information you provided, "
                "you appear to meet the available eligibility "
                "conditions."
            )

        elif status == "unlikely_eligible":

            eligibility_text = (
                "Based on the available eligibility "
                "information, you may not currently meet "
                "all conditions for this scheme."
            )

        elif status == "needs_verification":

            eligibility_text = (
                "Some eligibility information is missing, "
                "so the official source should be checked "
                "before applying."
            )

        else:

            eligibility_text = (
                "Eligibility could not be fully determined "
                "from the available information."
            )

        # --------------------------------------------------
        # DESCRIPTION
        # --------------------------------------------------

        if description:

            return (
                f"{name} may be relevant to your request. "
                f"{eligibility_text} "
                f"Official description: {description} "
                f"Always verify the latest eligibility and "
                f"application requirements on the official "
                f"government source."
            )

        return (
            f"{name} may be relevant to your request. "
            f"{eligibility_text} "
            f"Always verify the latest eligibility and "
            f"application requirements on the official "
            f"government source."
        )

    # ======================================================
    # SAFE SCORE
    # ======================================================

    def _safe_float(
        self,
        value,
        default=0.0
    ):

        try:
            return float(value)

        except (
            TypeError,
            ValueError
        ):

            return default

    # ======================================================
    # ANALYZE
    # ======================================================

    def analyze(
        self,
        query: str,
        user: dict
    ) -> dict:

        # --------------------------------------------------
        # NORMALIZE INPUT
        # --------------------------------------------------

        query = (
            query or ""
        ).strip()

        user = user or {}

        # --------------------------------------------------
        # 1. SEMANTIC RETRIEVAL
        # --------------------------------------------------

        schemes = self.retriever.search(
            query,
            top_k=10
        )

        if not schemes:

            return {

                "recommendations": [],

                "eligibility": [],

                "documents": [],

                "action_plan": [],

                "sources": [],

                "confidence": 0.0,

                "needs_verification": True,

                "message": (
                    "I could not find enough relevant "
                    "verified government schemes for "
                    "your request."
                )
            }

        # --------------------------------------------------
        # 2. ELIGIBILITY ANALYSIS
        # --------------------------------------------------

        eligibility_results = []

        for scheme in schemes:

            try:

                eligibility = (
                    calculate_eligibility_score(
                        scheme=scheme,
                        profile=user
                    )
                )

                # --------------------------------------------------
                # IMPORTANT:
                # Existing eligibility.py currently returns
                # a numeric score.
                # Convert it into a standard result object.
                # --------------------------------------------------

                eligibility_score = (
                    self._safe_float(
                        eligibility
                    )
                )

                if eligibility_score >= 0.50:

                    status = "likely_eligible"

                elif eligibility_score >= 0.20:

                    status = "needs_verification"

                else:

                    status = "unlikely_eligible"

                reasons = []

                # --------------------------------------------------
                # AGE
                # --------------------------------------------------

                age = user.get("age")

                scheme_eligibility = scheme.get(
                    "eligibility",
                    {}
                )

                age_min = scheme_eligibility.get(
                    "age_min"
                )

                age_max = scheme_eligibility.get(
                    "age_max"
                )

                if age is not None:

                    if (
                        age_min is not None
                        and age < age_min
                    ):

                        reasons.append(
                            f"Age is below the minimum "
                            f"requirement of {age_min}."
                        )

                    elif (
                        age_max is not None
                        and age > age_max
                    ):

                        reasons.append(
                            f"Age is above the maximum "
                            f"requirement of {age_max}."
                        )

                    else:

                        reasons.append(
                            "Age requirement appears compatible."
                        )

                # --------------------------------------------------
                # STATE
                # --------------------------------------------------

                states = [
                    str(x).lower()
                    for x in scheme.get(
                        "states",
                        []
                    )
                ]

                user_state = str(
                    user.get(
                        "state",
                        ""
                    )
                ).lower()

                if user_state and states:

                    if (
                        "all" in states
                        or user_state in states
                    ):

                        reasons.append(
                            "Your state appears to be covered."
                        )

                    else:

                        reasons.append(
                            "The available state information "
                            "may not cover your state."
                        )

                # --------------------------------------------------
                # OCCUPATION
                # --------------------------------------------------

                occupation = str(
                    user.get(
                        "occupation",
                        ""
                    )
                ).lower()

                occupations = [
                    str(x).lower()
                    for x in scheme_eligibility.get(
                        "occupation",
                        []
                    )
                ]

                if occupation and occupations:

                    if occupation in occupations:

                        reasons.append(
                            "Your occupation appears compatible."
                        )

                    else:

                        reasons.append(
                            "Your occupation may not match "
                            "the listed occupation criteria."
                        )

                eligibility_result = {

                    "status": status,

                    "score": eligibility_score,

                    "reasons": reasons
                }

                eligibility_results.append({

                    "scheme_id": scheme.get(
                        "id"
                    ),

                    "scheme_name": scheme.get(
                        "name"
                    ),

                    **eligibility_result

                })

            except Exception as error:

                print(
                    "Eligibility analysis error:",
                    error
                )

                eligibility_results.append({

                    "scheme_id": scheme.get(
                        "id"
                    ),

                    "scheme_name": scheme.get(
                        "name"
                    ),

                    "status": "needs_verification",

                    "score": 0.0,

                    "reasons": [
                        "Eligibility could not be "
                        "fully determined."
                    ]

                })

        # --------------------------------------------------
        # 3. RECOMMENDATION RANKING
        # --------------------------------------------------

        try:

            ranked = self.rank.rank(
                schemes,
                eligibility_results
            )

        except Exception as error:

            print(
                "Recommendation ranking error:",
                error
            )

            # --------------------------------------------------
            # SAFE FALLBACK
            # --------------------------------------------------

            ranked = []

            for index, scheme in enumerate(
                schemes
            ):

                retrieval_score = (
                    self._safe_float(
                        scheme.get(
                            "retrieval_score",
                            0.0
                        )
                    )
                )

                eligibility_score = (
                    self._safe_float(
                        eligibility_results[index].get(
                            "score",
                            0.0
                        )
                    )
                )

                final_score = (
                    retrieval_score * 0.70
                    +
                    eligibility_score * 0.30
                )

                ranked.append({

                    "scheme": scheme,

                    "eligibility": (
                        eligibility_results[index]
                    ),

                    "score": final_score

                })

            ranked.sort(
                key=lambda x: x.get(
                    "score",
                    0.0
                ),
                reverse=True
            )

        # --------------------------------------------------
        # 4. BUILD FINAL RECOMMENDATIONS
        # --------------------------------------------------

        recommendations = []

        final_eligibility = []

        document_results = []

        sources = []

        # --------------------------------------------------
        # LIMIT TO TOP 5
        # --------------------------------------------------

        ranked = ranked[:5]

        for result in ranked:

            # --------------------------------------------------
            # HANDLE DIFFERENT RANKER OUTPUT FORMATS
            # --------------------------------------------------

            if isinstance(
                result,
                dict
            ):

                scheme = result.get(
                    "scheme",
                    result
                )

                ranking_score = (
                    result.get(
                        "score",
                        result.get(
                            "final_score",
                            scheme.get(
                                "retrieval_score",
                                0.0
                            )
                        )
                    )
                )

                eligibility = result.get(
                    "eligibility"
                )

            else:

                continue

            # --------------------------------------------------
            # FIND ELIGIBILITY
            # --------------------------------------------------

            if not eligibility:

                eligibility = next(
                    (
                        item
                        for item in eligibility_results
                        if item.get(
                            "scheme_id"
                        )
                        == scheme.get(
                            "id"
                        )
                    ),
                    {
                        "scheme_id":
                            scheme.get("id"),

                        "scheme_name":
                            scheme.get("name"),

                        "status":
                            "needs_verification",

                        "score":
                            0.0,

                        "reasons": []
                    }
                )

            # --------------------------------------------------
            # DOCUMENT CHECKLIST
            # --------------------------------------------------

            try:

                documents = (
                    self.document_checklist.generate(
                        scheme,
                        user.get(
                            "documents",
                            []
                        )
                    )
                )

            except Exception as error:

                print(
                    "Document checklist error:",
                    error
                )

                documents = {
                    "required_documents": [],
                    "missing_documents": []
                }

            # --------------------------------------------------
            # EXPLANATION
            # --------------------------------------------------

            explanation = (
                self._generate_explanation(
                    scheme,
                    eligibility,
                    user
                )
            )

            # --------------------------------------------------
            # RECOMMENDATION
            # --------------------------------------------------

            recommendations.append({

                "scheme_id":
                    scheme.get("id"),

                "name":
                    scheme.get("name"),

                "description":
                    scheme.get(
                        "description",
                        ""
                    ),

                "benefits":
                    scheme.get(
                        "benefits",
                        []
                    ),

                "category":
                    scheme.get(
                        "category",
                        "general"
                    ),

                "states":
                    scheme.get(
                        "states",
                        []
                    ),

                "ministry":
                    scheme.get(
                        "nodal_ministry",
                        scheme.get(
                            "ministry",
                            ""
                        )
                    ),

                "level":
                    scheme.get(
                        "level",
                        ""
                    ),

                "verification":
                    scheme.get(
                        "verification_status",
                        "verified"
                    ),

                "official_source":
                    scheme.get(
                        "official_source",
                        ""
                    ),

                "retrieval_score":
                    self._safe_float(
                        scheme.get(
                            "retrieval_score",
                            0.0
                        )
                    ),

                "final_score":
                    self._safe_float(
                        ranking_score
                    ),

                "eligibility_status":
                    eligibility.get(
                        "status",
                        "needs_verification"
                    ),

                "eligibility_score":
                    self._safe_float(
                        eligibility.get(
                            "score",
                            0.0
                        )
                    ),

                "explanation":
                    explanation

            })

            # --------------------------------------------------
            # ELIGIBILITY
            # --------------------------------------------------

            final_eligibility.append(
                eligibility
            )

            # --------------------------------------------------
            # DOCUMENTS
            # --------------------------------------------------

            document_results.append({

                "scheme_id":
                    scheme.get("id"),

                "scheme_name":
                    scheme.get("name"),

                **documents

            })

            # --------------------------------------------------
            # SOURCE
            # --------------------------------------------------

            sources.append({

                "source_name":
                    scheme.get(
                        "source_name",
                        "Official Government Source"
                    ),

                "source_url":
                    scheme.get(
                        "official_source",
                        ""
                    ),

                "last_verified":
                    scheme.get(
                        "last_verified",
                        ""
                    ),

                "verification_status":
                    scheme.get(
                        "verification_status",
                        "verified"
                    ),

                "confidence":
                    self._safe_float(
                        scheme.get(
                            "confidence",
                            0.0
                        )
                    )

            })

        # --------------------------------------------------
        # 5. ACTION PLAN
        # --------------------------------------------------

        action_plan = []

        if ranked:

            try:

                first_result = ranked[0]

                first_scheme = first_result.get(
                    "scheme",
                    first_result
                )

                first_eligibility = (
                    first_result.get(
                        "eligibility"
                    )
                )

                if not first_eligibility:

                    first_eligibility = (
                        final_eligibility[0]
                        if final_eligibility
                        else {}
                    )

                first_documents = (
                    document_results[0]
                    if document_results
                    else {}
                )

                action_plan = (
                    self.action_plan_generator.generate(
                        first_scheme,
                        first_eligibility,
                        first_documents
                    )
                )

            except Exception as error:

                print(
                    "Action plan generation error:",
                    error
                )

                action_plan = []

        # --------------------------------------------------
        # 6. OVERALL CONFIDENCE
        # --------------------------------------------------

        if recommendations:

            confidence_values = [

                self._safe_float(
                    item.get(
                        "confidence",
                        0.0
                    )
                )

                for item in sources

            ]

            confidence = max(
                confidence_values,
                default=0.0
            )

        else:

            confidence = 0.0

        # --------------------------------------------------
        # 7. FINAL RESULT
        # --------------------------------------------------

        return {

            "recommendations":
                recommendations,

            "eligibility":
                final_eligibility,

            "documents":
                document_results,

            "action_plan":
                action_plan,

            "sources":
                sources,

            "confidence":
                confidence,

            "needs_verification":
                False,

            "query":
                query,

            "user":
                user

        }


# ==========================================================
# BACKWARD COMPATIBILITY
# ==========================================================

_analyzer = None


def analyze_query(
    query: str,
    user: dict | None = None
) -> dict:

    global _analyzer

    if _analyzer is None:

        _analyzer = JanSahayakAnalyzer()

    return _analyzer.analyze(
        query=query,
        user=user or {}
    )