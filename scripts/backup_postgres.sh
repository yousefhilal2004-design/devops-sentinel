
#!/usr/bin/env bash
set -Eeuo pipefail

# DevOps Sentinel - PostgreSQL Backup
# Stage 06

DB_CONTAINER="sentinel-postgres-dev"
DB_USER="sentinel"
DB_NAME="sentinel_db"

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKUP_DIR="$PROJECT_DIR/backups/postgres"
LOG_DIR="$PROJECT_DIR/logs"
LOG_FILE="$LOG_DIR/postgres_backup.log"

TIMESTAMP="$(date -u +%Y%m%d_%H%M%S)"
BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_${TIMESTAMP}.dump"
TEMP_FILE="${BACKUP_FILE}.partial"

# 0 means retention cleanup is disabled.
RETENTION_DAYS="${RETENTION_DAYS:-0}"

mkdir -p "$BACKUP_DIR" "$LOG_DIR"
chmod 700 "$BACKUP_DIR"

log() {
    local message="$1"
    printf '[%s] %s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" "$message" \
        | tee -a "$LOG_FILE"
}

cleanup() {
    rm -f -- "$TEMP_FILE"
}

trap cleanup EXIT

log "Starting PostgreSQL backup"

if ! docker inspect "$DB_CONTAINER" \
    --format '{{.State.Running}}' 2>/dev/null | grep -qx true; then
    log "ERROR: PostgreSQL container is not running"
    exit 1
fi

if ! docker exec "$DB_CONTAINER" \
    pg_isready -U "$DB_USER" -d "$DB_NAME" >/dev/null 2>&1; then
    log "ERROR: PostgreSQL is not ready"
    exit 1
fi

log "Database connection verified"

# Write directly to a host file.
# Do not use docker -t: a TTY can corrupt binary dumps.
if ! docker exec "$DB_CONTAINER" \
    pg_dump \
        -U "$DB_USER" \
        -d "$DB_NAME" \
        --format=custom \
        --no-owner \
        --no-acl \
        > "$TEMP_FILE"; then
    log "ERROR: pg_dump failed"
    exit 1
fi

if [[ ! -s "$TEMP_FILE" ]]; then
    log "ERROR: Backup file is empty"
    exit 1
fi

# Validate archive structure using pg_restore.
if ! docker exec -i "$DB_CONTAINER" \
    pg_restore --list < "$TEMP_FILE" >/dev/null; then
    log "ERROR: Backup archive validation failed"
    exit 1
fi

chmod 600 "$TEMP_FILE"
mv -- "$TEMP_FILE" "$BACKUP_FILE"

BACKUP_SIZE="$(du -h "$BACKUP_FILE" | cut -f1)"
log "Backup successful: $BACKUP_FILE"
log "Backup size: $BACKUP_SIZE"

# Optional retention policy.
if [[ "$RETENTION_DAYS" =~ ^[1-9][0-9]*$ ]]; then
    find "$BACKUP_DIR" \
        -maxdepth 1 \
        -type f \
        -name "${DB_NAME}_*.dump" \
        -mtime +"$RETENTION_DAYS" \
        -delete

    log "Retention cleanup completed"
else
    log "Retention cleanup disabled"
fi

log "PostgreSQL backup finished"
