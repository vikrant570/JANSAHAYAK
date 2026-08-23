from app.connectors.myscheme import MySchemeConnector
from app.services.scheme_normalizer import SchemeNormalizer


class SchemeSearchService:

    def __init__(self):

        self.connector = MySchemeConnector()
        self.normalizer = SchemeNormalizer()

    def search(
        self,
        query: str,
        page_size: int = 10
    ) -> list[dict]:

        raw_results = self.connector.search(
            query=query,
            page_size=page_size
        )

        results = []

        for raw in raw_results:

            normalized = self.normalizer.normalize(
                raw
            )

            results.append(
                normalized
            )

        return results