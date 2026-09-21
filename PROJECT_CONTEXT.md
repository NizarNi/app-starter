# Technical Project Context

This repository is a product-agnostic application foundation.

## Stack

- Frontend: TypeScript, React and Next.js.
- Backend: Python and FastAPI.
- Database: PostgreSQL, SQLAlchemy connectivity and Alembic migrations.
- Local environment: Docker Compose.
- CI: GitHub Actions.
- Tests: pytest for the backend and Vitest for the frontend; Compose integration and smoke checks.

## Current implementation

The frontend displays backend connection status. The backend exposes `/health` for liveness and `/ready` for database readiness. The initial migration creates no application tables.

## Development

Read `README.md` for setup and validation commands, `AGENTS.md` for development conventions, and `docs/07_Technical_Architecture.md` for architecture. Keep changes scoped and use reviewed branches.
