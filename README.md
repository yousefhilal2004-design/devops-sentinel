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

## Stage 02 — Monitoring REST API

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