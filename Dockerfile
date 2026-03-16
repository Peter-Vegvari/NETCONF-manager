# --- Frontend build ---
FROM node:22-slim AS frontend
WORKDIR /app
COPY manager-frontend/package.json manager-frontend/package-lock.json ./
RUN npm ci
COPY manager-frontend/ ./
RUN npm run build

# --- Backend ---
FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim
WORKDIR /app

COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --frozen --no-dev --no-install-project

COPY src/ src/
RUN uv sync --frozen --no-dev

COPY --from=frontend /app/dist static/

ENV FASTAPI_STATIC_DIR=static

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "netconf_manager.main:app", "--host", "0.0.0.0", "--port", "8000"]
