FROM python:3.12-slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY ./backendITSchool .

RUN uv sync --frozen

COPY ./docker/scripts/wait-for-it.sh /usr/local/bin/
COPY ./docker/backend/entrypoint.sh /docker/entrypoint.sh

RUN chmod +x /docker/entrypoint.sh \
    && chmod +x /usr/local/bin/wait-for-it.sh