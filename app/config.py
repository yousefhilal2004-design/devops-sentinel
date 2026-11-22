from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "DevOps Sentinel API"
    app_env: str = "development"

    database_url: str

    allowed_monitor_hosts: str = "example.com"

    monitor_interval_seconds: int = Field(
        default=30,
        ge=5,
        le=3600,
    )

    monitor_timeout_seconds: float = Field(
        default=5.0,
        gt=0,
        le=30,
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def allowed_hosts(self) -> set[str]:
        return {
            host.strip().lower() for host in self.allowed_monitor_hosts.split(",") if host.strip()
        }


@lru_cache
def get_settings() -> Settings:
    return Settings()
