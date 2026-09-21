# Technical Architecture

## Structure

A containerized modular monolith with a separate Next.js frontend, FastAPI REST API and PostgreSQL database. Backend modules remain in one deployable service.

- `apps/frontend`: TypeScript, React and Next.js application.
- `apps/backend`: Python API, database configuration, migrations and tests.
- `scripts/smoke.py`: running-stack checks.
- `.github/workflows/ci.yml`: automated validation.

## Request flow

The browser loads the frontend. Its server fetches API liveness with a two-second deadline. The API uses SQLAlchemy for PostgreSQL connectivity. `/health` checks liveness; `/ready` checks the database and returns HTTP 503 when unavailable.

## Database

One PostgreSQL database. Alembic applies migrations before the API starts. The baseline migration is empty; only Alembic bookkeeping exists. Future schema changes belong in reviewed migrations.

## Local environment

Docker Compose runs frontend, backend and database services. Application ports bind to localhost and the database has no published host port. Source is copied into images, so changes require rebuilding. See `README.md` for commands and development-only database authentication details.

## Validation

GitHub Actions runs backend Ruff checks and pytest unit tests, frontend ESLint, Vitest, TypeScript checks and production build, plus Compose integration and smoke checks. No deployment job is configured.

## Engineering conventions

Keep API and UI responsibilities separate. Use explicit module interfaces and avoid unnecessary dependencies or distributed infrastructure. Keep secrets outside source control and configuration in environment variables. Choose deployment infrastructure when a concrete hosting requirement exists.
