from pytest import MonkeyPatch

from app.core.config import get_settings
from app.core.database import get_database_url


def test_database_url_uses_environment_and_preserves_password(
    monkeypatch: MonkeyPatch,
) -> None:
    password = "test-only-@:/?#%"
    monkeypatch.setenv("DATABASE_HOST", "test-db")
    monkeypatch.setenv("DATABASE_PORT", "5433")
    monkeypatch.setenv("POSTGRES_DB", "test_database")
    monkeypatch.setenv("POSTGRES_USER", "test_user")
    monkeypatch.setenv("POSTGRES_PASSWORD", password)

    url = get_database_url()

    assert url.drivername == "postgresql+psycopg"
    assert url.host == "test-db"
    assert url.port == 5433
    assert url.database == "test_database"
    assert url.username == "test_user"
    assert url.password == password
    assert password not in repr(get_settings())
    assert password not in str(url)


def test_database_password_is_optional_for_local_development(
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.delenv("POSTGRES_PASSWORD", raising=False)

    assert get_database_url().password is None
