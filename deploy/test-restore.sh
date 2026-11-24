
#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")/.."

ENV_FILE="${ENV_FILE:-.env.compose}"

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 BACKUP_FILE"
    exit 1
fi

BACKUP_FILE="$1"

if [[ ! -s "$BACKUP_FILE" ]]; then
    echo "ERROR: Backup file is missing or empty."
    exit 1
fi

DB_USER="$(
    docker compose --env-file "$ENV_FILE" \
        exec -T db printenv POSTGRES_USER
)"

RESTORE_DB="sentinel_restore_$(date +%s)_$$"

CREATED=0

cleanup() {
    if [[ "$CREATED" == "1" ]]; then
        docker compose --env-file "$ENV_FILE" \
            exec -T db dropdb \
            -U "$DB_USER" "$RESTORE_DB" || true
    fi
}

trap cleanup EXIT

echo "=== Database Recovery Test ==="

echo "Creating temporary database: $RESTORE_DB"

docker compose --env-file "$ENV_FILE" exec -T db \
    createdb -U "$DB_USER" "$RESTORE_DB"

CREATED=1

echo "Restoring backup..."

docker compose --env-file "$ENV_FILE" exec -T db \
    pg_restore \
    --exit-on-error \
    --no-owner \
    --no-privileges \
    -U "$DB_USER" \
    -d "$RESTORE_DB" < "$BACKUP_FILE"

echo
echo "=== Restored Tables ==="

docker compose --env-file "$ENV_FILE" exec -T db \
    psql \
    -v ON_ERROR_STOP=1 \
    -U "$DB_USER" \
    -d "$RESTORE_DB" \
    -c '\dt'

echo
echo "Recovery test completed successfully."
echo "The temporary database will now be removed."
echo "The original database was not modified."

