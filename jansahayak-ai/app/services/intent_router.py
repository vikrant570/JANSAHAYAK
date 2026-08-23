import re


class IntentRouter:
    """
    Lightweight intent router for JanSahayak.

    Supported intents:
    - greeting
    - gratitude
    - scheme_query
    - out_of_scope

    Only scheme_query should continue to the existing
    JanSahayak RAG / FAISS recommendation pipeline.
    """

    # ---------------------------------------------------------
    # GREETINGS
    # ---------------------------------------------------------

    GREETING_PATTERNS = {
        "hi",
        "hii",
        "hiii",
        "hello",
        "hey",
        "hey there",
        "hello there",
        "good morning",
        "good afternoon",
        "good evening",
        "namaste",
        "namaskar",
    }

    # ---------------------------------------------------------
    # GRATITUDE
    # ---------------------------------------------------------

    GRATITUDE_PATTERNS = {
        "thanks",
        "thank you",
        "thankyou",
        "thank u",
        "thx",
        "thanks a lot",
        "thank you so much",
        "okay thanks",
        "ok thanks",
        "great thanks",
    }

    # ---------------------------------------------------------
    # GOVERNMENT / SCHEME CONTEXT
    # ---------------------------------------------------------

    SCHEME_KEYWORDS = {
        # General government assistance
        "scheme",
        "schemes",
        "government scheme",
        "government schemes",
        "government help",
        "government support",
        "government assistance",
        "government benefit",
        "government benefits",
        "government program",
        "government programme",
        "government aid",
        "financial assistance",
        "financial help",
        "financial support",
        "financial aid",
        "benefit",
        "benefits",
        "assistance",
        "subsidy",
        "subsidies",
        "grant",
        "grants",
        "welfare",
        "aid",

        # Eligibility / application
        "eligible",
        "eligibility",
        "am i eligible",
        "can i apply",
        "how to apply",
        "apply",
        "application",
        "application process",
        "documents",
        "document",
        "required documents",
        "documents required",
        "requirements",
        "criteria",

        # Farmers / agriculture
        "farmer",
        "farmers",
        "farming",
        "agriculture",
        "agricultural",
        "crop",
        "crops",
        "irrigation",
        "farm equipment",
        "agriculture loan",
        "farmer loan",

        # Students / education
        "student",
        "students",
        "scholarship",
        "scholarships",
        "education support",
        "education loan",
        "college fees",
        "school fees",
        "tuition fees",
        "study support",

        # Women / children
        "woman",
        "women",
        "girl",
        "girls",
        "girl child",
        "women entrepreneur",
        "maternity",
        "pregnancy assistance",

        # Senior citizens
        "senior citizen",
        "senior citizens",
        "elderly",
        "old age",
        "old age pension",

        # Disability
        "disabled",
        "disability",
        "differently abled",
        "divyang",
        "divyangjan",

        # Employment
        "unemployed",
        "unemployment",
        "jobless",
        "employment assistance",
        "employment support",
        "self employment",

        # Business / startup
        "entrepreneur",
        "entrepreneurs",
        "startup",
        "start-up",
        "small business",
        "business loan",
        "business support",
        "msme",
        "street vendor",
        "street vendors",

        # Social categories
        "widow",
        "widow pension",
        "scheduled caste",
        "scheduled tribe",
        "sc student",
        "st student",
        "obc",
        "minority",

        # Common assistance categories
        "pension",
        "loan",
        "insurance",
        "housing",
        "housing assistance",
        "home loan",
        "healthcare",
        "health assistance",
        "medical assistance",
        "ration",
        "food assistance",
        "income support",
        "skill development",
        "livelihood",
    }

    # ---------------------------------------------------------
    # OUT-OF-SCOPE TOPICS
    # These are used only when there is no scheme context.
    # ---------------------------------------------------------

    OUT_OF_SCOPE_KEYWORDS = {
        "weather",
        "temperature today",
        "cricket",
        "football",
        "movie",
        "movies",
        "song",
        "songs",
        "joke",
        "jokes",
        "recipe",
        "cooking",
        "python code",
        "java code",
        "javascript code",
        "calculator code",
        "coding problem",
        "programming",
        "photosynthesis",
        "history question",
        "math problem",
    }

    # =========================================================
    # PUBLIC METHOD
    # =========================================================

    def detect_intent(self, query: str) -> str:
        """
        Detect the intent of a user message.

        Returns:
            greeting
            gratitude
            scheme_query
            out_of_scope
        """

        if not query or not query.strip():
            return "out_of_scope"

        cleaned = self._clean_text(query)

        # -----------------------------------------------------
        # 1. Exact greeting
        # -----------------------------------------------------

        if cleaned in self.GREETING_PATTERNS:
            return "greeting"

        # -----------------------------------------------------
        # 2. Exact gratitude
        # -----------------------------------------------------

        if cleaned in self.GRATITUDE_PATTERNS:
            return "gratitude"

        # -----------------------------------------------------
        # 3. Greeting + actual scheme question
        #
        # Example:
        # "Hi, I am a farmer looking for financial help"
        #
        # This must NOT stop at greeting.
        # -----------------------------------------------------

        if self._starts_with_greeting(cleaned):

            if self._contains_scheme_context(cleaned):
                return "scheme_query"

            return "greeting"

        # -----------------------------------------------------
        # 4. Gratitude + continued scheme query
        #
        # Example:
        # "Thanks, can you also tell me about scholarships?"
        # -----------------------------------------------------

        if self._starts_with_gratitude(cleaned):

            if self._contains_scheme_context(cleaned):
                return "scheme_query"

            return "gratitude"

        # -----------------------------------------------------
        # 5. Scheme / government assistance query
        # -----------------------------------------------------

        if self._contains_scheme_context(cleaned):
            return "scheme_query"

        # -----------------------------------------------------
        # 6. Explicitly unrelated topic
        # -----------------------------------------------------

        if self._contains_out_of_scope_context(cleaned):
            return "out_of_scope"

        # -----------------------------------------------------
        # 7. Unknown queries should NOT enter FAISS automatically
        # -----------------------------------------------------

        return "out_of_scope"

    # =========================================================
    # RESPONSE METHOD
    # =========================================================

    def get_response(self, intent: str) -> str | None:
        """
        Return a ready-to-display Markdown response for
        conversational intents.

        scheme_query returns None because it should continue
        to the existing JanSahayak AI pipeline.
        """

        if intent == "greeting":
            return (
                "Hi! 👋 I'm **JanSahayak**.\n\n"
                "I can help you discover government schemes and understand "
                "their **eligibility, benefits, required documents, and "
                "application guidance**.\n\n"
                "Tell me what kind of assistance you're looking for."
            )

        if intent == "gratitude":
            return (
                "You're welcome! 😊\n\n"
                "If you need help finding another government scheme, "
                "checking eligibility, understanding required documents, "
                "or knowing how to apply, feel free to ask."
            )

        if intent == "out_of_scope":
            return (
                "I'm **JanSahayak**, an assistant focused on government "
                "schemes and citizen assistance.\n\n"
                "I can help you with:\n\n"
                "- Government schemes you may be eligible for\n"
                "- Financial assistance and subsidies\n"
                "- Scholarships and education support\n"
                "- Farmer and agriculture assistance\n"
                "- Women and entrepreneurship support\n"
                "- Pension and insurance schemes\n"
                "- Eligibility requirements\n"
                "- Required documents\n"
                "- Application guidance\n\n"
                "Tell me what kind of government assistance you're looking for."
            )

        return None

    # =========================================================
    # INTERNAL HELPERS
    # =========================================================

    def _contains_scheme_context(self, text: str) -> bool:
        """
        Check whether the query contains government assistance
        or scheme-related meaning.
        """

        for keyword in self.SCHEME_KEYWORDS:
            if self._contains_keyword(text, keyword):
                return True

        return False

    def _contains_out_of_scope_context(self, text: str) -> bool:
        """
        Detect common unrelated topics.
        """

        for keyword in self.OUT_OF_SCOPE_KEYWORDS:
            if self._contains_keyword(text, keyword):
                return True

        return False

    def _starts_with_greeting(self, text: str) -> bool:
        """
        Detect greetings at the beginning of a longer message.
        """

        for greeting in self.GREETING_PATTERNS:
            if text == greeting:
                return True

            if text.startswith(greeting + " "):
                return True

        return False

    def _starts_with_gratitude(self, text: str) -> bool:
        """
        Detect gratitude at the beginning of a longer message.
        """

        gratitude_starters = {
            "thanks",
            "thank you",
            "thankyou",
            "thank u",
        }

        for phrase in gratitude_starters:
            if text == phrase:
                return True

            if text.startswith(phrase + " "):
                return True

        return False

    @staticmethod
    def _contains_keyword(text: str, keyword: str) -> bool:
        """
        Match complete words/phrases rather than arbitrary substrings.

        Example:
            keyword='loan'

        matches:
            'I need a loan'

        but avoids accidental matching inside unrelated words.
        """

        pattern = rf"\b{re.escape(keyword)}\b"

        return re.search(pattern, text, flags=re.IGNORECASE) is not None

    @staticmethod
    def _clean_text(text: str) -> str:
        """
        Normalize user text before intent detection.
        """

        text = text.lower().strip()

        # Convert punctuation to spaces.
        text = re.sub(r"[^\w\s-]", " ", text)

        # Normalize repeated spaces.
        text = re.sub(r"\s+", " ", text)

        return text.strip()