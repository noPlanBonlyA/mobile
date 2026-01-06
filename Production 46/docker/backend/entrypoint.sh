#!/bin/bash

/usr/local/bin/wait-for-it.sh db:5432 --timeout=30 --strict -- echo "Database is up and ready"

echo "Run Alembic migrations..."
uv run alembic upgrade head

echo "Starting FastAPI application..."
uv run python -m scripts.create_user --password 1 --role superadmin --first_name a --surname a --patronymic c --email a@email.ru --birth_date 11.07.2000 --phone_number +79642501606
uv run uvicorn school_site.main:app --host 0.0.0.0 --port 8080
