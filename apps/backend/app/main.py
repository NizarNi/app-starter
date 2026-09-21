"""FastAPI entry point for the App Starter backend."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import get_settings
from app.core.database import database_is_ready


class HealthResponse(BaseModel):
    """Public response from the service health endpoint."""

    status: str
    service: str


settings = get_settings()
app = FastAPI(title=settings.app_name)


@app.get("/health", response_model=HealthResponse, tags=["health"])
def health() -> HealthResponse:
    """Return a lightweight liveness response for local infrastructure."""

    return HealthResponse(status="ok", service="backend")


@app.get("/ready", response_model=HealthResponse, tags=["health"])
def ready() -> HealthResponse:
    """Check database readiness separately from application liveness."""

    try:
        database_ready = database_is_ready()
    except SQLAlchemyError:
        database_ready = False

    if not database_ready:
        raise HTTPException(status_code=503, detail="Database unavailable")

    return HealthResponse(status="ready", service="backend")
