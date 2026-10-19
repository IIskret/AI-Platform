from functools import lru_cache

from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMApiSettings(BaseSettings):
    model_config=SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    mistral_api: SecretStr = Field(
        min_length=1
    )

@lru_cache
def get_llm_settings() -> LLMApiSettings:
    return LLMApiSettings()
