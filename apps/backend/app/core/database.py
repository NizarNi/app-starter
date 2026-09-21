"""Minimal PostgreSQL connectivity shared by the application and migrations."""

from sqlalchemy import URL, Engine, create_engine, text
from sqlalchemy.pool import NullPool

from app.core.config import get_settings


def get_database_url() -> URL:
    """Build a URL safely, including passwords containing reserved characters."""

    settings = get_settings()
    return URL.create(
        "postgresql+psycopg",
        username=settings.database_user,
        password=settings.database_password,
        host=settings.database_host,
        port=settings.database_port,
        database=settings.database_name,
    )


def create_database_engine() -> Engine:
    """Open short-lived connections with bounded connection and query waits."""

    return create_engine(
        get_database_url(),
        poolclass=NullPool,
        connect_args={
            "connect_timeout": 2,
            "options": "-c statement_timeout=2000",
        },
    )


def database_is_ready() -> bool:
    """Verify that PostgreSQL accepts a connection and executes a basic query."""

    engine = create_database_engine()
    try:
        with engine.connect() as connection:
            return connection.scalar(text("SELECT 1")) == 1
    finally:
        engine.dispose()
