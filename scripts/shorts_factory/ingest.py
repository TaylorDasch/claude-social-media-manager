"""Local master ingest using a reference/symlink instead of a media copy."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

from .errors import CommandError, ManifestError
from .state import PROCESSING
from .storage import (
    JOB_SCHEMA_VERSION,
    atomic_write_json,
    read_json,
    sha256_file,
    slugify,
    utc_now,
)


SUPPORTED_EXTENSIONS = {
    ".mp4",
    ".mov",
    ".m4v",
    ".mkv",
    ".webm",
    ".avi",
}


def _require_command(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise CommandError(f"required command is not on PATH: {name}")
    return path


def _run(command: list[str], *, label: str) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout or "").strip()[-1200:]
        raise CommandError(f"{label} failed ({exc.returncode}): {detail}") from exc


def ffprobe(path: Path) -> dict[str, Any]:
    command = [
        _require_command("ffprobe"),
        "-v",
        "error",
        "-show_format",
        "-show_streams",
        "-print_format",
        "json",
        str(path),
    ]
    result = _run(command, label="ffprobe")
    try:
        value = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise CommandError(f"ffprobe returned invalid JSON: {exc}") from exc
    if not isinstance(value, dict) or not isinstance(value.get("streams"), list):
        raise CommandError("ffprobe returned no stream metadata")
    return value


def _number(value: Any, *, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def summarize_probe(probe: dict[str, Any]) -> dict[str, Any]:
    streams = probe.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), {})
    audio = next((s for s in streams if s.get("codec_type") == "audio"), {})
    format_info = probe.get("format", {})
    duration = _number(format_info.get("duration")) or _number(video.get("duration"))
    return {
        "duration_s": round(duration, 3),
        "format_name": format_info.get("format_name"),
        "bit_rate": int(_number(format_info.get("bit_rate"))),
        "video": {
            "codec": video.get("codec_name"),
            "width": int(_number(video.get("width"))),
            "height": int(_number(video.get("height"))),
            "pixel_format": video.get("pix_fmt"),
            "frame_rate": video.get("avg_frame_rate"),
            "rotation": (video.get("tags") or {}).get("rotate"),
        },
        "audio": {
            "codec": audio.get("codec_name"),
            "sample_rate": int(_number(audio.get("sample_rate"))),
            "channels": int(_number(audio.get("channels"))),
        },
    }


def create_reference(source: Path, destination: Path) -> tuple[Path, str]:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() or destination.is_symlink():
        if destination.is_symlink() and destination.resolve() == source:
            return destination, "symlink"
        raise ManifestError(f"refusing to replace existing source reference: {destination}")
    try:
        destination.symlink_to(source)
        return destination, "symlink"
    except OSError:
        # A direct absolute reference still satisfies local ingest without copying.
        return source, "direct"


def extract_audio(source: Path, destination: Path, *, force: bool = False) -> Path:
    """Extract a 16 kHz mono PCM WAV with an atomic final rename."""
    if destination.exists() and destination.stat().st_size > 44 and not force:
        return destination
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(f".{destination.stem}.tmp{destination.suffix}")
    if temporary.exists():
        temporary.unlink()
    command = [
        _require_command("ffmpeg"),
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-i",
        str(source),
        "-map",
        "0:a:0",
        "-vn",
        "-ac",
        "1",
        "-ar",
        "16000",
        "-c:a",
        "pcm_s16le",
        str(temporary),
    ]
    try:
        _run(command, label="audio extraction")
        if not temporary.exists() or temporary.stat().st_size <= 44:
            raise CommandError("audio extraction produced an empty WAV")
        os.replace(temporary, destination)
    finally:
        if temporary.exists():
            temporary.unlink()
    return destination


def ingest_local(
    source: str | Path,
    output_root: Path,
    *,
    title: str | None = None,
    source_kind: str = "youtube_long",
    force_audio: bool = False,
) -> tuple[Path, dict[str, Any]]:
    """Create `<root>/jobs/<job_id>/job.json` and return its path + payload."""
    original = Path(source).expanduser().resolve()
    if not original.is_file():
        raise FileNotFoundError(f"local master not found: {original}")
    if original.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ManifestError(
            f"unsupported video extension {original.suffix!r}; "
            f"expected one of {sorted(SUPPORTED_EXTENSIONS)}"
        )

    source_hash = sha256_file(original)
    display_title = (title or original.stem).strip()
    job_id = f"{slugify(display_title)}-{source_hash[:12]}"
    job_dir = output_root.expanduser().resolve() / "jobs" / job_id
    job_path = job_dir / "job.json"

    if job_path.exists():
        existing = read_json(job_path)
        if existing.get("schema_version") != JOB_SCHEMA_VERSION:
            raise ManifestError(
                f"existing job has unsupported schema: {existing.get('schema_version')}"
            )
        if (existing.get("source") or {}).get("sha256") != source_hash:
            raise ManifestError(f"job id collision at {job_path}")
        return job_path, existing

    source_dir = job_dir / "source"
    artifacts_dir = job_dir / "artifacts"
    source_dir.mkdir(parents=True, exist_ok=True)
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    reference, reference_type = create_reference(
        original, source_dir / f"master{original.suffix.lower()}"
    )
    probe = ffprobe(original)
    atomic_write_json(source_dir / "ffprobe.json", probe)
    audio_path = extract_audio(reference, artifacts_dir / "audio.wav", force=force_audio)
    audio_hash = sha256_file(audio_path)
    stat = original.stat()
    now = utc_now()
    job: dict[str, Any] = {
        "schema_version": JOB_SCHEMA_VERSION,
        "revision": 1,
        "job_id": job_id,
        "title": display_title,
        "status": PROCESSING,
        "created_at": now,
        "updated_at": now,
        "source_kind": source_kind,
        "source": {
            "path": str(original),
            "reference_path": str(reference),
            "reference_type": reference_type,
            "sha256": source_hash,
            "size_bytes": stat.st_size,
            "mtime_ns": stat.st_mtime_ns,
            "probe": summarize_probe(probe),
            "probe_path": str(source_dir / "ffprobe.json"),
        },
        "audio": {
            "path": str(audio_path),
            "sha256": audio_hash,
            "sample_rate": 16000,
            "channels": 1,
        },
        "analysis": None,
        "clips": [],
        "warnings": [],
        "error": None,
        "history": [
            {
                "at": now,
                "event": "ingested",
                "to": PROCESSING,
                "source_path": str(original),
            }
        ],
    }
    atomic_write_json(job_path, job)
    return job_path, job
