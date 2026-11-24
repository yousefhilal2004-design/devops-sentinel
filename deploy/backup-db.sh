
#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")/.."

ENV_FILE="${ENV_FILE:-.env.compose}"
BACKUP_DIR="${BACKUP_DIR:-$HOME/sentinel-backups}"

umask 077

echo "=== DevOps Sentinel Database Backup ==="

if [[ ! -f "$ENV_FILE" ]]; then
    echo "ERROR: Environment file not found."
    exit 1
fi

mkdir -p "$BACKUP_DIR"
chmod 700 "$BACKUP_DIR"

DB_USER="$(
    docker compose --env-file "$ENV_FILE" \
        exec -T db printenv POSTGRES_USER
)"

DB_NAME="$(
    docker compose --env-file "$ENV_FILE" \
        exec -T db printenv POSTGRES_DB
)"

if [[ -z "$DB_USER" || -z "$DB_NAME" ]]; then
    echo "ERROR: Database configuration is missing."
    exit 1
fi

TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"

BACKUP_FILE="$BACKUP_DIR/sentinel-${TIMESTAMP}.dump"

TEMP_FILE="$(mktemp "$BACKUP_DIR/.backup-XXXXXX")"

trap 'rm -f "$TEMP_FILE"' EXIT

echo "Database: $DB_NAME"
echo "Creating backup..."

docker compose --env-file "$ENV_FILE" exec -T db \
    pg_dump \
    -U "$DB_USER" \
    -d "$DB_NAME" \
    -Fc > "$TEMP_FILE"

if [[ ! -s "$TEMP_FILE" ]]; then
    echo "ERROR: Backup file is empty."
    exit 1
fi

docker compose --env-file "$ENV_FILE" exec -T db \
    pg_restore --list < "$TEMP_FILE" > /dev/null

mv "$TEMP_FILE" "$BACKUP_FILE"

echo
echo "Backup completed successfully."
echo "Backup location: $BACKUP_FILE"

ls -lh "$BACKUP_FILE"

