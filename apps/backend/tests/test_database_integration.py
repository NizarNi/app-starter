from pathlib import Path
from uuid import uuid4

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import inspect, text
from sqlalchemy.schema import CreateSchema

from app.core.database import create_database_engine, database_is_ready

pytestmark = pytest.mark.integration


def test_backend_connects_to_postgresql_and_executes_query() -> None:
    assert database_is_ready()


def test_empty_baseline_migration_is_repeatable_and_creates_only_version_table() -> (
    None
):
    config = Config(str(Path(__file__).resolve().parents[1] / "alembic.ini"))
    engine = create_database_engine()
    schema_name = f"test_baseline_{uuid4().hex}"

    try:
        with engine.connect() as connection:
            transaction = connection.begin()
            try:
                # PostgreSQL transactional DDL removes this isolated schema on rollback.
                connection.execute(CreateSchema(schema_name))
                connection.execute(
                    text("SELECT set_config('search_path', :schema, true)"),
                    {"schema": schema_name},
                )
                config.attributes["connection"] = connection

                command.upgrade(config, "head")
                command.upgrade(config, "head")

                assert inspect(connection).get_table_names(schema=schema_name) == [
                    "alembic_version"
                ]
                assert (
                    connection.scalar(text("SELECT version_num FROM alembic_version"))
                    == "0001_baseline"
                )
            finally:
                transaction.rollback()
    finally:
        engine.dispose()
