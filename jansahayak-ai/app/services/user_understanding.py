from app.services.profile_extractor import ProfileExtractor
from app.services.query_understanding import QueryUnderstanding


class UserUnderstanding:

    def __init__(self):

        self.profile_extractor = (
            ProfileExtractor()
        )

        self.query_understanding = (
            QueryUnderstanding()
        )

    def understand(
        self,
        text: str
    ) -> dict:

        profile = (
            self.profile_extractor.extract(
                text
            )
        )

        query = (
            self.query_understanding.understand(
                text
            )
        )

        return {
            "profile": profile,
            "query": query
        }