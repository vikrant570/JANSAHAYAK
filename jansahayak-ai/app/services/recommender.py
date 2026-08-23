from app.services.scheme_search import SchemeSearchService
from app.services.scheme_filter import SchemeFilter
from app.services.eligibility import EligibilityService


class SchemeRecommender:

    def __init__(self):

        self.search_service = (
            SchemeSearchService()
        )

        self.filter_service = (
            SchemeFilter()
        )

        self.eligibility_service = (
            EligibilityService()
        )

    def recommend(
        self,
        query: str,
        profile: dict,
        limit: int = 5
    ) -> list[dict]:

        schemes = self.search_service.search(
            query=query,
            page_size=10
        )

        schemes = (
            self.filter_service
            .filter_verified(schemes)
        )

        schemes = (
            self.filter_service
            .filter_by_state(
                schemes,
                profile.get("state")
            )
        )

        recommendations = []

        for scheme in schemes:

            eligibility = (
                self.eligibility_service.check(
                    scheme,
                    profile
                )
            )

            if eligibility["eligible"]:

                scheme = scheme.copy()

                scheme["eligibility_result"] = (
                    eligibility
                )

                recommendations.append(
                    scheme
                )

        return recommendations[:limit]