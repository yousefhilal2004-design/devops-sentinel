
# syntax=docker/dockerfile:1

# ==========================================
# STAGE 1 - BUILD DEPENDENCIES
# ==========================================

FROM python:3.14-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /build

# Install available Debian security updates
RUN apt-get update \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

# Create Python virtual environment
RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements
COPY requirements.txt .

# Upgrade packaging tools and install dependencies
RUN python -m pip install --no-cache-dir \
        --upgrade pip setuptools wheel \
    && python -m pip install --no-cache-dir \
        -r requirements.txt

# Remove build-only tools from virtual environment
RUN python -m pip uninstall -y \
        pip setuptools wheel

# ==========================================
# STAGE 2 - RUNTIME
# ==========================================

FROM python:3.14-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Install available Debian security updates
RUN apt-get update \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

# Remove system pip and its package metadata
# The application does not need pip at runtime
RUN rm -rf \
    /usr/local/lib/python3.14/site-packages/pip \
    /usr/local/lib/python3.14/site-packages/pip-*.dist-info

# Create non-root application user
RUN groupadd --system sentinel \
    && useradd --system \
        --gid sentinel \
        --home-dir /app \
        sentinel

# Copy Python virtual environment
COPY --from=builder /opt/venv /opt/venv

# Copy application source code
COPY --chown=sentinel:sentinel app/ ./app/
COPY --chown=sentinel:sentinel worker/ ./worker/

# Run application as non-root
USER sentinel

# FastAPI port
EXPOSE 8000

# Start FastAPI application
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
