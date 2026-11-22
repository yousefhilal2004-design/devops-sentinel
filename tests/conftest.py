import os
from urllib.parse import urlsplit

import pytest
from fastapi.testclient import TestClient

from app.config import get_settings


TEST_DATABASE_URL = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql://sentinel:sentinel_local_dev_only"
    "@127.0.0.1:5433/sentinel_test",
)


@pytest.fixture
def client(monkeypatch):
    parsed = urlsplit(TEST_DATABASE_URL)

    if (
        parsed.path != "/sentinel_test"
        or parsed.hostname not in ("127.0.0.1", "localhost")
        or parsed.port != 5433
    ):
        raise RuntimeError(
            "Tests must use the local disposable "
            "sentinel_test database on port 5433"
        )

    monkeypatch.setenv(
        "DATABASE_URL",
        TEST_DATABASE_URL,
    )

    monkeypatch.setenv(
        "ALLOWED_MONITOR_HOSTS",
        "example.com",
    )

    get_settings.cache_clear()

    from app.main import app
    from app.database import get_connection

    try:
        with TestClient(app) as test_client:
            with get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        TRUNCATE TABLE checks, services
                        RESTART IDENTITY CASCADE
                        """
                    )

            yield test_client
    finally:
        get_settings.cache_clear()