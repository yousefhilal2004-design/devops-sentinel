from datetime import datetime
from urllib.parse import urlsplit

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)


class ServiceCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    url: str = Field(min_length=10, max_length=2048)

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        from app.config import get_settings

        try:
            parsed = urlsplit(value)
            hostname = parsed.hostname
            port = parsed.port
        except ValueError as exc:
            raise ValueError("Invalid URL") from exc

        if parsed.scheme != "https":
            raise ValueError("Only HTTPS URLs are allowed")

        if not hostname:
            raise ValueError("URL must contain a hostname")

        if hostname.lower() not in get_settings().allowed_hosts:
            raise ValueError("Hostname is not on the approved allowlist")

        if parsed.username or parsed.password:
            raise ValueError("Credentials in URLs are not allowed")

        if port not in (None, 443):
            raise ValueError("Only the standard HTTPS port is allowed")

        if parsed.fragment:
            raise ValueError("URL fragments are not allowed")

        return value


class ServiceUpdate(BaseModel):
    enabled: bool


class ServiceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    url: str
    enabled: bool
    created_at: datetime


class CheckResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    service_id: int
    status: str
    status_code: int | None
    response_time_ms: float | None
    error_message: str | None
    checked_at: datetime