from datetime import datetime, timezone

from app.services.source_fetcher import SourceFetcher
from app.services.source_registry import load_sources


class IngestionService:

    def __init__(self):
        self.fetcher = SourceFetcher()

    def fetch_sources(self):

        sources = load_sources()

        results = []

        for source in sources:

            try:

                print(
                    f"\nFetching: {source.name}"
                )

                text = self.fetcher.fetch_text(
                    source.base_url
                )

                results.append({
                    "source_id": source.id,
                    "source_name": source.name,
                    "authority": source.authority,
                    "source_url": source.base_url,
                    "content": text,
                    "retrieved_at": datetime.now(
                        timezone.utc
                    ).isoformat(),
                    "success": True
                })

            except Exception as error:

                print(
                    f"ERROR for {source.name}:"
                )

                print(
                    repr(error)
                )

                results.append({
                    "source_id": source.id,
                    "source_name": source.name,
                    "source_url": source.base_url,
                    "content": "",
                    "error": repr(error),
                    "success": False
                })

        return results