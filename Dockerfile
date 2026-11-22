# syntax=docker/dockerfile:1

# ======================================
# Stage 1 — Dependencies
# ======================================

FROM python:3.14-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /build

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

RUN python -m pip install \
    --no-cache-dir \
    -r requirements.txt


# ======================================
# Stage 2 — Runtime
# ======================================

FROM python:3.14-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Create non-root user
RUN groupadd --system sentinel && \
    useradd --system \
    --gid sentinel \
    --home-dir /app \
    sentinel

# Copy Python dependencies
COPY --from=builder /opt/venv /opt/venv

# Copy application files
COPY --chown=sentinel:sentinel app/ ./app/
COPY --chown=sentinel:sentinel worker/ ./worker/

# Run as non-root
USER sentinel

# FastAPI port
EXPOSE 8000

# Default command
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]