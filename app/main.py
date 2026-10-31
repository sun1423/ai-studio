import secrets
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field

from app.config import get_settings
from app.db import initialise_database
from app.jobs import enqueue, list_jobs

settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.1.0")
basic_auth = HTTPBasic()


def require_login(credentials: HTTPBasicCredentials = Depends(basic_auth)) -> str:
    username_ok = secrets.compare_digest(credentials.username, settings.app_username)
    password_ok = bool(settings.app_password) and secrets.compare_digest(
        credentials.password, settings.app_password
    )
    if not (username_ok and password_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


class JobRequest(BaseModel):
    kind: str
    payload: dict[str, Any] = Field(default_factory=dict)


@app.on_event("startup")
def startup() -> None:
    initialise_database()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "app": settings.app_name}


@app.get("/")
def dashboard(_: str = Depends(require_login)) -> dict[str, str]:
    return {
        "app": settings.app_name,
        "status": "foundation",
        "message": "Dashboard API is protected. Content and voice runners are added in the next step.",
        "jobs_endpoint": "/api/jobs",
    }


@app.get("/api/jobs")
def get_jobs(_: str = Depends(require_login)) -> dict[str, list[dict[str, Any]]]:
    return {"jobs": list_jobs()}


@app.post("/api/jobs", status_code=status.HTTP_202_ACCEPTED)
def create_job(request: JobRequest, _: str = Depends(require_login)) -> dict[str, Any]:
    try:
        job_id = enqueue(request.kind, request.payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"id": job_id, "status": "queued", "kind": request.kind}
