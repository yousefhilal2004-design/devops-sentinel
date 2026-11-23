import time

from fastapi import Request
from prometheus_client import Counter, Gauge, Histogram, make_asgi_app
from starlette.middleware.base import BaseHTTPMiddleware

REQUEST_COUNT = Counter(
    "sentinel_http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status_code"],
)

REQUEST_DURATION = Histogram(
    "sentinel_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
)

REQUEST_IN_PROGRESS = Gauge(
    "sentinel_http_requests_in_progress",
    "HTTP requests currently being processed",
)

metrics_app = make_asgi_app()


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Do not count Prometheus scraping requests.
        if request.url.path.startswith("/metrics"):
            return await call_next(request)

        start = time.perf_counter()
        method = request.method
        REQUEST_IN_PROGRESS.inc()

        status_code = 500

        try:
            response = await call_next(request)
            status_code = response.status_code
            return response

        finally:
            duration = time.perf_counter() - start

            route = request.scope.get("route")
            endpoint = (getattr(route, "path", None) if route is not None else None) or "unmatched"

            REQUEST_COUNT.labels(
                method=method,
                endpoint=endpoint,
                status_code=str(status_code),
            ).inc()

            REQUEST_DURATION.labels(
                method=method,
                endpoint=endpoint,
            ).observe(duration)

            REQUEST_IN_PROGRESS.dec()
