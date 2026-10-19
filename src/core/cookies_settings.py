from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from functools import lru_cache

class CookiesSettings(BaseSettings):
    model_config=SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    httponly: bool = Field(
        default=True
    )

    secure: bool = Field(
        default=True
    )

    samesite: str = Field(
        min_length=1
    )

    access_token_expire_minutes: int = Field(
        ge=1
    )

    refresh_token_expire_days: int = Field(
        ge=1
    )

@lru_cache
def get_cookies_settings() -> CookiesSettings:
    return CookiesSettings()
