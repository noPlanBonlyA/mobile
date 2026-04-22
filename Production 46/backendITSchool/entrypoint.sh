#!/bin/bash

/usr/local/bin/wait-for-it.sh db:5432 --timeout=30 --strict -- echo "Database is up and ready"

echo "Run Alembic migrations..."
uv run alembic revision --autogenerate -m "Init databases" || echo "Migration already exists"
uv run alembic upgrade head

echo "Starting FastAPI application..."
uv run uvicorn school_site.main:app --host 0.0.0.0 --port 8080
