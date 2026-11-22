
#!/usr/bin/env bash
set -Eeuo pipefail

CONTAINER="sentinel-postgres-dev"
DB_USER="sentinel"
DB_NAME="sentinel_db"

echo "================================="
echo "DevOps Sentinel - Database Health"
echo "================================="

echo "[1] Container status"
docker inspect "$CONTAINER" \
  --format 'Running: {{.State.Running}}'

echo "[2] PostgreSQL readiness"
docker exec "$CONTAINER" \
  pg_isready -U "$DB_USER" -d "$DB_NAME"

echo "[3] Database size"
docker exec "$CONTAINER" \
  psql -U "$DB_USER" -d "$DB_NAME" \
  -c "SELECT pg_size_pretty(pg_database_size(current_database())) AS database_size;"

echo "[4] Service and check counts"
docker exec "$CONTAINER" \
  psql -U "$DB_USER" -d "$DB_NAME" \
  -c "SELECT (SELECT COUNT(*) FROM services) AS services, (SELECT COUNT(*) FROM checks) AS checks;"

echo "[5] Database connections"
docker exec "$CONTAINER" \
  psql -U "$DB_USER" -d "$DB_NAME" \
  -c "SELECT COUNT(*) AS connections FROM pg_stat_activity WHERE datname = current_database();"

echo "Database health check completed"
