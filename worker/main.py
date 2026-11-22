import ipaddress
import json
import logging
import signal
import socket
import time

from datetime import datetime, timezone
from urllib.parse import urlsplit

import httpx

from app.config import get_settings
from app.database import get_connection
from app.models import validate_monitor_url


logger = logging.getLogger("sentinel.worker")

stop_requested = False


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
    )


def log_event(level, event, **fields):
    record = {
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
        "level": level.upper(),
        "event": event,
        **fields,
    }

    message = json.dumps(record, default=str)

    getattr(logger, level.lower())(message)


def resolve_public_addresses(hostname):
    results = socket.getaddrinfo(
        hostname,
        443,
        type=socket.SOCK_STREAM,
    )

    addresses = {
        result[4][0]
        for result in results
    }

    if not addresses:
        raise ValueError(
            "Hostname has no resolved addresses"
        )

    for address in addresses:
        ip = ipaddress.ip_address(address)

        if not ip.is_global:
            raise ValueError(
                "Monitoring target resolves "
                "to a non-public IP address"
            )

    return addresses


def validate_target(url):
    validate_monitor_url(url)

    hostname = urlsplit(url).hostname

    resolve_public_addresses(hostname)

    return url


def get_enabled_services():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, name, url
                FROM services
                WHERE enabled = TRUE
                ORDER BY id
                """
            )

            return cursor.fetchall()


def check_service(service, client):
    start = time.perf_counter()

    status = "down"
    status_code = None
    error_message = None

    try:
        validate_target(service["url"])

        response = client.get(
            service["url"],
            follow_redirects=False,
        )

        status_code = response.status_code

        if 200 <= status_code < 300:
            status = "up"
        else:
            error_message = (
                f"Unexpected HTTP status: {status_code}"
            )

    except (
        httpx.RequestError,
        ValueError,
        OSError,
    ) as exc:
        error_message = (
            f"{type(exc).__name__}: "
            f"{str(exc)[:300]}"
        )

    elapsed_ms = (
        time.perf_counter() - start
    ) * 1000

    return {
        "service_id": service["id"],
        "status": status,
        "status_code": status_code,
        "response_time_ms": round(
            elapsed_ms, 2
        ),
        "error_message": error_message,
    }


def save_check(result):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO checks (
                    service_id,
                    status,
                    status_code,
                    response_time_ms,
                    error_message
                )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    result["service_id"],
                    result["status"],
                    result["status_code"],
                    result["response_time_ms"],
                    result["error_message"],
                ),
            )

            return cursor.fetchone()["id"]


def run_cycle():
    services = get_enabled_services()

    log_event(
        "info",
        "monitoring_cycle_started",
        service_count=len(services),
    )

    settings = get_settings()

    with httpx.Client(
        timeout=settings.monitor_timeout_seconds,
        follow_redirects=False,
        trust_env=False,
        verify=True,
    ) as client:

        for service in services:
            try:
                result = check_service(
                    service,
                    client,
                )

                check_id = save_check(result)

                log_event(
                    "info",
                    "service_checked",
                    check_id=check_id,
                    service_id=service["id"],
                    status=result["status"],
                    status_code=result["status_code"],
                    response_time_ms=result[
                        "response_time_ms"
                    ],
                )

            except Exception:
                logger.exception(
                    "Failed to process service %s",
                    service["id"],
                )

    log_event(
        "info",
        "monitoring_cycle_completed",
        service_count=len(services),
    )


def handle_shutdown(signum, frame):
    global stop_requested

    stop_requested = True

    log_event(
        "info",
        "shutdown_requested",
        signal=signum,
    )


def main():
    configure_logging()

    signal.signal(
        signal.SIGINT,
        handle_shutdown,
    )

    signal.signal(
        signal.SIGTERM,
        handle_shutdown,
    )

    settings = get_settings()

    log_event(
        "info",
        "worker_started",
        interval_seconds=(
            settings.monitor_interval_seconds
        ),
        timeout_seconds=(
            settings.monitor_timeout_seconds
        ),
    )

    while not stop_requested:
        try:
            run_cycle()

        except Exception:
            logger.exception(
                "Monitoring cycle failed"
            )

        for _ in range(
            settings.monitor_interval_seconds
        ):
            if stop_requested:
                break

            time.sleep(1)

    log_event(
        "info",
        "worker_stopped",
    )


if __name__ == "__main__":
    main()