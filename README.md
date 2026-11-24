
# 🛡️ DevOps Sentinel

### Service Monitoring Platform — From Development to Deployment

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Bash](https://img.shields.io/badge/Bash-4EAA25?style=for-the-badge&logo=gnubash&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)

---

## 📖 Project Overview

DevOps Sentinel is a containerized service-monitoring platform
developed as an independent, hands-on DevOps engineering project.

The application allows users to register services, monitor their
availability, store monitoring results, and observe application
performance through monitoring dashboards.

The main purpose of this project is to demonstrate how different
DevOps technologies and practices can work together throughout
the software development lifecycle.

The project covers application development, database integration,
Linux administration, automation, containerization, automated
testing, continuous integration, security scanning, monitoring,
deployment, and database recovery.

Rather than focusing on individual tools separately, DevOps Sentinel
combines these technologies into a single practical system.

---

## 📑 Table of Contents

- [Project Objectives](#-project-objectives)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [System Architecture](#-system-architecture)
- [Project Development Roadmap](#-project-development-roadmap)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [API Documentation](#-api-documentation)
- [Database](#-database)
- [Background Worker](#-background-worker)
- [Docker and Containerization](#-docker-and-containerization)
- [Testing and Code Quality](#-testing-and-code-quality)
- [CI/CD Pipeline](#-cicd-pipeline)
- [Security](#-security)
- [Monitoring and Observability](#-monitoring-and-observability)
- [Linux Deployment](#-linux-deployment)
- [Database Backup and Recovery](#-database-backup-and-recovery)
- [Deployment Operations](#-deployment-operations)
- [Troubleshooting](#-troubleshooting)
- [Project Documentation](#-project-documentation)
- [Skills Demonstrated](#-skills-demonstrated)
- [Future Improvements](#-future-improvements)
- [Author](#-author)

---

## 🎯 Project Objectives

The main objectives of DevOps Sentinel are:

- Build a functional REST API using Python and FastAPI.
- Integrate PostgreSQL for persistent data storage.
- Implement background service-monitoring tasks.
- Apply Linux and Bash automation skills.
- Manage application configuration through environment variables.
- Containerize application components using Docker.
- Orchestrate multiple services using Docker Compose.
- Implement automated testing and code quality checks.
- Build continuous integration workflows using GitHub Actions.
- Identify security vulnerabilities in dependencies and images.
- Collect application metrics using Prometheus.
- Visualize application performance using Grafana.
- Deploy and manage the application in a Linux environment.
- Implement database backup and recovery procedures.
- Document the complete development and deployment lifecycle.

---

## ✨ Key Features

### Application Features

- RESTful API using FastAPI.
- Service registration and management.
- Create, read, update, and delete operations.
- Background service availability monitoring.
- Monitoring check history.
- PostgreSQL database integration.
- Interactive Swagger API documentation.
- Application health endpoints.
- Environment-based configuration.

### DevOps Features

- Linux-based development environment.
- Bash automation scripts.
- Docker multi-stage builds.
- Non-root application containers.
- Docker Compose orchestration.
- Container health checks.
- Service dependency management.
- Internal Docker networking.
- Persistent Docker volumes.
- Automated continuous integration.
- Automated testing and linting.
- Dependency vulnerability auditing.
- Trivy container vulnerability scanning.

### Monitoring Features

- Prometheus metrics collection.
- Grafana dashboard visualization.
- HTTP request monitoring.
- HTTP status code monitoring.
- Request duration measurement.
- Active request tracking.
- Prometheus target monitoring.

### Deployment and Operations

- Local Linux deployment using WSL2.
- Private service port bindings.
- Deployment verification scripts.
- Database backup automation.
- Database recovery testing.
- Scheduled backups using cron.
- Application management scripts.
- Manual deployment update workflow.

---

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Operating System | Ubuntu Linux, WSL2 |
| Programming | Python, Bash |
| Backend Framework | FastAPI |
| API Documentation | Swagger UI, OpenAPI |
| Database | PostgreSQL 17 |
| Background Processing | Python Worker |
| Version Control | Git |
| Repository Hosting | GitHub |
| Containerization | Docker |
| Container Orchestration | Docker Compose |
| Continuous Integration | GitHub Actions |
| Automated Testing | pytest |
| Code Quality | Ruff |
| Dependency Security | pip-audit |
| Container Security | Trivy |
| Metrics Collection | Prometheus |
| Visualization | Grafana |
| Task Scheduling | Cron |
| Database Backup | pg_dump |
| Database Recovery | pg_restore |

---

## 🏗️ System Architecture

DevOps Sentinel consists of five main application services:

1. FastAPI application.
2. PostgreSQL database.
3. Background monitoring worker.
4. Prometheus monitoring server.
5. Grafana visualization server.

### Application Architecture

```mermaid
flowchart TD
    Client[User / API Client]
    API[FastAPI Application]
    DB[(PostgreSQL Database)]
    Worker[Background Monitoring Worker]
    Services[Registered External Services]
    Prometheus[Prometheus]
    Grafana[Grafana Dashboard]
    Backup[Database Backup Files]

    Client -->|HTTP Requests| API
    API -->|Read and Write| DB
    Worker -->|Read Services| DB
    Worker -->|Availability Checks| Services
    Worker -->|Store Check Results| DB
    Prometheus -->|Scrape Metrics| API
    Grafana -->|PromQL Queries| Prometheus
    DB -->|pg_dump| Backup
```

### Development and Delivery Workflow

```mermaid
flowchart LR
    Developer[Developer]
    Git[Git Repository]
    GitHub[GitHub]
    CI[GitHub Actions]
    Quality[Code Quality]
    Tests[Automated Tests]
    Audit[Dependency Audit]
    Build[Docker Build]
    Scan[Trivy Scan]
    Image[Validated Image]
    Deploy[Manual Linux Deployment]
    Monitor[Prometheus and Grafana]

    Developer --> Git
    Git --> GitHub
    GitHub --> CI
    CI --> Quality
    CI --> Tests
    CI --> Audit
    CI --> Build
    Build --> Scan
    Scan --> Image
    Image -.-> Deploy
    Deploy --> Monitor
```

The continuous integration pipeline validates the application.
Deployment is currently performed manually using Docker Compose
and deployment scripts.

---

## 📚 Project Development Roadmap

The project was developed progressively, starting with application
foundations and ending with monitoring and Linux deployment.

The following table summarizes the major development phases.

| Phase | Focus | Main Technologies |
|---|---|---|
| Foundation | Project setup and Linux environment | Linux, Git, Python |
| Backend Development | REST API and application structure | FastAPI, Python |
| Database Integration | Persistent data storage | PostgreSQL |
| Monitoring Logic | Background service checks | Python Worker |
| Configuration and Automation | Environment variables and scripts | Bash, Python |
| Testing and Quality | Automated tests and code quality | pytest, Ruff |
| Stage 07 | Containerization and service orchestration | Docker, Docker Compose |
| Stage 08 | Continuous integration and security | GitHub Actions, Trivy, pip-audit |
| Stage 09 | Monitoring and observability | Prometheus, Grafana |
| Stage 10 | Linux deployment and operations | Linux, Bash, Cron, PostgreSQL |
| Stage 11 | Kubernetes fundamentals | Planned |
| Stage 12 | Kubernetes deployment | Planned |

### Application Foundations

The initial development phases focused on building the application
and preparing the development environment.

Main activities included:

- Preparing the Linux development environment.
- Creating the Git repository.
- Configuring Python virtual environments.
- Organizing application directories.
- Developing REST API endpoints.
- Connecting the application to PostgreSQL.
- Implementing background monitoring tasks.
- Managing configuration and dependencies.
- Implementing automated tests.

### Stage 07 — Docker and Docker Compose

The application was containerized to provide a consistent and
reproducible runtime environment.

Main activities included:

- Creating a Dockerfile.
- Implementing multi-stage Docker builds.
- Running the application as a non-root user.
- Configuring Docker Compose.
- Connecting the API, worker, and database.
- Configuring Docker networks.
- Implementing persistent database storage.
- Configuring container health checks.
- Managing service dependencies.

### Stage 08 — CI/CD and Security

Continuous integration was introduced to automate application
validation and improve software quality.

Main activities included:

- Configuring GitHub Actions.
- Running Ruff linting and formatting checks.
- Executing automated pytest tests.
- Preparing an isolated test database.
- Auditing Python dependencies.
- Building Docker images automatically.
- Scanning container images using Trivy.
- Resolving dependency vulnerabilities.
- Preventing failed validation from being treated as successful.

### Stage 09 — Monitoring and Observability

Application monitoring was implemented using Prometheus and Grafana.

Main activities included:

- Integrating the Prometheus Python client.
- Implementing FastAPI metrics middleware.
- Creating request counters.
- Measuring request duration.
- Tracking active requests.
- Configuring Prometheus scrape targets.
- Provisioning Grafana data sources.
- Creating monitoring dashboards.
- Generating application traffic.
- Verifying monitoring targets.

### Stage 10 — Linux Deployment and Operations

The application was deployed in a local Ubuntu Linux environment
using WSL2 and Docker Compose.

Main activities included:

- Preparing the deployment environment.
- Configuring private environment files.
- Binding application ports to localhost.
- Resolving host port conflicts.
- Deploying all five application services.
- Creating deployment verification scripts.
- Implementing PostgreSQL backup procedures.
- Implementing database recovery testing.
- Preparing scheduled backups using cron.
- Creating deployment management scripts.
- Preparing manual deployment updates.
- Completing project documentation.

### Future Stages

Kubernetes fundamentals and Kubernetes deployment are planned
as future extensions after completing dedicated Kubernetes learning.

---

## 📂 Project Structure

```text
devops-sentinel/
│
├── .github/
│   └── workflows/
│       └── CI workflow configurations
│
├── app/
│   ├── main.py
│   ├── metrics.py
│   └── Application modules
│
├── worker/
│   ├── main.py
│   └── Background monitoring modules
│
├── database/
│   └── Database-related files
│
├── tests/
│   └── Automated application tests
│
├── scripts/
│   └── Development and automation scripts
│
├── monitoring/
│   ├── prometheus.yml
│   └── grafana/
│       ├── dashboards/
│       │   └── sentinel.json
│       └── provisioning/
│           ├── datasources/
│           └── dashboards/
│
├── deploy/
│   ├── verify.sh
│   ├── backup-db.sh
│   ├── test-restore.sh
│   ├── manage.sh
│   └── update.sh
│
├── docs/
│   ├── STAGE09_MONITORING.md
│   ├── STAGE10_DEPLOYMENT.md
│   └── PROJECT_FINAL.md
│
├── .dockerignore
├── .gitignore
├── .env.compose.example
├── Dockerfile
├── compose.yaml
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

The structure separates application logic, background processing,
testing, monitoring, deployment automation, and documentation.

---

## 🚀 Getting Started

### Prerequisites

Make sure the following tools are installed:

- Git
- Docker Engine or Docker Desktop
- Docker Compose
- Linux or WSL2
- Python for local development

Verify Docker:

```bash
docker --version
docker compose version
```

Verify Git:

```bash
git --version
```

### 1. Clone the Repository

Using HTTPS:

```bash
git clone https://github.com/yousefhilal2004-design/devops-sentinel.git

cd devops-sentinel
```

Or using SSH:

```bash
git clone git@github.com:yousefhilal2004-design/devops-sentinel.git

cd devops-sentinel
```

### 2. Configure Environment Variables

Create the local environment file:

```bash
cp .env.compose.example .env.compose

chmod 600 .env.compose
```

Edit the configuration:

```bash
nano .env.compose
```

Configure the database credentials, application settings,
monitoring restrictions, and Grafana credentials.

Replace example passwords with unique passwords.

Never commit the actual environment file to GitHub.

### 3. Validate Docker Compose

```bash
docker compose --env-file .env.compose config --quiet
```

### 4. Build and Start the Application

```bash
docker compose --env-file .env.compose up -d --build
```

### 5. Verify Container Status

```bash
docker compose --env-file .env.compose ps
```

The following five services should be running:

| Service | Purpose |
|---|---|
| api | FastAPI REST API |
| db | PostgreSQL database |
| worker | Background monitoring |
| prometheus | Metrics collection |
| grafana | Monitoring visualization |

### 6. Access the Application

| Service | URL |
|---|---|
| FastAPI | http://localhost:8001 |
| Swagger UI | http://localhost:8001/docs |
| ReDoc | http://localhost:8001/redoc |
| OpenAPI | http://localhost:8001/openapi.json |
| Health Endpoint | http://localhost:8001/health |
| Application Metrics | http://localhost:8001/metrics/ |
| Prometheus | http://localhost:9091 |
| Prometheus Targets | http://localhost:9091/targets |
| Grafana | http://localhost:3001 |

The current deployment uses ports 8001, 9091, and 3001
to avoid conflicts with existing local services.

---

## 🔌 API Documentation

DevOps Sentinel provides REST API endpoints for managing
registered services and accessing monitoring information.

### Available Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Application information |
| GET | `/health` | Application health |
| GET | `/docs` | Swagger documentation |
| GET | `/redoc` | ReDoc documentation |
| GET | `/openapi.json` | OpenAPI specification |
| POST | `/services` | Register a new service |
| GET | `/services` | List registered services |
| GET | `/services/{service_id}` | Retrieve a service |
| PATCH | `/services/{service_id}` | Update a service |
| DELETE | `/services/{service_id}` | Delete a service |
| GET | `/services/{service_id}/checks` | Retrieve monitoring history |
| GET | `/metrics/` | Prometheus metrics |

### Check Application Health

```bash
curl -fsS http://localhost:8001/health
```

### List Registered Services

```bash
curl -fsS http://localhost:8001/services
```

### Retrieve a Specific Service

Replace SERVICE_ID with an existing service identifier.

```bash
curl -fsS http://localhost:8001/services/SERVICE_ID
```

### Retrieve Monitoring History

```bash
curl -fsS \
  "http://localhost:8001/services/SERVICE_ID/checks?limit=10"
```

### Interactive API Testing

Swagger UI provides an interactive interface for testing
API endpoints and viewing request and response schemas.

Open:

http://localhost:8001/docs

Use the documented request schemas when creating or updating
registered services.

---

## 🗄️ Database

PostgreSQL is used as the main database for DevOps Sentinel.

The database stores registered services and monitoring results.

### Database Features

- Persistent application data.
- Integration with FastAPI.
- Integration with the background worker.
- Docker volume-based storage.
- Database health checks.
- Environment-based credentials.
- Separate test database.
- Backup and recovery support.

### Database Access

PostgreSQL runs internally on port 5432.

The database port is not published to the host in the
current application deployment.

Application components communicate with PostgreSQL through
Docker's internal network.

### Persistent Storage

Docker volumes are used to preserve database data when
containers are stopped or recreated.

View existing volumes:

```bash
docker volume ls
```

Avoid removing database volumes unless the stored data is
no longer required and an appropriate backup exists.

---

## ⚙️ Background Worker

The background worker performs service-monitoring tasks
independently of the FastAPI application.

### Worker Responsibilities

- Retrieve registered services from PostgreSQL.
- Perform service availability checks.
- Process monitoring results.
- Store check history in PostgreSQL.
- Continue monitoring independently of API requests.

The worker runs as a separate Docker Compose service.

### View Worker Logs

```bash
docker compose --env-file .env.compose logs --tail=100 worker
```

Follow worker logs:

```bash
docker compose --env-file .env.compose logs -f worker
```

The monitoring worker should only check authorized services
that satisfy the application's monitoring configuration.

---

## 🐳 Docker and Containerization

Docker provides a consistent runtime environment for
DevOps Sentinel.

### Docker Implementation

The project uses:

- Multi-stage Docker builds.
- A Python-based application image.
- Separate builder and runtime stages.
- Optimized dependency installation.
- Non-root application execution.
- Docker Compose service orchestration.
- Container health checks.
- Persistent volumes.
- Internal networking.
- Environment-based configuration.

### Container Architecture

```mermaid
flowchart TD
    Host[Linux Host]

    subgraph Docker[Docker Compose Environment]
        API[API Container]
        Worker[Worker Container]
        DB[(PostgreSQL Container)]
        Prometheus[Prometheus Container]
        Grafana[Grafana Container]

        API --> DB
        Worker --> DB
        Prometheus --> API
        Grafana --> Prometheus
    end

    Host -->|127.0.0.1:8001| API
    Host -->|127.0.0.1:9091| Prometheus
    Host -->|127.0.0.1:3001| Grafana
```

### Build the Application Image

```bash
docker compose --env-file .env.compose build
```

### Start Services

```bash
docker compose --env-file .env.compose up -d
```

### Stop Services

```bash
docker compose --env-file .env.compose stop
```

### Restart Services

```bash
docker compose --env-file .env.compose restart
```

### View Logs

```bash
docker compose --env-file .env.compose logs --tail=100
```

### Remove Containers While Preserving Named Volumes

```bash
docker compose --env-file .env.compose down
```

Do not use `down -v` during normal operations because it
removes Compose-managed volumes and may delete application data.

---

## 🧪 Testing and Code Quality

Automated testing and code quality checks are important parts
of the development workflow.

### Create a Python Virtual Environment

```bash
python3 -m venv .venv

source .venv/bin/activate
```

### Install Dependencies

```bash
python -m pip install -r requirements.txt

python -m pip install -r requirements-dev.txt
```

### Ruff Linting

```bash
python -m ruff check app worker tests
```

Automatically fix supported linting issues:

```bash
python -m ruff check app worker tests --fix
```

### Ruff Formatting

Check formatting:

```bash
python -m ruff format --check app worker tests
```

Apply formatting:

```bash
python -m ruff format app worker tests
```

### Test Database

Integration tests use a separate PostgreSQL database.

| Setting | Value |
|---|---|
| Container | sentinel-test-db |
| Database | sentinel_test |
| Host Port | 5433 |
| Container Port | 5432 |

The test database is isolated from the deployed application
database.

Create the test database container if it does not already exist:

```bash
docker run -d \
  --name sentinel-test-db \
  -e POSTGRES_USER=sentinel \
  -e POSTGRES_PASSWORD=sentinel_local_dev_only \
  -e POSTGRES_DB=sentinel_test \
  -p 127.0.0.1:5433:5432 \
  postgres:17
```

The example password above is intended only for disposable
local testing.

If the container already exists, start it instead:

```bash
docker start sentinel-test-db
```

Verify database readiness:

```bash
docker exec sentinel-test-db \
  pg_isready -U sentinel -d sentinel_test
```

### Run Automated Tests

Use the isolated test database configuration before running tests.

```bash
export DATABASE_URL="postgresql://sentinel:sentinel_local_dev_only@127.0.0.1:5433/sentinel_test"

export ALLOWED_MONITOR_HOSTS="example.com"

python -m pytest -v
```

Clear the temporary database configuration after testing:

```bash
unset DATABASE_URL
unset ALLOWED_MONITOR_HOSTS
```

Never run database integration tests against the deployed
application database.

---

## 🔄 CI/CD Pipeline

DevOps Sentinel uses GitHub Actions to automate application
validation.

The CI pipeline provides feedback about code quality, testing,
dependency security, and container security.

### Pipeline Components

| Component | Purpose |
|---|---|
| Repository Checkout | Retrieve source code |
| Python Setup | Prepare Python environment |
| Dependency Installation | Install required packages |
| Ruff Linting | Detect code quality issues |
| Ruff Formatting | Validate formatting |
| PostgreSQL Test Service | Provide isolated test database |
| pytest | Execute automated tests |
| Dependency Audit | Identify vulnerable packages |
| Docker Build | Build the application image |
| Trivy Scan | Detect container vulnerabilities |

### Pipeline Workflow

```mermaid
flowchart TD
    Push[Git Push / Pull Request]
    CI[GitHub Actions]
    Quality[Lint and Format]
    Test[Automated Tests]
    Audit[Dependency Audit]
    Build[Docker Image Build]
    Scan[Trivy Security Scan]
    Result{Validation Passed?}
    Success[Successful CI]
    Failure[Failed CI - Review Logs]

    Push --> CI
    CI --> Quality
    CI --> Test
    CI --> Audit
    CI --> Build
    Build --> Scan
    Quality --> Result
    Test --> Result
    Audit --> Result
    Scan --> Result
    Result -->|Yes| Success
    Result -->|No| Failure
```

### View Pipeline Results

[GitHub Actions Workflows](https://github.com/yousefhilal2004-design/devops-sentinel/actions)

The current project implements continuous integration and a
manual deployment workflow. Fully automated deployment and
automatic rollback remain future improvements.

---

## 🔐 Security

Security is integrated into the development, containerization,
and deployment workflow.

### Dependency Security

Python dependencies are audited to identify known vulnerabilities.

```bash
python -m pip_audit -r requirements.txt
```

### Container Security

Trivy scans the application container image for known
vulnerabilities.

The CI security policy checks high and critical severity findings.

A failed security scan requires reviewing the affected packages,
updating vulnerable dependencies when fixes are available,
rebuilding the image, and running the validation again.

### Container Hardening

The application Docker image uses:

- Multi-stage builds.
- Non-root execution.
- A separate runtime environment.
- Reduced unnecessary runtime tooling.
- Dependency vulnerability scanning.

### Secret Management

Sensitive configuration is stored in local environment files.

Examples include:

- Database passwords.
- Application database connection settings.
- Grafana administrator credentials.

Only example configuration files should be committed.

The actual `.env.compose` file must remain private.

Verify that the environment file is ignored:

```bash
git check-ignore .env.compose
```

Verify that it is not tracked:

```bash
git ls-files .env.compose
```

### Network Security

The current deployment uses private host bindings.

| Service | Host Binding |
|---|---|
| FastAPI | 127.0.0.1:8001 |
| Prometheus | 127.0.0.1:9091 |
| Grafana | 127.0.0.1:3001 |
| PostgreSQL | Not published |
| Worker | Not published |

This configuration reduces unnecessary network exposure.

A public production deployment would require additional
security controls, authentication, HTTPS, and infrastructure
hardening.

---

## 📊 Monitoring and Observability

DevOps Sentinel uses Prometheus and Grafana to monitor
application behavior and performance.

### Monitoring Architecture

```mermaid
flowchart LR
    Traffic[Application Requests]
    API[FastAPI]
    Middleware[Metrics Middleware]
    Endpoint[Metrics Endpoint]
    Prometheus[Prometheus]
    Grafana[Grafana Dashboard]

    Traffic --> API
    API --> Middleware
    Middleware --> Endpoint
    Prometheus -->|Scrape| Endpoint
    Grafana -->|Query| Prometheus
```

### Prometheus

Prometheus periodically collects application metrics from:

```text
http://api:8000/metrics/
```

The internal Docker service address is used instead of
the host port.

### Application Metrics

| Metric | Type | Purpose |
|---|---|---|
| sentinel_http_requests_total | Counter | Total HTTP requests |
| sentinel_http_request_duration_seconds | Histogram | Request duration |
| sentinel_http_requests_in_progress | Gauge | Active HTTP requests |

### Metric Labels

Request metrics include relevant labels such as:

- HTTP method.
- API endpoint.
- HTTP status code.

### Verify Application Metrics

```bash
curl -fsS http://localhost:8001/metrics/
```

Filter custom Sentinel metrics:

```bash
curl -fsS http://localhost:8001/metrics/ | grep sentinel_
```

### Generate Application Traffic

```bash
for i in {1..30}; do
    curl -fsS -o /dev/null \
        http://localhost:8001/health
done
```

Allow Prometheus time to collect the generated metrics.

### Verify Prometheus

Open:

http://localhost:9091/targets

Check that the configured monitoring targets are UP.

### PromQL Queries

#### Total HTTP Requests

```promql
sum(sentinel_http_requests_total)
```

#### HTTP Requests per Second

```promql
sum(rate(sentinel_http_requests_total[5m]))
```

#### Requests by HTTP Method

```promql
sum by (method) (
    rate(sentinel_http_requests_total[5m])
)
```

#### Requests by Status Code

```promql
sum by (status_code) (
    rate(sentinel_http_requests_total[5m])
)
```

#### Server Error Rate

```promql
sum(
    rate(
        sentinel_http_requests_total{
            status_code=~"5.."
        }[5m]
    )
)
```

#### Average Request Duration

```promql
sum(
    rate(sentinel_http_request_duration_seconds_sum[5m])
)
/
sum(
    rate(sentinel_http_request_duration_seconds_count[5m])
)
```

#### 95th Percentile Request Duration

```promql
histogram_quantile(
    0.95,
    sum by (le) (
        rate(
            sentinel_http_request_duration_seconds_bucket[5m]
        )
    )
)
```

#### Active Requests

```promql
sentinel_http_requests_in_progress
```

### Grafana

Grafana provides visual dashboards using Prometheus as
the data source.

Open:

http://localhost:3001

The monitoring dashboard is provisioned through files
stored in the monitoring directory.

The dashboard visualizes application request activity,
HTTP status codes, and request duration.

---

## 🖥️ Linux Deployment

The current deployment environment is Ubuntu Linux running
through WSL2.

This environment was used to practice Linux deployment,
Docker Compose operations, private networking, application
verification, and database management.

### Deployment Architecture

```mermaid
flowchart TD
    Windows[Windows Host]
    WSL[Ubuntu WSL2]

    subgraph Application[Docker Compose Stack]
        API[FastAPI]
        DB[(PostgreSQL)]
        Worker[Monitoring Worker]
        Prometheus[Prometheus]
        Grafana[Grafana]
    end

    Windows --> WSL
    WSL --> API
    WSL --> Prometheus
    WSL --> Grafana
    API --> DB
    Worker --> DB
    Prometheus --> API
    Grafana --> Prometheus
```

### Port Configuration

| Service | Host Port | Container Port |
|---|---:|---:|
| FastAPI | 8001 | 8000 |
| Prometheus | 9091 | 9090 |
| Grafana | 3001 | 3000 |
| PostgreSQL | Private | 5432 |

The host ports were changed to resolve conflicts with existing
local services.

Internal container ports remain unchanged.

### Deploy the Application

```bash
docker compose --env-file .env.compose up -d --build
```

### Verify Deployment

```bash
docker compose --env-file .env.compose ps
```

Run the deployment verification script:

```bash
./deploy/verify.sh
```

The script checks:

- Docker Compose configuration.
- Container status.
- API health endpoint.
- Application metrics.
- Prometheus health.
- Grafana health.

### Deployment Scope

The current deployment is a local Linux learning deployment.

The application can be adapted to a dedicated Ubuntu server,
but remote production hosting is not claimed as part of the
current implementation.

---

## 💾 Database Backup and Recovery

Database backup and recovery procedures are included to
protect application data and practice operational reliability.

### Backup Architecture

```mermaid
flowchart LR
    DB[(Application Database)]
    Dump[pg_dump]
    File[Timestamped Backup File]
    Restore[pg_restore]
    TestDB[(Temporary Recovery Database)]
    Verify[Recovery Verification]

    DB --> Dump
    Dump --> File
    File --> Restore
    Restore --> TestDB
    TestDB --> Verify
```

### Create a Database Backup

```bash
./deploy/backup-db.sh
```

Backups are stored outside the Git repository:

```text
~/sentinel-backups/
```

The backup script uses:

- PostgreSQL pg_dump.
- Timestamped backup filenames.
- PostgreSQL custom backup format.
- Restricted file permissions.
- Temporary files during backup creation.
- Archive validation using pg_restore.

### View Available Backups

```bash
ls -lh ~/sentinel-backups/
```

### Test Database Recovery

Select an existing backup file:

```bash
LATEST_BACKUP="$(find "$HOME/sentinel-backups" \
    -maxdepth 1 \
    -type f \
    -name 'sentinel-*.dump' \
    | sort | tail -n 1)"
```

Run the recovery test:

```bash
./deploy/test-restore.sh "$LATEST_BACKUP"
```

The recovery script restores the selected backup into a
temporary database.

This allows backup recovery to be tested without overwriting
the application database.

### Scheduled Backups

Cron can be used to schedule daily database backups.

Example schedule:

```cron
0 2 * * * /absolute/path/to/devops-sentinel/deploy/backup-db.sh >> /absolute/path/to/backup.log 2>&1
```

Replace the example paths with the actual deployment and
log file paths.

In WSL2, scheduled backups require WSL and Docker to be running.

Local backup files should eventually be supplemented with
encrypted off-site backups and a backup retention policy.

---

## 🔧 Deployment Operations

The deploy directory contains Bash scripts that simplify
application administration.

### Deployment Scripts

| Script | Responsibility |
|---|---|
| verify.sh | Verify application endpoints |
| backup-db.sh | Create PostgreSQL backups |
| test-restore.sh | Test database recovery |
| manage.sh | Manage application services |
| update.sh | Perform manual deployment updates |

### Application Management

Display available commands:

```bash
./deploy/manage.sh help
```

Start the application:

```bash
./deploy/manage.sh start
```

Stop the application:

```bash
./deploy/manage.sh stop
```

Restart the application:

```bash
./deploy/manage.sh restart
```

Check application status:

```bash
./deploy/manage.sh status
```

View API logs:

```bash
./deploy/manage.sh logs api
```

View worker logs:

```bash
./deploy/manage.sh logs worker
```

Follow application logs:

```bash
./deploy/manage.sh follow api
```

Verify application endpoints:

```bash
./deploy/manage.sh verify
```

Create a database backup:

```bash
./deploy/manage.sh backup
```

### Manual Deployment Updates

The update script provides a basic deployment workflow.

```mermaid
flowchart TD
    Start[Start Update]
    Clean[Check Git Working Directory]
    Backup[Create Database Backup]
    Pull[Pull Latest Changes]
    Config[Validate Compose Configuration]
    Build[Build Application Image]
    Deploy[Update Containers]
    Verify[Verify Application Endpoints]
    Finish[Update Completed]

    Start --> Clean
    Clean --> Backup
    Backup --> Pull
    Pull --> Config
    Config --> Build
    Build --> Deploy
    Deploy --> Verify
    Verify --> Finish
```

Before updating, make sure the working directory is clean
and the latest changes have passed CI validation.

```bash
git status
```

Run the update script:

```bash
./deploy/update.sh
```

Automatic rollback is not implemented in the current
deployment workflow.

---

## 🩺 Troubleshooting

### Container Status

```bash
docker compose --env-file .env.compose ps -a
```

### Application Logs

```bash
docker compose --env-file .env.compose logs --tail=100 api
```

### Database Logs

```bash
docker compose --env-file .env.compose logs --tail=100 db
```

### Worker Logs

```bash
docker compose --env-file .env.compose logs --tail=100 worker
```

### Port Already in Use

A port conflict occurs when another application or container
is already using the required host port.

Check active listening ports:

```bash
sudo ss -ltnp
```

Check published Docker ports:

```bash
docker ps --format 'table {{.Names}}\t{{.Ports}}'
```

Change the host-side port mapping when necessary without
changing the application's internal container port.

### API Container Is Unhealthy

Check API and database logs:

```bash
docker compose --env-file .env.compose logs api db
```

Verify database health and application configuration.

### Prometheus Target Is Down

Check Prometheus logs:

```bash
docker compose --env-file .env.compose logs prometheus
```

Verify that the application metrics endpoint is available:

```bash
curl -fsS http://localhost:8001/metrics/
```

Check the internal Prometheus target configuration.

### Grafana Dashboard Has No Data

Verify:

- Prometheus is running.
- Prometheus scrape targets are UP.
- The Grafana data source is configured correctly.
- Application traffic has been generated.
- The selected dashboard time range is appropriate.

### GitHub HTTPS Authentication Failure

GitHub does not support account password authentication
for Git operations over HTTPS.

If SSH authentication is configured, update the remote:

```bash
git remote set-url origin \
  git@github.com:yousefhilal2004-design/devops-sentinel.git
```

Test SSH authentication:

```bash
ssh -T git@github.com
```

Push changes:

```bash
git push origin main
```

---

## 📋 Project Documentation

Additional project documentation is available in the docs directory.

| Document | Description |
|---|---|
| [Monitoring Documentation](docs/STAGE09_MONITORING.md) | Prometheus, Grafana, and application metrics |
| [Deployment Documentation](docs/STAGE10_DEPLOYMENT.md) | Linux deployment and operational procedures |
| [Final Project Documentation](docs/PROJECT_FINAL.md) | Complete project overview |

---

## 🧠 Skills Demonstrated

This project demonstrates practical experience across
multiple areas of DevOps engineering.

### Linux Administration

- Linux command-line operations.
- File and directory management.
- File permissions.
- Process and service management.
- Environment configuration.
- Scheduled tasks.
- Application troubleshooting.

### Bash and Automation

- Bash scripting.
- Error handling.
- Environment variables.
- Deployment automation.
- Backup automation.
- Operational scripts.
- Recovery testing.

### Git and GitHub

- Repository management.
- Version control.
- Structured commits.
- Remote repository management.
- SSH authentication.
- GitHub Actions integration.
- Project documentation.

### Networking

- HTTP communication.
- API endpoints.
- Service availability monitoring.
- TCP port configuration.
- Docker networking.
- Localhost bindings.
- Internal service communication.
- Port conflict troubleshooting.

### Python and Backend Development

- Python application development.
- REST API implementation.
- FastAPI.
- Background processing.
- Dependency management.
- Database integration.
- Automated testing.
- Application metrics.

### Docker

- Docker image creation.
- Dockerfile development.
- Multi-stage builds.
- Docker Compose.
- Container networking.
- Persistent volumes.
- Container health checks.
- Service orchestration.
- Container troubleshooting.

### CI/CD and Security

- Continuous integration.
- Automated quality checks.
- Automated testing.
- Container image validation.
- Dependency vulnerability auditing.
- Container vulnerability scanning.
- Secret management.
- Basic container hardening.

### Monitoring and Observability

- Prometheus.
- Grafana.
- PromQL.
- Application instrumentation.
- HTTP request monitoring.
- Latency monitoring.
- Dashboard visualization.

### Deployment and Operations

- Linux application deployment.
- Application lifecycle management.
- Deployment verification.
- Database backup.
- Database recovery testing.
- Scheduled backups.
- Manual deployment updates.
- Operational troubleshooting.

---

## 🔮 Future Improvements

The current project provides a foundation for more advanced
DevOps and infrastructure engineering topics.

### Infrastructure

- Dedicated remote Linux server deployment.
- Cloud infrastructure deployment.
- Infrastructure as Code using Terraform.
- Configuration management using Ansible.

### Container Orchestration

- Kubernetes fundamentals.
- Kubernetes Deployments and Services.
- ConfigMaps and Secrets.
- Persistent Volumes.
- Kubernetes health probes.
- Helm charts.
- Kubernetes-based application deployment.

### CI/CD

- Container registry integration.
- Automated deployment pipelines.
- Deployment environments.
- Automated rollback.
- GitOps workflows.
- Release automation.

### Security

- HTTPS reverse proxy.
- API authentication and authorization.
- Advanced secret management.
- Additional container security policies.
- Software Bill of Materials.
- Image signing.

### Observability

- Alertmanager integration.
- Centralized logging.
- Grafana Loki.
- Distributed tracing.
- OpenTelemetry.
- Infrastructure monitoring.
- Service-level objectives.

### Reliability

- Automated backup retention.
- Encrypted off-site backups.
- Disaster recovery procedures.
- High availability.
- Load balancing.
- Performance testing.

---

## 📌 Project Status

DevOps Sentinel currently focuses on the complete
Docker Compose–based application lifecycle.

| Area | Status |
|---|---|
| Application Development | Implemented |
| PostgreSQL Integration | Implemented |
| Background Monitoring | Implemented |
| Linux and Bash Automation | Implemented |
| Docker Containerization | Implemented |
| Docker Compose | Implemented |
| Automated Testing | Implemented |
| GitHub Actions CI | Implemented |
| Security Scanning | Implemented |
| Prometheus Monitoring | Implemented |
| Grafana Dashboards | Implemented |
| Local Linux Deployment | Implemented |
| Backup and Recovery Scripts | Stage 10 |
| Deployment Management Scripts | Stage 10 |
| Automated Remote Deployment | Planned |
| Cloud Infrastructure | Planned |
| Terraform | Planned |
| Kubernetes | Planned |
| Helm | Planned |

The current milestone covers Stages 01–10.

Kubernetes integration will be introduced in future versions
after completing dedicated Kubernetes learning.

---

## 🎓 What I Learned

Building DevOps Sentinel helped me understand how different
DevOps tools work together in a practical application.

During this project, I practiced building a backend application,
connecting it to a database, running background tasks,
containerizing services, and managing their communication.

I also learned how to automate testing and code quality checks,
identify security vulnerabilities, collect application metrics,
visualize performance, and manage an application deployment
in a Linux environment.

Some of the most important lessons were:

- Understanding the complete application lifecycle.
- Troubleshooting container startup failures.
- Resolving host port conflicts.
- Managing application configuration securely.
- Investigating failed CI workflows.
- Updating vulnerable dependencies.
- Understanding the importance of persistent storage.
- Preparing database backup and recovery procedures.
- Understanding the difference between monitoring and deployment.
- Writing clear technical documentation.

This project represents an important milestone in my
DevOps learning journey and provides a foundation for
future cloud and Kubernetes projects.

---

## 👨‍💻 Author

**Yousef Aed Hilal**

Computer Engineering — Birzeit University

Aspiring DevOps Engineer

Interests:

- DevOps Engineering
- Linux Administration
- Cloud Computing
- Infrastructure Automation
- Containerization
- CI/CD
- Monitoring and Observability

GitHub:

https://github.com/yousefhilal2004-design

Project Repository:

https://github.com/yousefhilal2004-design/devops-sentinel

---

## ⭐ Acknowledgments

This project was developed as an independent practical learning
project to apply DevOps engineering concepts in a complete
application environment.

The project uses open-source technologies including Python,
FastAPI, PostgreSQL, Docker, Prometheus, and Grafana.

---

**DevOps Sentinel — Build. Test. Secure. Deploy. Monitor. Improve.**
