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