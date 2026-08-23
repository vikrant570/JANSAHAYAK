from abc import ABC, abstractmethod


class BaseConnector(ABC):

    @abstractmethod
    def fetch(self, url: str) -> str:
        """
        Fetch raw content from an official source.
        """
        pass

    @abstractmethod
    def extract(self, content: str) -> list[dict]:
        """
        Convert source content into structured records.
        """
        pass