
#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")/.."

ENV_FILE="${ENV_FILE:-.env.compose}"

COMPOSE=(docker compose --env-file "$ENV_FILE")

ACTION="${1:-help}"

case "$ACTION" in

    start)
        echo "Starting DevOps Sentinel..."
        "${COMPOSE[@]}" up -d
        ;;

    stop)
        echo "Stopping DevOps Sentinel..."
        "${COMPOSE[@]}" stop
        ;;

    restart)
        echo "Restarting DevOps Sentinel..."
        "${COMPOSE[@]}" restart
        ;;

    status)
        "${COMPOSE[@]}" ps
        ;;

    logs)
        "${COMPOSE[@]}" logs --tail=100 "${@:2}"
        ;;

    follow)
        "${COMPOSE[@]}" logs -f "${@:2}"
        ;;

    build)
        "${COMPOSE[@]}" build
        ;;

    verify)
        ./deploy/verify.sh
        ;;

    backup)
        ./deploy/backup-db.sh
        ;;

    help)
        echo "DevOps Sentinel Deployment Manager"
        echo
        echo "Usage: $0 COMMAND"
        echo
        echo "start    Start containers"
        echo "stop     Stop containers"
        echo "restart  Restart containers"
        echo "status   Show container status"
        echo "logs     Show recent logs"
        echo "follow   Follow container logs"
        echo "build    Build application image"
        echo "verify   Verify application endpoints"
        echo "backup   Back up PostgreSQL"
        echo "help     Show available commands"
        ;;

    *)
        echo "ERROR: Unknown command: $ACTION"
        exit 1
        ;;

esac

