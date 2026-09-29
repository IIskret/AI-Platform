from functools import lru_cache
from pathlib import Path

from pydantic import PrivateAttr, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class JWTSettings(BaseSettings):

    model_config=SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    jwt_algorithm: str = Field(
        min_length=1
    )

    access_token_expire_minutes: int = Field(
        ge=1
    )
    refresh_token_expire_days: int = Field(
        ge=1
    )

    jwt_iss: str = Field(
        min_length=1
    )
    jwt_aud: str = Field(
        min_length=1
    )

    jwt_private_key_path: Path
    jwt_public_key_path: Path

    _private_key: str | None = PrivateAttr(default=None)
    _public_key: str | None = PrivateAttr(default=None)

    @field_validator("jwt_public_key_path", "jwt_private_key_path")
    @classmethod
    def check_path(cls, path: Path):
        if not path.is_file():
            raise ValueError(f"file is not exists at path: {path}")
        return path

    @property
    def private_key(self) -> str:
        if self._private_key is None:
            self._private_key = self.jwt_private_key_path.read_text(encoding="utf-8")
        return self._private_key

    @property
    def public_key(self) -> str:
        if self._public_key is None:
            self._public_key = self.jwt_public_key_path.read_text(encoding="utf-8")
        return self._public_key


@lru_cache
def get_jwt_settings() -> JWTSettings:
    return JWTSettings()
