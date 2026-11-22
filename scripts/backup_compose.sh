
#!/usr/bin/env bash
set -Eeuo pipefail

# DevOps Sentinel - Docker Compose PostgreSQL Backup
# Stage 07

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKUP_DIR="$PROJECT_DIR/backups/postgres"
LOG_DIR="$PROJECT_DIR/logs"
LOG_FILE="$LOG_DIR/compose_backup.log"

TIMESTAMP="$(date -u +%Y%m%d_%H%M%S)"
BACKUP_FILE="$BACKUP_DIR/sentinel_compose_${TIMESTAMP}.dump"
TEMP_FILE="${BACKUP_FILE}.partial"

mkdir -p "$BACKUP_DIR" "$LOG_DIR"
chmod 700 "$BACKUP_DIR"

cd "$PROJECT_DIR"

compose() {
    docker compose --env-file .env.compose "$@"
}

log() {
    printf '[%s] %s\n' \
        "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" \
        "$1" | tee -a "$LOG_FILE"
}

cleanup() {
    rm -f -- "$TEMP_FILE"
}

trap cleanup EXIT

log "Starting Compose database backup"

if ! compose exec -T db \
    sh -c 'pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB"' \
    >/dev/null 2>&1; then
    log "ERROR: Database is not ready"
    exit 1
fi

log "Database connection successful"

if ! compose exec -T db \
    sh -c 'exec pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" --format=custom --no-owner --no-acl' \
    > "$TEMP_FILE"; then
    log "ERROR: Backup failed"
    exit 1
fi

if [[ ! -s "$TEMP_FILE" ]]; then
    log "ERROR: Backup file is empty"
    exit 1
fi

if ! compose exec -T db pg_restore --list \
    < "$TEMP_FILE" > /dev/null; then
    log "ERROR: Backup validation failed"
    exit 1
fi

chmod 600 "$TEMP_FILE"
mv -- "$TEMP_FILE" "$BACKUP_FILE"

log "Backup successful: $BACKUP_FILE"
log "Backup size: $(du -h "$BACKUP_FILE" | cut -f1)"
log "Compose backup completed"
