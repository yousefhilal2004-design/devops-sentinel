# DevOps Sentinel

A containerized monitoring and automation platform built
with Python, Docker, Docker Compose, PostgreSQL, and Prometheus.

## Project Goals

- Monitor configured HTTP services
- Record response times and availability
- Store monitoring history in PostgreSQL
- Expose monitoring results through a REST API
- Collect application metrics using Prometheus
- Apply Docker security best practices
- Support reproducible deployment and recovery

## Technology Stack

- Python
- FastAPI
- PostgreSQL
- Docker
- Docker Compose
- Prometheus
- Git and GitHub

## Project Status

In development.

## Architecture

See docs/ for architecture and technical documentation.

## Setup

Setup instructions will be added as the project develops.

------------------------------------------------------------------

## Monitoring REST API

Implemented a Python REST API using FastAPI and PostgreSQL.

### Features

- Register approved HTTP monitoring targets
- List and retrieve registered services
- Enable or disable monitoring
- Delete services
- Retrieve monitoring history
- Check application and database health
- Validate API requests using Pydantic
- Test API functionality using Pytest

### Run Locally

1. Start the PostgreSQL development container.
2. Activate the Python virtual environment.
3. Install dependencies:

   ```bash
   python -m pip install -r requirements-dev.txt

   --------------------------------------------------------------------


   ## Automated Monitoring Worker

DevOps Sentinel includes a Python monitoring worker that
runs independently from the FastAPI application.

### Features

- Periodic HTTPS health checks
- HTTP status monitoring
- Response-time measurement
- Timeout and connection-error handling
- PostgreSQL monitoring history
- Structured JSON logs
- Configurable monitoring intervals
- Graceful shutdown
- Disabled-service filtering
- Automated unit and integration tests

### Running the Worker

Start PostgreSQL and configure `.env`.

```bash
python -m worker.main

----------------------------------------------------------------------

## Docker Containerization

DevOps Sentinel uses a multi-stage Dockerfile to build
a reusable Python runtime image.

### Features

- Multi-stage Docker build
- Python virtual environment
- Non-root runtime user
- Separate API and monitoring worker containers
- Docker bridge networking
- Environment-based configuration
- API container health checks
- Persistent PostgreSQL storage
- Container logs and troubleshooting

### Build

```bash
docker build -t devops-sentinel:stage04 .

-----------------------------------------------------------------------

## Docker Networking

DevOps Sentinel uses two user-defined Docker bridge networks.

### Network Architecture

- `sentinel-frontend`: API container
- `sentinel-backend`: API, worker, and PostgreSQL containers

The API is attached to both networks.
The worker and PostgreSQL are attached only to the backend network.

### Features

- User-defined Docker bridge networks
- Container-name DNS resolution
- Internal container-to-container communication
- Host port publishing for FastAPI
- Separation of application and database network traffic
- Docker networking troubleshooting

### Verification

```bash
docker network ls
docker network inspect sentinel-frontend
docker network inspect sentinel-backend
docker port sentinel-api
curl http://127.0.0.1:8000/health
```

### Security Notes

Network separation reduces unnecessary direct connectivity,
but it does not replace authentication or firewall controls.

The backend network is not marked `internal` because the
monitoring worker requires outbound HTTPS access.

PostgreSQL's development host port remains published until
the database container is recreated with different settings.


-----------------------------------------------------------------------

## PostgreSQL Persistence, Backups & Recovery

In this stage, I improved the database reliability of DevOps Sentinel.

### What I implemented

- Inspected PostgreSQL storage and Docker volume mounts
- Verified database persistence after container restart
- Created a Bash script for PostgreSQL backups
- Used `pg_dump` to create custom-format backup archives
- Added backup validation and logging
- Generated SHA-256 checksums
- Restored a backup into a separate test database
- Verified restored tables and monitoring records
- Inspected PostgreSQL indexes and query execution plans
- Created a database health-check script
- Configured a daily cron backup job

### Backup

Run:

```bash
./scripts/backup_postgres.sh
```

Backups are saved in `backups/postgres/`.

### Database health

Run:

```bash
./scripts/check_postgres.sh
```

### Recovery

A backup can be restored into a separate empty database using:

```bash
docker exec -i sentinel-postgres-dev \
  pg_restore \
  -U sentinel \
  -d sentinel_restore_test \
  --no-owner \
  --no-acl \
  --exit-on-error \
  < backups/postgres/BACKUP_FILE.dump
```

Replace `BACKUP_FILE.dump` with the actual filename.

### Security

Database credentials, backups, and runtime logs are excluded from Git.

Backups should be stored securely and tested regularly.

### Skills Practiced

PostgreSQL, Docker persistence, Bash scripting, backup automation,
database recovery, SQL queries, indexes, monitoring, and cron.


-----------------------------------------------------------------------


## Docker Compose

DevOps Sentinel now uses Docker Compose to manage its
multi-container application.

### Services

- **api** — FastAPI REST API
- **worker** — Automated HTTP monitoring
- **db** — PostgreSQL 17 database

### Networking

Two user-defined Docker bridge networks:

- `frontend`: API
- `backend`: API, worker, PostgreSQL

PostgreSQL is not published to the host.

### Persistence

PostgreSQL uses a named Docker volume:

`devops-sentinel_postgres_data`

### Start the Application

1. Copy `.env.compose.example` to `.env.compose`.
2. Configure the local development credentials.
3. Build and start:

```bash
docker compose --env-file .env.compose up -d --build
```

### Check Services

```bash
docker compose --env-file .env.compose ps
docker compose --env-file .env.compose logs -f
```

### Stop Services

```bash
docker compose --env-file .env.compose stop
```

### Start Existing Services

```bash
docker compose --env-file .env.compose start
```

### Remove Compose Containers

```bash
docker compose --env-file .env.compose down
```

This command preserves the named PostgreSQL volume
unless volume removal is explicitly requested.

### PostgreSQL Backup

```bash
./scripts/backup_compose.sh
```

Backups are saved in `backups/postgres/`.

### Health Check

```bash
curl http://127.0.0.1:8000/health
```

### Security Notes

- The API binds to localhost.
- PostgreSQL is not published to the host.
- Database credentials are excluded from Git.
- Backup files are excluded from Git.
- Containers use a non-root application user.
- Docker Compose manages service startup dependencies.

This is a local development configuration,
not a production deployment.
