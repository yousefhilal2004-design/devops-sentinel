from datetime import datetime
from urllib.parse import urlsplit

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)

from app.config import get_settings


def validate_monitor_url(value: str) -> str:
    try:
        parsed = urlsplit(value)
        hostname = parsed.hostname
        port = parsed.port
    except ValueError as exc:
        raise ValueError("Invalid monitoring URL") from exc

    if parsed.scheme != "https":
        raise ValueError("Only HTTPS URLs are supported")

    if not hostname:
        raise ValueError("Hostname is required")

    if hostname.lower() not in get_settings().allowed_hosts:
        raise ValueError("Hostname is not approved")

    if parsed.username or parsed.password:
        raise ValueError("URL credentials are not allowed")

    if port not in (None, 443):
        raise ValueError("Only HTTPS port 443 is supported")

    if parsed.fragment:
        raise ValueError("URL fragments are not supported")

    return value


class ServiceCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    url: str = Field(min_length=10, max_length=2048)

    @field_validator("url")
    @classmethod
    def check_url(cls, value: str) -> str:
        return validate_monitor_url(value)


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