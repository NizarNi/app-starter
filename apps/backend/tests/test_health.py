from fastapi.testclient import TestClient
from pytest import MonkeyPatch

from app.main import app


def test_health_endpoint_returns_successful_status(monkeypatch: MonkeyPatch) -> None:
    def unexpected_database_check() -> bool:
        raise AssertionError("Liveness must not depend on PostgreSQL")

    monkeypatch.setattr("app.main.database_is_ready", unexpected_database_check)
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "backend"}
