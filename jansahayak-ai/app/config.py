from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "JanSahayak AI"
    app_version: str = "1.0.0"

    llm_provider: str = "mock"
    llm_api_key: str = ""
    llm_model: str = ""

    allowed_origins: str = (
        "http://localhost:3000,http://localhost:8501"
    )

    max_file_size_mb: int = 10

    embedding_model: str = "all-MiniLM-L6-v2"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    @property
    def cors_origins(self):
        return [
            origin.strip()
            for origin in self.allowed_origins.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings():
    return Settings()