"""Source-bound vertical graphic replacement manifests and render evidence."""

from __future__ import annotations

import json
import math
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any, Mapping, Sequence

from .errors import ManifestError
from .storage import sha256_file, validate_safe_id


GRAPHICS_MANIFEST_VERSION = "shorts-visual-replacements/v1"
APPLIED_GRAPHICS_VERSION = "shorts-applied-graphics/v1"
GRAPHICS_WIDTH = 1080
GRAPHICS_HEIGHT = 1920
GRAPHICS_FPS = 30.0
TIMING_MODES = {"hold_last"}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def _fraction(value: object) -> float:
    text = str(value or "0")
    if "/" not in text:
        return float(text)
    numerator, denominator = text.split("/", 1)
    divisor = float(denominator)
    return 0.0 if divisor == 0 else float(numerator) / divisor


def _probe_asset(path: Path, *, ffprobe_path: str | None = None) -> dict[str, Any]:
    executable = ffprobe_path or shutil.which("ffprobe")
    if not executable:
        raise ManifestError("ffprobe is required to validate replacement graphics")
    try:
        result = subprocess.run(
            [
                executable,
                "-v",
                "error",
                "-show_entries",
                (
                    "stream=index,codec_type,codec_name,width,height,pix_fmt,avg_frame_rate:"
                    "format=duration"
                ),
                "-of",
                "json",
                str(path),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(result.stdout)
    except (OSError, subprocess.SubprocessError, json.JSONDecodeError) as exc:
        raise ManifestError(f"could not probe replacement graphic {path}: {exc}") from exc
    videos = [
        stream
        for stream in payload.get("streams", [])
        if stream.get("codec_type") == "video"
    ]
    if len(videos) != 1:
        raise ManifestError(
            f"replacement graphic must have one video stream, found {len(videos)}: {path}"
        )
    video = videos[0]
    try:
        info = {
            "duration_s": float(payload.get("format", {}).get("duration") or 0.0),
            "width": int(video.get("width") or 0),
            "height": int(video.get("height") or 0),
            "fps": round(_fraction(video.get("avg_frame_rate")), 6),
            "codec": str(video.get("codec_name") or ""),
            "pixel_format": str(video.get("pix_fmt") or ""),
        }
    except (TypeError, ValueError) as exc:
        raise ManifestError(f"replacement graphic has invalid media metadata: {path}") from exc
    if info["duration_s"] <= 0:
        raise ManifestError(f"replacement graphic has no positive duration: {path}")
    if (info["width"], info["height"]) != (GRAPHICS_WIDTH, GRAPHICS_HEIGHT):
        raise ManifestError(
            f"replacement graphic must be {GRAPHICS_WIDTH}x{GRAPHICS_HEIGHT}; "
            f"received {info['width']}x{info['height']}: {path}"
        )
    if abs(float(info["fps"]) - GRAPHICS_FPS) > 0.05:
        raise ManifestError(
            f"replacement graphic must be {GRAPHICS_FPS:.0f}fps; "
            f"received {info['fps']}: {path}"
        )
    if info["codec"] != "h264":
        raise ManifestError(
            f"replacement graphic codec must be h264; received {info['codec']!r}: {path}"
        )
    if info["pixel_format"] != "yuv420p":
        raise ManifestError(
            "replacement graphic pixel format must be yuv420p; "
            f"received {info['pixel_format']!r}: {path}"
        )
    return info


def _number(value: object, *, label: str) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ManifestError(f"{label} must be numeric") from exc
    if not math.isfinite(number):
        raise ManifestError(f"{label} must be finite")
    return number


def _resolve_asset_path(raw_path: object, manifest_path: Path) -> Path:
    if not isinstance(raw_path, str) or not raw_path.strip():
        raise ManifestError("replacement asset_path must be a non-empty string")
    candidate = Path(raw_path).expanduser()
    if not candidate.is_absolute():
        candidate = manifest_path.parent / candidate
    resolved = candidate.resolve()
    if not resolved.is_file():
        raise ManifestError(f"replacement graphic is missing: {resolved}")
    if resolved.suffix.lower() != ".mp4":
        raise ManifestError(f"replacement graphic must be an MP4: {resolved}")
    return resolved


def load_visual_replacements(
    manifest_path: str | Path,
    *,
    expected_source_sha256: str,
    source_duration_s: float | None = None,
    ffprobe_path: str | None = None,
) -> dict[str, Any]:
    """Load and fully validate a source-timeline replacement manifest."""
    path = Path(manifest_path).expanduser().resolve()
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ManifestError(f"visual replacement manifest not found: {path}") from exc
    except (OSError, json.JSONDecodeError) as exc:
        raise ManifestError(f"could not read visual replacement manifest {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ManifestError("visual replacement manifest must be a JSON object")
    if payload.get("schema_version") != GRAPHICS_MANIFEST_VERSION:
        raise ManifestError(
            "unsupported visual replacement schema: "
            f"{payload.get('schema_version')!r}"
        )
    expected_source = str(expected_source_sha256).lower()
    recorded_source = str(payload.get("source_sha256") or "").lower()
    if not SHA256_RE.fullmatch(expected_source):
        raise ManifestError("expected source SHA-256 is invalid")
    if recorded_source != expected_source:
        raise ManifestError(
            "visual replacement manifest is bound to a different source SHA-256"
        )
    raw_replacements = payload.get("replacements")
    if not isinstance(raw_replacements, list):
        raise ManifestError("visual replacement manifest replacements must be a list")

    validated: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for index, raw in enumerate(raw_replacements):
        if not isinstance(raw, dict):
            raise ManifestError(f"replacement {index + 1} must be an object")
        if not isinstance(raw.get("id"), str):
            raise ManifestError(f"replacement {index + 1} id must be a string")
        replacement_id = validate_safe_id(raw.get("id"), label="replacement id")
        if replacement_id in seen_ids:
            raise ManifestError(f"duplicate replacement id: {replacement_id}")
        seen_ids.add(replacement_id)
        start = _number(raw.get("source_start_s"), label=f"{replacement_id}.source_start_s")
        end = _number(raw.get("source_end_s"), label=f"{replacement_id}.source_end_s")
        if start < 0 or end <= start:
            raise ManifestError(
                f"replacement {replacement_id} requires 0 <= source_start_s < source_end_s"
            )
        if source_duration_s is not None and end > float(source_duration_s) + 0.05:
            raise ManifestError(
                f"replacement {replacement_id} ends beyond the source duration"
            )
        timing_mode = str(raw.get("timing_mode") or "hold_last")
        if timing_mode not in TIMING_MODES:
            raise ManifestError(
                f"replacement {replacement_id} has unsupported timing_mode {timing_mode!r}"
            )
        asset_path = _resolve_asset_path(raw.get("asset_path"), path)
        expected_asset_sha = str(raw.get("asset_sha256") or "").lower()
        if not SHA256_RE.fullmatch(expected_asset_sha):
            raise ManifestError(
                f"replacement {replacement_id} asset_sha256 must be a SHA-256 digest"
            )
        actual_asset_sha = sha256_file(asset_path)
        if actual_asset_sha != expected_asset_sha:
            raise ManifestError(
                f"replacement graphic checksum mismatch for {replacement_id}: {asset_path}"
            )
        asset = _probe_asset(asset_path, ffprobe_path=ffprobe_path)
        validated.append(
            {
                "id": replacement_id,
                "timeline_start_s": round(start, 6),
                "timeline_end_s": round(end, 6),
                "asset_path": str(asset_path),
                "asset_sha256": actual_asset_sha,
                "timing_mode": timing_mode,
                "asset": asset,
            }
        )

    validated.sort(key=lambda item: (item["timeline_start_s"], item["timeline_end_s"]))
    for left, right in zip(validated, validated[1:]):
        if float(right["timeline_start_s"]) < float(left["timeline_end_s"]) - 0.0005:
            raise ManifestError(
                f"visual replacement ranges overlap: {left['id']} and {right['id']}"
            )
    return {
        "schema_version": GRAPHICS_MANIFEST_VERSION,
        "manifest_path": str(path),
        "source_sha256": recorded_source,
        "replacements": validated,
    }


def replacements_for_clip(
    manifest: Mapping[str, Any],
    clip_start_s: float,
    clip_end_s: float,
) -> list[dict[str, Any]]:
    """Intersect an absolute source timeline with one selected clip span."""
    clip_start = float(clip_start_s)
    clip_end = float(clip_end_s)
    if clip_start < 0 or clip_end <= clip_start:
        raise ValueError("clip replacement span requires 0 <= start < end")
    result: list[dict[str, Any]] = []
    for raw in manifest.get("replacements") or []:
        if not isinstance(raw, Mapping):
            continue
        timeline_start = float(raw["timeline_start_s"])
        timeline_end = float(raw["timeline_end_s"])
        source_start = max(clip_start, timeline_start)
        source_end = min(clip_end, timeline_end)
        if source_end - source_start < 0.001:
            continue
        asset = dict(raw["asset"])
        result.append(
            {
                "id": str(raw["id"]),
                "timeline_start_s": timeline_start,
                "timeline_end_s": timeline_end,
                "source_start_s": round(source_start, 6),
                "source_end_s": round(source_end, 6),
                "clip_start_s": round(source_start - clip_start, 6),
                "clip_end_s": round(source_end - clip_start, 6),
                "asset_start_s": round(source_start - timeline_start, 6),
                "asset_path": str(raw["asset_path"]),
                "asset_sha256": str(raw["asset_sha256"]),
                "timing_mode": str(raw["timing_mode"]),
                "asset": asset,
            }
        )
    return result


def build_applied_graphics_plan(
    *,
    source_sha256: str | None,
    clip_start_s: float,
    clip_end_s: float,
    replacements: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    return {
        "schema_version": APPLIED_GRAPHICS_VERSION,
        "source_sha256": str(source_sha256 or ""),
        "clip_source_span": {
            "start_s": round(float(clip_start_s), 6),
            "end_s": round(float(clip_end_s), 6),
        },
        "replacement_count": len(replacements),
        "replacements": [dict(replacement) for replacement in replacements],
    }


def validate_applied_graphics_plan(path: str | Path) -> list[str]:
    """Revalidate load-bearing replacement evidence after media rendering."""
    plan_path = Path(path).expanduser().resolve()
    if not plan_path.is_file() or plan_path.stat().st_size == 0:
        return [f"graphics-plan sidecar missing or empty: {plan_path}"]
    try:
        payload = json.loads(plan_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"graphics-plan sidecar is invalid JSON: {exc}"]
    if not isinstance(payload, dict):
        return ["graphics-plan sidecar must be a JSON object"]
    errors: list[str] = []
    if payload.get("schema_version") != APPLIED_GRAPHICS_VERSION:
        errors.append("graphics-plan sidecar has an unsupported schema")
    source_sha = str(payload.get("source_sha256") or "").lower()
    if source_sha and not SHA256_RE.fullmatch(source_sha):
        errors.append("graphics-plan source_sha256 is invalid")
    span = payload.get("clip_source_span")
    if not isinstance(span, dict):
        return errors + ["graphics-plan clip_source_span is missing"]
    try:
        clip_start = float(span["start_s"])
        clip_end = float(span["end_s"])
    except (KeyError, TypeError, ValueError):
        return errors + ["graphics-plan clip_source_span is invalid"]
    if clip_start < 0 or clip_end <= clip_start:
        errors.append("graphics-plan clip_source_span is not positive")
    replacements = payload.get("replacements")
    if not isinstance(replacements, list):
        return errors + ["graphics-plan replacements must be a list"]
    if replacements and not SHA256_RE.fullmatch(source_sha):
        errors.append("graphics-plan with replacements requires source_sha256")
    if payload.get("replacement_count") != len(replacements):
        errors.append("graphics-plan replacement_count does not match replacements")
    prior_end = -1.0
    seen: set[str] = set()
    for index, raw in enumerate(replacements, start=1):
        if not isinstance(raw, dict):
            errors.append(f"graphics-plan replacement {index} is not an object")
            continue
        replacement_id = str(raw.get("id") or "")
        try:
            validate_safe_id(replacement_id, label="replacement id")
        except ManifestError as exc:
            errors.append(str(exc))
        if replacement_id in seen:
            errors.append(f"graphics-plan has duplicate replacement id {replacement_id!r}")
        seen.add(replacement_id)
        try:
            source_start = float(raw["source_start_s"])
            source_end = float(raw["source_end_s"])
            local_start = float(raw["clip_start_s"])
            local_end = float(raw["clip_end_s"])
            timeline_start = float(raw["timeline_start_s"])
            timeline_end = float(raw["timeline_end_s"])
            asset_start = float(raw["asset_start_s"])
        except (KeyError, TypeError, ValueError):
            errors.append(f"graphics-plan replacement {replacement_id!r} has invalid timing")
            continue
        timing_values = (
            source_start,
            source_end,
            local_start,
            local_end,
            timeline_start,
            timeline_end,
            asset_start,
        )
        if not all(math.isfinite(value) for value in timing_values):
            errors.append(
                f"graphics-plan replacement {replacement_id!r} has non-finite timing"
            )
            continue
        if local_start < -0.001 or local_end <= local_start:
            errors.append(f"graphics-plan replacement {replacement_id!r} has invalid clip timing")
        if local_end > clip_end - clip_start + 0.05:
            errors.append(f"graphics-plan replacement {replacement_id!r} exceeds the clip")
        if local_start < prior_end - 0.0005:
            errors.append("graphics-plan replacement ranges overlap")
        prior_end = max(prior_end, local_end)
        if abs(source_start - (clip_start + local_start)) > 0.002 or abs(
            source_end - (clip_start + local_end)
        ) > 0.002:
            errors.append(
                f"graphics-plan replacement {replacement_id!r} source/clip timing disagrees"
            )
        if not (
            timeline_start - 0.002 <= source_start < source_end <= timeline_end + 0.002
        ):
            errors.append(
                f"graphics-plan replacement {replacement_id!r} exceeds its timeline range"
            )
        if abs(asset_start - (source_start - timeline_start)) > 0.002:
            errors.append(
                f"graphics-plan replacement {replacement_id!r} asset timing disagrees"
            )
        if asset_start < -0.001 or asset_start + (local_end - local_start) > (
            timeline_end - timeline_start
        ) + 0.002:
            errors.append(
                f"graphics-plan replacement {replacement_id!r} asset span is invalid"
            )
        if str(raw.get("timing_mode")) not in TIMING_MODES:
            errors.append(
                f"graphics-plan replacement {replacement_id!r} has invalid timing_mode"
            )
        asset_path = Path(str(raw.get("asset_path") or "")).expanduser().resolve()
        expected_sha = str(raw.get("asset_sha256") or "").lower()
        if not asset_path.is_file():
            errors.append(f"graphics-plan replacement asset is missing: {asset_path}")
            continue
        if not SHA256_RE.fullmatch(expected_sha):
            errors.append(
                f"graphics-plan replacement {replacement_id!r} asset SHA-256 is invalid"
            )
            continue
        if sha256_file(asset_path) != expected_sha:
            errors.append(
                f"graphics-plan replacement {replacement_id!r} asset checksum changed"
            )
            continue
        recorded_asset = raw.get("asset")
        if not isinstance(recorded_asset, dict):
            errors.append(
                f"graphics-plan replacement {replacement_id!r} asset metadata is missing"
            )
            continue
        try:
            actual_asset = _probe_asset(asset_path)
        except ManifestError as exc:
            errors.append(str(exc))
            continue
        for key in ("width", "height", "codec", "pixel_format"):
            if recorded_asset.get(key) != actual_asset.get(key):
                errors.append(
                    f"graphics-plan replacement {replacement_id!r} recorded asset {key} changed"
                )
        for key in ("duration_s", "fps"):
            try:
                differs = abs(
                    float(recorded_asset.get(key)) - float(actual_asset.get(key))
                ) > 0.05
            except (TypeError, ValueError):
                differs = True
            if differs:
                errors.append(
                    f"graphics-plan replacement {replacement_id!r} recorded asset {key} changed"
                )
    return errors


__all__ = [
    "APPLIED_GRAPHICS_VERSION",
    "GRAPHICS_MANIFEST_VERSION",
    "build_applied_graphics_plan",
    "load_visual_replacements",
    "replacements_for_clip",
    "validate_applied_graphics_plan",
]
