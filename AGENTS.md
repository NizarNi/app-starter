# App Starter Agent Instructions

## Project Context

Before making changes, read:

1. `PROJECT_CONTEXT.md`
2. The relevant documents under `docs/`
3. `docs/07_Technical_Architecture.md` for technical decisions

These documents describe the technical foundation. No product requirements are defined.

## Scope Rules

Implement the requested task without inventing product requirements or business rules.
Ask for a decision when missing requirements block implementation.

## Architecture Rules

Use a modular monolith for the application.

Do not introduce microservices unless explicitly approved.

Use Docker for the local development environment.

Keep application source code inside the WSL Linux filesystem.

Backend: Python.

Frontend: TypeScript.

Database: PostgreSQL.

Use an API-first separation between frontend and backend so future mobile clients can use the same backend.

Avoid unnecessary infrastructure and dependencies.

Do not introduce Kubernetes, Kafka, event buses or other distributed-system infrastructure unless an explicit requirement is established.

## Development Workflow

Never develop directly on `main`.

Each meaningful change must use a dedicated branch.

Branch naming:

* `feature/<name>` for functionality
* `fix/<name>` for bug fixes
* `chore/<name>` for tooling or maintenance
* `docs/<name>` for documentation changes

Keep branches focused and short-lived.

Do not mix unrelated changes in the same branch.

The normal workflow is:

1. Start from the latest `main`.
2. Create a feature/fix/chore/docs branch.
3. Implement the requested change.
4. Add or update tests.
5. Run the relevant tests.
6. Review the diff.
7. Commit the change.
8. Push the branch.
9. Open a pull request to `main`.
10. The Product Owner reviews and validates it.
11. Merge only after acceptance.

## Commit Convention

Use clear conventional-style commit messages.

Examples:

* `feat: add API endpoint`
* `fix: handle connection timeout`
* `chore: configure docker compose`
* `test: add API response coverage`
* `docs: update development workflow`

Use signed-off commits with:

`git commit -s`

## Testing

Every meaningful feature must include appropriate automated tests.

At minimum, consider:

* Unit tests for business logic
* API/integration tests for backend behavior
* End-to-end tests for important user journeys

Do not claim a feature is complete without running the relevant tests.

Do not weaken or delete tests merely to make the test suite pass.

## Code Quality

Prefer simple, readable and maintainable code.

Avoid premature abstraction.

Avoid duplicated business logic.

Keep modules focused.

Use explicit types where appropriate.

Handle errors explicitly.

Do not introduce a framework or dependency without a clear reason.

## Security

Never commit secrets, tokens, passwords or private keys.

Use environment variables for configuration and secrets.

Keep `.env` files out of Git.

Update `.env.example` when a new required environment variable is introduced.

Do not expose sensitive information in logs or API responses.

## Scope Control

Implement only what the current user story requires.

Do not redesign unrelated parts of the application.

Do not modify product documentation to justify an implementation decision.

If the existing architecture or requirements appear inconsistent, report the inconsistency before making a broad change.

## Codex Behavior

Before coding:

* Inspect the repository.
* Read the relevant documentation.
* Identify the files likely to change.
* Explain any important implementation assumption.

While coding:

* Keep changes scoped.
* Prefer existing project conventions.
* Add tests with the implementation.

Before finishing:

* Run relevant tests.
* Check formatting/linting where configured.
* Review the Git diff.
* Summarize changed files and validation performed.

Do not merge pull requests or make product decisions on behalf of the Product Owner.
