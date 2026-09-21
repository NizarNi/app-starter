# App Starter

A product-agnostic development foundation with a Next.js frontend, FastAPI REST API, PostgreSQL connectivity, and an empty Alembic migration baseline.

## Prerequisites

- Docker Engine with Docker Compose v2.20+ (including `up --wait`)
- Keep the repository and application source in the **WSL Linux filesystem**, for example `/home/<user>/projects/app-starter`, rather than a Windows-mounted directory such as `/mnt/c/...`.
- No host Python or Node installation is needed for the container commands below. For tools outside containers, the supported frontend runtime is **Node.js 22.12.0 or later within 22.x** (matching Docker and CI); the backend is tested with Python 3.12.

## Run locally

From the repository root:

```bash
docker compose up --build
```

Then open [http://localhost:3000](http://localhost:3000). Published frontend/backend ports bind to `127.0.0.1` only. PostgreSQL has no published host port.

The frontend fetches backend health on the server with a two-second deadline, including response-body reading, and displays an unavailable status if the request fails. `BACKEND_URL` is a server-side environment variable; it uses the Compose service name `backend` by default.

- [GET /health](http://localhost:8000/health) checks application liveness only; it does not contact PostgreSQL.
- [GET /ready](http://localhost:8000/ready) executes `SELECT 1` using the backend database connection and returns HTTP 503 if PostgreSQL is unavailable. Compose uses this endpoint for backend readiness.
- The frontend health check requests the actual landing page. The smoke check below also verifies that the page reports a successful backend connection.

The Compose stack uses non-secret defaults and reads optional overrides from a root `.env` file based on `.env.example`. No `.env` file is required or committed. The backend and migrations share `DATABASE_HOST`, `DATABASE_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, and optional `POSTGRES_PASSWORD` configuration.

**PostgreSQL `trust` authentication is exclusively for this local, disposable development environment. It must not be used in shared, staging, or production environments.** Those environments require a separate database configuration with password-based authentication and externally supplied credentials. Setting `POSTGRES_PASSWORD` alone does not disable the local Compose file's `trust` mode.

## Source changes and migrations

Source is copied into images; there are no source bind mounts or automatic reload. After editing frontend/backend code, migration files, or dependencies, rebuild and recreate the services:

```bash
docker compose up --build --wait --wait-timeout 120
```

This runs in the background and waits for service health checks. A plain `docker compose restart` does not rebuild source changes. Inspect logs with `docker compose logs -f`.

The backend runs `alembic upgrade head` before starting FastAPI. The initial migration is empty: it creates no domain tables; Alembic creates only its `alembic_version` bookkeeping table. Applying the same migration again is safe. To inspect or explicitly apply migrations while the stack is running:

```bash
docker compose exec backend alembic current
docker compose exec backend alembic upgrade head
```

Future schema changes belong in reviewed Alembic revisions under `apps/backend/migrations/versions/`.

To stop the stack:

```bash
docker compose down
```

To discard the disposable local database as well (this deletes its data):

```bash
docker compose down --volumes
```

## Tests and validation

From the repository root, build and start the stack first as above. Unit checks use one-off containers; the database integration test uses the running backend's connection configuration:

```bash
docker compose run --rm --no-deps backend pytest -m 'not integration'
docker compose exec -T backend pytest -m integration
docker compose run --rm --no-deps backend ruff check .
docker compose run --rm --no-deps backend ruff format --check .
docker compose run --rm --no-deps frontend npm run test:run
docker compose run --rm --no-deps frontend npm run lint
docker compose run --rm --no-deps frontend npm run typecheck
docker compose run --rm --no-deps frontend npm run build
```

The integration marker selects real PostgreSQL tests: connection failures fail the test rather than silently skipping it. The baseline test runs migrations twice in a temporary, transaction-isolated schema, checks Alembic state and the absence of application tables, then rolls back its test schema.

The same checks can run directly from `apps/backend` after installing `requirements.txt` in a Python virtual environment, and from `apps/frontend` after `npm ci`. Backend unit tests need no database. Native database checks require the database environment variables to point at a reachable disposable PostgreSQL instance and `alembic upgrade head` to have run; the local Compose database deliberately has no host port.

Validate the Compose configuration and the running stack's published endpoints (the latter uses host Python 3.12, or the Python provided on WSL):

```bash
docker compose config --quiet
python3 scripts/smoke.py
```

The smoke script verifies backend liveness, backend/PostgreSQL readiness, and the frontend's rendered backend status. GitHub Actions runs backend lint/format/unit tests, frontend lint/tests/type checks/production build, and a separate Compose build/start/integration/smoke job. There is no deployment job.


## Development workflow

Do not commit directly to `main`. Start a focused `feature/`, `fix/`, `chore/`, or `docs/` branch from the latest `main`; add tests, run the relevant checks, review the diff, then create a signed-off conventional commit. Push the branch and open a pull request for Product Owner review. Do not merge without acceptance.

Technical context is defined in `PROJECT_CONTEXT.md` and `docs/07_Technical_Architecture.md`.
