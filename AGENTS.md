# ==============================================================================
# AGENTS.MD — EDGE VLM PERCEPTION (SYS_05)
# Production Architecture, Rules & Operational Directives
# Author: Bernard Birendra Das (https://github.com/bernardbdas)
# ==============================================================================

> **MANDATORY SPECIFICATION FOR AUTONOMOUS AGENTS AND DEVELOPERS**
> This repository strictly adheres to the engineering standards, architecture, and design styles specified herein. No simplifications, removals, or degradations are permitted.

---

## 1. System Topology & Identity

- **System ID**: `SYS_05`
- **Repository Name**: `edge-vlm-perception`
- **Primary Domain**: Low-Latency Vision-Language Perception Pipeline with TensorRT INT4 Quantization & ROS2 Robotics Telemetry for NVIDIA Jetson Orin
- **Backend Port**: `8005` (FastAPI)
- **Frontend Framework**: Vite + React 19 + TypeScript (Scaffolded with `bun`)
- **Frontend Port (Dev)**: `5173`
- **UI Aesthetic Style**: **High-Tech Tactical HUD / Military Cyber-Brutalist Interface** (Inspired by Bernard's portfolio `bernardbdas.github.io` & UXPlanet HUD Brutalism)
  - Color Palette: Matte black `#08090a`, tactical amber `#ff9900`, targeting reticle red `#ff3333`, phosphor green `#00ff88`, hairline grid `#1c1f24`
  - Typography: Monospace (`JetBrains Mono`, `IBM Plex Mono`)
  - Layout: High-density real-time tactical camera HUD with bounding box overlays, target coordinate reticles, TensorRT latency counters, and ROS2 topic status
- **Domain CLI**: `edge-cli` (`src/cli.py`)

---

## 2. Decoupled Architecture & Execution Directives

1. **Decoupled Independence**:
   - Backend and frontend are completely decoupled and must run independently.
   - Run backend independently: `just backend` (FastAPI on port `8005`).
   - Run frontend independently: `just frontend` (Vite dev server on port `5173`).
   - Run both concurrently: `just dev`.
2. **Production Serving**:
   - Compiling frontend via `just build` writes to `frontend/dist`.
   - In production, FastAPI statically mounts `frontend/dist` at `/`.
   - Streaming endpoints (`/video/stream`, `/telemetry`, `/detect`, `/prompt/update`) always take routing priority.

---

## 3. Project Management with `uv`

1. **UV Enforcement**: All Python environment management, locking, and execution MUST use `uv`.
2. **Build System**: Managed via `hatchling` in `pyproject.toml`:
   ```toml
   [build-system]
   requires = ["hatchling"]
   build-backend = "hatchling.build"

   [tool.hatch.build.targets.wheel]
   packages = ["src"]
   ```
3. **Jetson & Robotic Drivers**: Graceful fallback for Jetson-specific libraries (TensorRT, PyCUDA, ROS2 rclpy) when running outside target hardware.

---

## 4. Frontend & UI Design Rules (`bun` & Tactical HUD)

1. Managed exclusively using `bun` inside `frontend/`.
2. High-Tech Tactical HUD styling:
   - Live simulated/hardware MJPEG video stream with target bounding coordinates.
   - Spatial grounding prompt input drawer with instantaneous ROS2 topic publishing.
   - Edge telemetry: TensorRT inference time (<22ms), memory usage, and FPS counters.

---

## 5. Command Runner (`just`) Specification

Standardized `Justfile` tasks:
- `just backend`: Run FastAPI server (`http://localhost:8005`) with reload.
- `just frontend`: Run Bun frontend dev server.
- `just dev`: Launch backend and frontend concurrently.
- `just install`: Install backend with `uv sync --extra dev` and frontend with `bun install`.
- `just test`: Run `uv run pytest` and frontend TypeScript check.
- `just build`: Compile frontend to `dist/` and build Python wheel.
- `just check`: Run `uv run ruff check src` and format checks.
- `just benchmark`: Run TensorRT FP16/INT4 latency benchmark.
- `just set-prompt "<text>"`: Update ROS2 spatial grounding target.
- `just docker-build`: Build multi-stage production Docker image.
- `just docker-up`: Start perception services via Docker Compose.

---

## 6. Containerization & Docker

- Multi-stage `Dockerfile`:
  - Stage 1: `oven/bun:1-alpine` compiles `frontend/dist`.
  - Stage 2: `python:3.11-slim` installs dependencies via `uv sync --frozen --no-dev` and hosts FastAPI.
- `docker-compose.yml`: Configured for edge hardware passthrough and camera mounts.

---

## 7. Developer Tooling & `.vscode` Setup

- `.vscode/settings.json`: Configured with Ruff default formatter, format on save, and `.venv` python interpreter path.
- `.vscode/launch.json`: Debugging configurations for FastAPI backend, CLI commands, and Chrome frontend.
- `.vscode/extensions.json`: Recommended VS Code extensions.
- `.vscode/tasks.json`: Standard VS Code build and test tasks wired to `just`.

---

## 8. Environment Management Rules

- `example.env`: Tracked template with descriptions for camera index, TensorRT model path, and ROS2 topics.
- `local.env`: Tracked developer defaults for immediate out-of-the-box local execution.
- `.env` / `.env.local`: Ignored in `.gitignore` for private robotics credentials.

---

## 9. Code Quality, Linters & Pre-Commit Hooks

- Linter & Formatter: `ruff` with `select = ["E", "F", "I"]`, `line-length = 100`.
- Pre-commit hooks (`.pre-commit-config.yaml`):
  - `trailing-whitespace`, `end-of-file-fixer`, `check-yaml`, `check-toml`, `check-added-large-files` (`--maxkb=5000`), `ruff`, and `ruff-format`.
- All git commits must be verified against pre-commit hooks.

---

## 10. Continuous Integration (CI)

- `.github/workflows/ci.yml` runs on every push and PR to `main`:
  - Python lint (`ruff check src`) and test (`pytest`).
  - Bun frontend typecheck (`tsc -b`) and build (`bun run build`).

---

## 11. Git & Remote Repository Rules

- Branch: `main`.
- Remote: `https://github.com/bernardbdas/edge-vlm-perception.git`.
