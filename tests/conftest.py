import os

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
    # Prevent accidentally clearing the development database
    if TEST_DATABASE_URL.rsplit("/", 1)[-1] != "sentinel_test":
        raise RuntimeError(
            "Tests must use the disposable sentinel_test database"
        )

    monkeypatch.setenv("DATABASE_URL", TEST_DATABASE_URL)
    monkeypatch.setenv("ALLOWED_MONITOR_HOSTS", "example.com")

    get_settings.cache_clear()

    from app.main import app
    from app.database import get_connection

    with TestClient(app) as test_client:
        # Reset test data before each test
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    TRUNCATE TABLE checks, services
                    RESTART IDENTITY CASCADE
                    """
                )

        yield test_client

    get_settings.cache_clear()