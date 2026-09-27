from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

SSLMode = Literal[
    'disable',
    'allow',
    'prefer',
    'require',
    'verify-ca',
    'verify-full'
]

class DBSettings(BaseSettings):

    model_config=SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    db_user: str = Field(
        min_length=1
    )
    db_password: SecretStr = Field(
        min_length=1
    )
    db_host: str = Field(
        min_length=1
    )
    db_port: int = Field(
        ge=1,
        le=65535,
        default=5432
    )
    db_name: str = Field(
        min_length=1
    )

    ssl_mode: SSLMode = 'require'


    pool_size: int = Field(
        default=10,
        ge=1,
        le=100
    )
    max_overflow: int = Field(
        default=10,
        ge=0
    )
    pool_timeout: int = Field(
        default=30,
        ge=1
    )

    @property
    def dsn_asyncpg(self):
        pwd = self.db_password.get_secret_value()
        return f"postgresql+asyncpg://{self.db_user}:{pwd}@{self.db_host}:{self.db_port}/{self.db_name}"

@lru_cache
def get_db_settings() -> DBSettings:
    return DBSettings()
