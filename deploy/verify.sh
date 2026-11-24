
#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")/.."

ENV_FILE="${ENV_FILE:-.env.compose}"

API_PORT="${API_PORT:-8001}"
PROMETHEUS_PORT="${PROMETHEUS_PORT:-9091}"
GRAFANA_PORT="${GRAFANA_PORT:-3001}"

echo "=== Validating Docker Compose ==="
docker compose --env-file "$ENV_FILE" config --quiet

echo
echo "=== Container Status ==="
docker compose --env-file "$ENV_FILE" ps

echo
echo "=== API Health ==="
curl -fsS "http://127.0.0.1:${API_PORT}/health"

echo
echo "=== Application Metrics ==="

METRICS="$(curl -fsS "http://127.0.0.1:${API_PORT}/metrics/")"

grep "sentinel_http_requests_total" <<< "$METRICS"

echo
echo "=== Prometheus Health ==="
curl -fsS "http://127.0.0.1:${PROMETHEUS_PORT}/-/healthy"

echo
echo "=== Grafana Health ==="
curl -fsS "http://127.0.0.1:${GRAFANA_PORT}/api/health"

echo
echo "================================"
echo "All endpoint checks passed!"
echo "================================"

