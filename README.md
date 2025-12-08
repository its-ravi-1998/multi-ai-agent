## Multi-Agent AI

This repository is a starting point for a Python 3.13 project built with Poetry. The source layout lives under `app/`, with subpackages for configuration, routing, services, utilities, memory, and request/response models.

### Project structure
- `app/config.py` — configuration entry point (currently empty).
- `app/main.py` — application bootstrap placeholder.
- `app/routers.py/` — router definitions (e.g., `chat.py`).
- `app/services/` — service layer (e.g., `chat_agent.py`).
- `app/utils/` — helpers such as auth/logging utilities.
- `app/models/` — request/response schemas.
- `app/memory/` — memory-related modules.
- `pyproject.toml` — Poetry project metadata.
- `Dockerfile` — container build placeholder.

### Requirements
- Python 3.13+
- Poetry >= 2.0

### Setup
```bash
poetry install
```

### Running
The application entry point is not yet defined. Once `app/main.py` is implemented, you can run it via:
```bash
poetry run python -m app.main
```

### Development notes
- Populate the empty modules with concrete implementations before use.
- Add dependencies to `pyproject.toml` via `poetry add <package>`.
- If containerizing, complete the `Dockerfile` with build/run instructions tailored to the finalized app.

