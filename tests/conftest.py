import os
from urllib.parse import urlsplit

import pytest
from fastapi.testclient import TestClient

from app.config import get_settings

LOCAL_TEST_DATABASE_URL = (
    "postgresql://sentinel:sentinel_local_dev_only@127.0.0.1:5433/sentinel_test"
)


@pytest.fixture
def client(monkeypatch):
    # Use the CI database URL when GitHub Actions provides it.
    # Otherwise, use the local disposable test database.
    test_database_url = os.environ.get(
        "DATABASE_URL",
        LOCAL_TEST_DATABASE_URL,
    )

    parsed = urlsplit(test_database_url)

    # Safety: never run destructive tests against the
    # development or production database.
    if (
        parsed.path != "/sentinel_test"
        or parsed.hostname not in ("127.0.0.1", "localhost")
        or parsed.port != 5433
    ):
        raise RuntimeError(
            "Tests must use the local disposable sentinel_test database on port 5433"
        )

    monkeypatch.setenv(
        "DATABASE_URL",
        test_database_url,
    )

    monkeypatch.setenv(
        "ALLOWED_MONITOR_HOSTS",
        "example.com",
    )

    get_settings.cache_clear()

    from app.database import get_connection
    from app.main import app

    try:
        with TestClient(app) as test_client:
            # Clear only the disposable test database.
            with get_connection() as connection:
                connection.execute("TRUNCATE TABLE checks, services RESTART IDENTITY CASCADE")

            yield test_client

    finally:
        get_settings.cache_clear()
