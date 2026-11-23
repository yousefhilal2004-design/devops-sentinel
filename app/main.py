import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query
from psycopg import errors

from app.database import get_connection, init_db
from app.metrics import MetricsMiddleware, metrics_app
from app.models import (
    CheckResponse,
    ServiceCreate,
    ServiceResponse,
    ServiceUpdate,
)

# ==========================================
# LOGGING CONFIGURATION
# ==========================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

logger = logging.getLogger(__name__)


# ==========================================
# APPLICATION LIFESPAN
# ==========================================


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    logger.info("DevOps Sentinel API started")

    yield

    logger.info("DevOps Sentinel API stopped")


# ==========================================
# FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="DevOps Sentinel API",
    description="Containerized service monitoring platform",
    version="0.4.0",
    lifespan=lifespan,
)

# ==========================================
# STAGE 09 - PROMETHEUS METRICS
# ==========================================

app.add_middleware(MetricsMiddleware)
app.mount("/metrics", metrics_app)


# ==========================================
# ROOT ENDPOINT
# ==========================================


@app.get("/")
def root():
    return {
        "application": "DevOps Sentinel",
        "version": "0.4.0",
        "documentation": "/docs",
        "metrics": "/metrics",
    }


# ==========================================
# HEALTH CHECK
# ==========================================


@app.get("/health")
def health():
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()

        return {
            "status": "healthy",
            "database": "connected",
        }

    except Exception:
        logger.exception("Database health check failed")
        raise HTTPException(
            status_code=503,
            detail="Database unavailable",
        ) from None


# ==========================================
# CREATE MONITORING SERVICE
# ==========================================


@app.post(
    "/services",
    response_model=ServiceResponse,
    status_code=201,
)
def create_service(service: ServiceCreate):
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO services (name, url)
                    VALUES (%s, %s)
                    RETURNING *
                    """,
                    (service.name, service.url),
                )

                created = cursor.fetchone()

        logger.info("Registered monitoring service")
        return created

    except errors.UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="Service URL already registered",
        ) from None


# ==========================================
# LIST ALL MONITORING SERVICES
# ==========================================


@app.get(
    "/services",
    response_model=list[ServiceResponse],
)
def list_services():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT *
                FROM services
                ORDER BY id
                """
            )

            return cursor.fetchall()


# ==========================================
# GET SERVICE BY ID
# ==========================================


@app.get(
    "/services/{service_id}",
    response_model=ServiceResponse,
)
def get_service(service_id: int):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT *
                FROM services
                WHERE id = %s
                """,
                (service_id,),
            )

            service = cursor.fetchone()

    if service is None:
        raise HTTPException(
            status_code=404,
            detail="Service not found",
        )

    return service


# ==========================================
# UPDATE MONITORING SERVICE
# ==========================================


@app.patch(
    "/services/{service_id}",
    response_model=ServiceResponse,
)
def update_service(
    service_id: int,
    update: ServiceUpdate,
):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE services
                SET enabled = %s
                WHERE id = %s
                RETURNING *
                """,
                (update.enabled, service_id),
            )

            service = cursor.fetchone()

    if service is None:
        raise HTTPException(
            status_code=404,
            detail="Service not found",
        )

    return service


# ==========================================
# DELETE MONITORING SERVICE
# ==========================================


@app.delete(
    "/services/{service_id}",
    status_code=204,
)
def delete_service(service_id: int):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM services
                WHERE id = %s
                RETURNING id
                """,
                (service_id,),
            )

            deleted = cursor.fetchone()

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Service not found",
        )


# ==========================================
# LIST RECENT MONITORING CHECKS
# ==========================================


@app.get(
    "/checks",
    response_model=list[CheckResponse],
)
def list_checks(
    limit: int = Query(default=50, ge=1, le=200),
):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT *
                FROM checks
                ORDER BY checked_at DESC, id DESC
                LIMIT %s
                """,
                (limit,),
            )

            return cursor.fetchall()


# ==========================================
# GET CHECKS FOR A SPECIFIC SERVICE
# ==========================================


@app.get(
    "/services/{service_id}/checks",
    response_model=list[CheckResponse],
)
def service_checks(
    service_id: int,
    limit: int = Query(default=50, ge=1, le=200),
):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id
                FROM services
                WHERE id = %s
                """,
                (service_id,),
            )

            if cursor.fetchone() is None:
                raise HTTPException(
                    status_code=404,
                    detail="Service not found",
                )

            cursor.execute(
                """
                SELECT *
                FROM checks
                WHERE service_id = %s
                ORDER BY checked_at DESC, id DESC
                LIMIT %s
                """,
                (service_id, limit),
            )

            return cursor.fetchall()
