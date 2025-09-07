## Airflow 3.0 on Docker with Playwright

Run Apache Airflow 3.0.x with CeleryExecutor on Docker (Postgres + Redis) and execute a Playwright-based crawler from a DAG.

[English](README.md) | [Русский](README.ru.md)

> OS: UNIX-like only (Linux/macOS/WSL2). These instructions target UNIX systems. On Windows, use WSL2.

### Features
- Airflow 3.0.6 (Python 3.12), CeleryExecutor
- Postgres + Redis, healthchecks, API server enabled
- Playwright 1.55.0 (Chromium; browsers installed in image)
- Example crawler (`crawlers/playwright/my_crawler`) + example DAG (`playwright_crawler`)
- Makefile for build/up/down/clean/sync
- `uv` for fast, reproducible dependency management
- `ruff` as linter (configured in `ruff.toml`)

### Prerequisites (UNIX)
- Docker and Docker Compose (v2)
- Make (install via your package manager, e.g. Ubuntu: `sudo apt-get install make`)
- uv (recommended locally if you run dev tools):
  - `pipx install uv` (preferred), or
  - `pip install uv`, or follow uv docs

### Quick start
1) Create `.env` from the template (required; without it the stack will NOT start):
```bash
cp env_sample .env
# update AIRFLOW_USER, AIRFLOW_PASSWORD, AIRFLOW_EMAIL, AIRFLOW_PORT as needed
```
2) Build images and prepare volumes:
```bash
make build
```
3) Start the stack:
```bash
make up
```
4) Open Airflow UI at `http://localhost:8080`  
   Sign in with credentials from `.env` (defaults: admin/admin).
5) Trigger the DAG:
   - DAG ID: `playwright_crawler`
   - Unpause it and click “Trigger DAG” to run the Playwright crawler.

Stop:
```bash
make down
```
Full cleanup (containers, images, volumes, data):
```bash
make clean
```

### Available Make targets
- `make build`: create local data dirs and build Docker image(s) with uv + Playwright browsers.
- `make up`: start the full Airflow stack in background; uses `.env` for initial admin user and port.
- `make down`: stop the stack (containers only).
- `make clean`: stop and remove containers, images, volumes and `data/` directory.
- `make sync`: install project dependencies locally via uv (all groups) and install Playwright Chromium.
- `make lint`: run ruff static checks for `crawlers`, `dags`, `operators`.

### Project structure
```
.
├─ dags/
│  └─ playwright_crawler_dag.py         # imports and runs the crawler module
├─ crawlers/
│  ├─ base/const.py                      # logging config
│  └─ playwright/my_crawler/main.py     # example Playwright crawler
├─ operators/                            # placeholder for custom operators
├─ .docker/
│  ├─ Dockerfile                         # installs uv + deps + Playwright browsers
│  └─ docker-compose.yaml                # Airflow + Postgres + Redis services
├─ Makefile                              # build/up/down/clean/sync/lint targets
├─ env_sample                            # .env template (copy to .env)
├─ pyproject.toml                        # deps and groups (airflow/lint/test)
├─ ruff.toml                             # linter configuration
└─ uv.lock
```

### How it works
- The DAG `playwright_crawler` imports `crawlers.playwright.my_crawler.main` and runs `main()`.
- The crawler launches headless Chromium via Playwright, iterates dummy pages (1..9), logs progress, and exits.

### Development (local)
Install dependencies and Playwright browsers locally:
```bash
make sync
```
Run the crawler directly:
```bash
uv run python crawlers/playwright/my_crawler/main.py
```
Lint:
```bash
make lint
```

### Configuration
- `.env` is mandatory: sets admin credentials and UI port.
- Volumes mount `dags/`, `crawlers/`, `operators/`, and `data/*` into containers.
- The image installs dependencies with `uv` and Playwright browsers at build time.

### Troubleshooting
- Resource checks: the init step warns if RAM/CPU/disk are low (needs ≥4GB RAM and ≥2 vCPU).
- Playwright browsers: bundled in the Docker image; for local runs use `make sync`.
- Linux file permissions: `AIRFLOW_UID` is auto-detected to avoid root-owned files.

### License
MIT
