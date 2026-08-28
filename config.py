from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration. All deployable values come from the environment."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore", enable_decoding=False)

    database_url: str = Field(alias="DATABASE_URL")
    jwt_secret: str = Field(min_length=32, alias="JWT_SECRET")
    access_token_expire_minutes: int = Field(default=15, ge=5, le=60 * 24, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(default=14, ge=1, le=90, alias="REFRESH_TOKEN_EXPIRE_DAYS")
    cors_origins: list[str] = Field(default_factory=list, alias="CORS_ORIGINS")
    environment: str = Field(default="development", alias="ENVIRONMENT")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def split_cors_origins(cls, value: str | list[str] | None) -> list[str]:
        if value is None:
            return []
        if isinstance(value, str):
            return [origin.strip().rstrip("/") for origin in value.split(",") if origin.strip()]
        return [origin.rstrip("/") for origin in value]


@lru_cache
def get_settings() -> Settings:
    return Settings()
