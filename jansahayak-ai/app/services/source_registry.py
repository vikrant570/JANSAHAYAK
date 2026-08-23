import json
from pathlib import Path

from app.models.source import SourceRecord


BASE_DIR = Path(
    __file__
).resolve().parents[2]

SOURCES_FILE = (
    BASE_DIR / "data" / "sources.json"
)


def load_sources() -> list[SourceRecord]:

    with open(
        SOURCES_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    return [
        SourceRecord(**source)
        for source in data
        if source.get(
            "enabled",
            True
        )
    ]