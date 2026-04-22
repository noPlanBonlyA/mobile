#!/bin/bash
uv run uvicorn school_site.main:app --host 0.0.0.0 --port 8080 --reload