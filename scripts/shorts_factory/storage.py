"""Atomic JSON storage and canonical job-path resolution."""

from __future__ import annotations

import fcntl
import hashlib
import json
import os
import re
import tempfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterator, TypeVar

from .errors import ManifestError, RevisionConflict


DEFAULT_ROOT = Path.home() / "claude-video" / "shorts-factory"
JOB_SCHEMA_VERSION = "shorts-job/v1"
CLIP_SCHEMA_VERSION = "shorts-clip/v1"

T = TypeVar("T")
SAFE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def slugify(value: str, *, max_length: int = 64) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value[:max_length].strip("-") or "video"


def validate_safe_id(value: object, *, label: str = "id") -> str:
    text = str(value)
    if not SAFE_ID_RE.fullmatch(text):
        raise ManifestError(f"unsafe {label}: {text!r}")
    return text


def sha256_file(path: Path, *, chunk_size: int = 8 * 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ManifestError(f"manifest not found: {path}") from exc
    except (OSError, json.JSONDecodeError) as exc:
        raise ManifestError(f"could not read JSON at {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ManifestError(f"expected a JSON object at {path}")
    return value


def atomic_write_json(path: Path, value: Any) -> None:
    """Write JSON with fsync + same-directory replace."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(value, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def resolve_job_path(root: Path, job: str | Path) -> Path:
    candidate = Path(job).expanduser()
    if candidate.name == "job.json" and candidate.exists():
        return candidate.resolve()
    if candidate.is_dir() and (candidate / "job.json").exists():
        return (candidate / "job.json").resolve()
    job_id = validate_safe_id(job, label="job id")
    jobs_root = root.expanduser().resolve() / "jobs"
    path = jobs_root / job_id / "job.json"
    if not path.exists():
        raise ManifestError(f"job not found: {job} (looked at {path})")
    try:
        real_jobs_root = jobs_root.resolve(strict=True)
        resolved = path.resolve(strict=True)
        resolved.relative_to(real_jobs_root)
    except (FileNotFoundError, ValueError) as exc:
        raise ManifestError(f"job path escapes the factory jobs root: {job_id}") from exc
    return resolved


@contextmanager
def manifest_lock(job_path: Path) -> Iterator[None]:
    """Serialize local readers/writers while still using revision checks."""
    lock_path = job_path.with_suffix(job_path.suffix + ".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+", encoding="utf-8") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock.fileno(), fcntl.LOCK_UN)


def update_job(
    job_path: Path,
    *,
    expected_revision: int | None,
    mutate: Callable[[dict[str, Any]], T],
) -> tuple[dict[str, Any], T]:
    """Atomically mutate canonical job.json with optimistic concurrency."""
    with manifest_lock(job_path):
        job = read_json(job_path)
        current = job.get("revision")
        if not isinstance(current, int) or current < 1:
            raise ManifestError(f"invalid revision in {job_path}: {current!r}")
        if expected_revision is not None and expected_revision != current:
            raise RevisionConflict(
                f"revision conflict for {job.get('job_id', job_path.parent.name)}: "
                f"expected {expected_revision}, current {current}"
            )
        result = mutate(job)
        job["revision"] = current + 1
        job["updated_at"] = utc_now()
        atomic_write_json(job_path, job)
        return job, result


def write_clip_manifests(job_path: Path, job: dict[str, Any]) -> None:
    """Mirror embedded clips; job.json remains the canonical source of truth."""
    job_id = str(job["job_id"])
    validate_safe_id(job_id, label="job id")
    for clip in job.get("clips", []):
        clip_id = validate_safe_id(clip["id"], label="clip id")
        payload = {
            "schema_version": CLIP_SCHEMA_VERSION,
            "job_id": job_id,
            **clip,
        }
        atomic_write_json(job_path.parent / "clips" / clip_id / "clip.json", payload)
