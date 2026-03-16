FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim
WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked
    
EXPOSE 8000
CMD ["uv", "run", "fastapi", "dev", "--host", "0.0.0.0", "src/main.py"]
