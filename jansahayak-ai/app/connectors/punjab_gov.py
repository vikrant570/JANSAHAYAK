from app.connectors.base import BaseConnector


class PunjabGovConnector(BaseConnector):

    def fetch(
        self,
        url: str
    ) -> str:

        # TODO:
        #
        # Punjab Government's current TLS
        # configuration is incompatible
        # with the default OpenSSL 3
        # security settings.
        #
        # Implement a dedicated secure
        # connector after testing the
        # official source/API/PDF endpoints.

        raise RuntimeError(
            "Punjab Government connector "
            "requires source-specific "
            "TLS handling."
        )

    def extract(
        self,
        content: str
    ) -> list[dict]:

        return []