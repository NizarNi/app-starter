import pytest
from fastapi.testclient import TestClient
from pytest import MonkeyPatch
from sqlalchemy.exc import OperationalError

from app.main import app


def test_readiness_succeeds_when_database_is_available(
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.setattr("app.main.database_is_ready", lambda: True)

    response = TestClient(app).get("/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready", "service": "backend"}


@pytest.mark.parametrize("database_error", [False, True])
def test_readiness_returns_safe_failure(
    monkeypatch: MonkeyPatch, database_error: bool
) -> None:
    def failed_database_check() -> bool:
        if database_error:
            raise OperationalError("SELECT 1", {}, Exception("private connection data"))
        return False

    monkeypatch.setattr("app.main.database_is_ready", failed_database_check)

    response = TestClient(app).get("/ready")

    assert response.status_code == 503
    assert response.json() == {"detail": "Database unavailable"}

    liveness = TestClient(app).get("/health")
    assert liveness.status_code == 200
    assert liveness.json() == {"status": "ok", "service": "backend"}
