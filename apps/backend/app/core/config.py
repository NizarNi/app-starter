"""Environment-backed configuration for the backend skeleton."""

from dataclasses import dataclass, field
from os import getenv


@dataclass(frozen=True)
class Settings:
    """Configuration values supplied by the runtime environment."""

    app_name: str
    database_host: str
    database_port: int
    database_name: str
    database_user: str
    database_password: str | None = field(default=None, repr=False)


def get_settings() -> Settings:
    """Read settings without embedding deployment-specific credentials."""

    return Settings(
        app_name=getenv("APP_NAME", "App Starter API"),
        database_host=getenv("DATABASE_HOST", "db"),
        database_port=int(getenv("DATABASE_PORT", "5432")),
        database_name=getenv("POSTGRES_DB", "app_starter"),
        database_user=getenv("POSTGRES_USER", "app_starter"),
        database_password=getenv("POSTGRES_PASSWORD") or None,
    )
