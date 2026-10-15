# ═══════════════════════════════════════════════════════════════════════
# SYS_05 // EDGE VLM PERCEPTION SYSTEM JUSTFILE
# Frontend: Vite + React 19 + TypeScript (Bun)
# Backend:  FastAPI + TensorRT + ROS2 + Python 3.11 (Python uv)
# ═══════════════════════════════════════════════════════════════════════

default:
    @just --list

install:
    @echo "[+] Syncing Python backend dependencies with uv..."
    uv sync --extra dev
    @echo "[+] Installing React frontend dependencies with bun..."
    cd frontend && bun install

# Run backend independently on port 8005
backend host="0.0.0.0" port="8005":
    @echo "[*] Launching Edge VLM Perception API on http://{{host}}:{{port}}..."
    uv run uvicorn src.main:app --host {{host}} --port {{port}} --reload

# Run frontend independently on port 5175 (proxies /api to :8005)
frontend:
    @echo "[*] Launching Vite React frontend on http://localhost:5175..."
    cd frontend && bun run dev

# Run both backend and frontend concurrently
dev:
    @echo "[*] Launching Edge Perception Mesh (Backend: :8005 | Frontend: :5175)..."
    (trap 'kill 0' SIGINT; just backend & just frontend)

# Build production bundle with Vite
build:
    @echo "[*] Building Vite frontend production bundle..."
    cd frontend && bun run build

# Run test suite
test:
    @echo "[*] Running backend pytest suite..."
    uv run pytest
    @echo "[*] Typechecking frontend..."
    cd frontend && bun run build

# Execute open-vocabulary spatial detection via CLI
detect prompt="locate robotic arm components":
    uv run edge-cli detect -p "{{prompt}}"

# Display NVIDIA Jetson AGX Orin hardware telemetry via CLI
telemetry:
    uv run edge-cli telemetry

docker-build:
    docker build -t edge-vlm-perception:latest .

docker-up:
    docker compose up -d

docker-down:
    docker compose down
