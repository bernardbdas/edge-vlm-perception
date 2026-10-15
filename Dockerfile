# Multi-Stage Build: Bun Frontend + uv Python Backend

FROM oven/bun:1.2-slim AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package.json frontend/bun.lock* ./
RUN bun install
COPY frontend/ ./
RUN bun run build

FROM python:3.11-slim AS runner
WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock* ./
RUN uv pip install --system -e .

COPY src/ ./src/
COPY configs/ ./configs/
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

EXPOSE 8005

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8005"]
