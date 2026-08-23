from app.services.scheme_normalizer import (
    SchemeNormalizer
)


class SchemePipeline:

    def __init__(
        self,
        connectors
    ):

        self.connectors = connectors

        self.normalizer = (
            SchemeNormalizer()
        )

    def search(
        self,
        query: str
    ) -> list[dict]:

        all_results = []

        for connector in self.connectors:

            try:

                results = connector.search(
                    query
                )

                for result in results:

                    normalized = (
                        self.normalizer.normalize(
                            result
                        )
                    )

                    all_results.append(
                        normalized
                    )

            except Exception as error:

                print(
                    f"Connector error: {error}"
                )

        return self.deduplicate(
            all_results
        )

    @staticmethod
    def deduplicate(
        schemes: list[dict]
    ) -> list[dict]:

        unique = {}

        for scheme in schemes:

            name = (
                scheme.get("name")
                or ""
            )

            key = (
                name
                .strip()
                .lower()
            )

            if not key:
                continue

            if key not in unique:

                unique[key] = scheme

            else:

                existing = unique[key]

                if (
                    scheme.get("confidence", 0)
                    >
                    existing.get("confidence", 0)
                ):

                    unique[key] = scheme

        return list(
            unique.values()
        )