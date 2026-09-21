"""Run migrations with the same PostgreSQL configuration as the backend."""

from alembic import context

from app.core.database import create_database_engine, get_database_url


def run_migrations_offline() -> None:
    context.configure(
        url=get_database_url(),
        target_metadata=None,
        literal_binds=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    # Tests can supply an existing transaction to isolate migration validation.
    connection = context.config.attributes.get("connection")
    if connection is not None:
        context.configure(connection=connection, target_metadata=None)
        with context.begin_transaction():
            context.run_migrations()
        return

    engine = create_database_engine()
    try:
        with engine.connect() as connection:
            context.configure(connection=connection, target_metadata=None)
            with context.begin_transaction():
                context.run_migrations()
    finally:
        engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
