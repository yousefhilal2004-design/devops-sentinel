
#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")/.."

ENV_FILE="${ENV_FILE:-.env.compose}"

COMPOSE=(docker compose --env-file "$ENV_FILE")

echo "=== DevOps Sentinel Deployment Update ==="

if [[ -n "$(git status --porcelain)" ]]; then
    echo "ERROR: Working directory contains local changes."
    echo "Commit or resolve them before updating."
    exit 1
fi

echo
echo "=== Current Version ==="
git rev-parse --short HEAD

echo
echo "=== Creating Database Backup ==="
./deploy/backup-db.sh

echo
echo "=== Downloading Latest Changes ==="
git pull --ff-only

echo
echo "=== Validating Configuration ==="
"${COMPOSE[@]}" config --quiet

echo
echo "=== Building Application ==="
"${COMPOSE[@]}" build

echo
echo "=== Updating Containers ==="
"${COMPOSE[@]}" up -d --wait --wait-timeout 120

echo
echo "=== Verifying Deployment ==="
./deploy/verify.sh

echo
echo "=== Deployed Version ==="
git rev-parse --short HEAD

echo
echo "Deployment update completed successfully."

