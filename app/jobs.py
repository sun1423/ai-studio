import json
import shutil
from pathlib import Path
from typing import Any

from app.config import get_settings
from app.db import connection

ALLOWED_KINDS = {"content.generate", "content.publish", "voice.create_profile", "voice.preview"}


def enqueue(kind: str, payload: dict[str, Any]) -> int:
    if kind not in ALLOWED_KINDS:
        raise ValueError(f"Unsupported job type: {kind}")
    with connection() as conn:
        cursor = conn.execute(
            "INSERT INTO jobs(kind, payload_json) VALUES (?, ?)",
            (kind, json.dumps(payload)),
        )
        return int(cursor.lastrowid)


def list_jobs(limit: int = 50) -> list[dict[str, Any]]:
    with connection() as conn:
        rows = conn.execute(
            "SELECT id, kind, payload_json, status, error, result_json, created_at, started_at, finished_at "
            "FROM jobs ORDER BY id DESC LIMIT ?",
            (max(1, min(limit, 200)),),
        ).fetchall()
    return [dict(row) for row in rows]


def check_upload_capacity(file_size: int) -> None:
    settings = get_settings()
    if file_size > settings.max_upload_mb * 1024 * 1024:
        raise ValueError(f"Upload exceeds {settings.max_upload_mb} MB limit")
    free_bytes = shutil.disk_usage(settings.data_dir).free
    required = settings.min_free_disk_gb * 1024**3
    if free_bytes - file_size < required:
        raise ValueError("Not enough free disk space for this upload")


def safe_filename(name: str) -> str:
    return Path(name).name.replace("/", "_").replace("\\", "_")[:160] or "upload.bin"
