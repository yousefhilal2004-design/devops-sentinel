import logging
from contextlib import contextmanager

import psycopg
from psycopg.rows import dict_row

from app.config import get_settings


logger = logging.getLogger(__name__)


@contextmanager
def get_connection():
    settings = get_settings()

    with psycopg.connect(
        settings.database_url,
        row_factory=dict_row,
        connect_timeout=5,
    ) as connection:
        yield connection


def init_db():
    logger.info("Initializing database tables")

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS services (
                    id BIGINT GENERATED ALWAYS AS IDENTITY
                        PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    url TEXT NOT NULL UNIQUE,
                    enabled BOOLEAN NOT NULL DEFAULT TRUE,
                    created_at TIMESTAMPTZ NOT NULL
                        DEFAULT NOW()
                )
                """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS checks (
                    id BIGINT GENERATED ALWAYS AS IDENTITY
                        PRIMARY KEY,
                    service_id BIGINT NOT NULL
                        REFERENCES services(id)
                        ON DELETE CASCADE,
                    status VARCHAR(20) NOT NULL
                        CHECK (status IN ('up', 'down')),
                    status_code INTEGER,
                    response_time_ms DOUBLE PRECISION,
                    error_message TEXT,
                    checked_at TIMESTAMPTZ NOT NULL
                        DEFAULT NOW()
                )
                """
            )

            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS
                    idx_checks_service_time
                ON checks(service_id, checked_at DESC)
                """
            )

    logger.info("Database tables initialized")