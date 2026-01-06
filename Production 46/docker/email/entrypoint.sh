#!/bin/bash

/usr/local/bin/wait-for-it.sh email_db:5432 --timeout=30 --strict -- echo "Database is up and ready"

echo "Run Alembic migrations..."
uv run alembic revision --autogenerate -m "Init databases" || echo "Migration already exists"
uv run alembic upgrade head

echo "Starting FastAPI application..."
uv run uvicorn notification_email_service.main:app --host 0.0.0.0 --port 9090
