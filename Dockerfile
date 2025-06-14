# Base Python image
FROM python:3.12-slim-bookworm AS base
# Stage to copy the uv binary from the external image
FROM ghcr.io/astral-sh/uv:latest AS uv-binary
# Builder stage: setup environment and install dependencies using uv
FROM base AS builder
COPY --from=uv-binary /uv /bin/uv
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
WORKDIR /app
COPY uv.lock pyproject.toml /app/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev
COPY . /app
# Final runtime image
FROM base
COPY --from=builder /app /app
COPY --from=builder /bin/uv /bin/uv
ENV PATH="/app/.venv/bin:$PATH"
WORKDIR /app
CMD ["uv", "run", "server.py"] 