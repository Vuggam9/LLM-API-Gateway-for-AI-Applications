from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    redis_url: str = "redis://localhost:6379/0"
    cache_ttl_seconds: int = 3600
    log_level: str = "INFO"
    api_keys: str = Field(default="local-dev-key", alias="API_KEYS")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", populate_by_name=True)

    @property
    def api_key_list(self) -> list[str]:
        return [value.strip() for value in self.api_keys.split(",") if value.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
