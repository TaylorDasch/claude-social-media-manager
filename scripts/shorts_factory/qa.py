"""Fail-closed technical QA for rendered short-form video."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

from .captions import DEFAULT_MAX_WORDS_PER_CARD, QA_MIN_WORDS_PER_EVENT
from .vision import validate_visual_analysis


DELIVERY_WIDTH = 1080
DELIVERY_HEIGHT = 1920
DELIVERY_FPS = 30.0
MIN_DURATION_S = 10.0
MAX_DURATION_S = 60.0


def sha256_file(path: str | Path, *, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def sidecar_paths(path: str | Path) -> dict[str, Path]:
    media = Path(path)
    stem = media.with_suffix("")
    return {
        "captions": Path(f"{stem}.ass"),
        "crop_track": Path(f"{stem}.crop.json"),
        "checksum": Path(f"{stem}.sha256"),
        "manifest": Path(f"{stem}.render.json"),
    }


def _fraction(value: object) -> float:
    text = str(value or "0")
    if "/" not in text:
        return float(text)
    numerator, denominator = text.split("/", 1)
    divisor = float(denominator)
    return 0.0 if divisor == 0 else float(numerator) / divisor


def _probe(path: Path, *, ffprobe_path: str | None = None) -> dict[str, Any]:
    executable = ffprobe_path or shutil.which("ffprobe")
    if not executable:
        raise RuntimeError("ffprobe is required for render QA")
    result = subprocess.run(
        [
            executable,
            "-v",
            "error",
            "-show_streams",
            "-show_format",
            "-of",
            "json",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def _has_faststart(path: Path) -> bool:
    # A delivery MP4 should place moov before mdat.  Atom names can safely be
    # found in the first 16 MiB for the small front-loaded moov written by
    # ``+faststart``; fall back to the whole file only when needed.
    with path.open("rb") as handle:
        head = handle.read(16 * 1024 * 1024)
    moov = head.find(b"moov")
    mdat = head.find(b"mdat")
    # If moov is not in the head it cannot be a useful faststart atom.  Do not
    # load a potentially multi-gigabyte delivery into memory merely to locate
    # the trailing non-faststart atom.
    return moov >= 0 and mdat >= 0 and moov < mdat


def _validate_captions(path: Path) -> list[str]:
    if not path.is_file() or path.stat().st_size == 0:
        return [f"caption sidecar missing or empty: {path}"]
    text = path.read_text(encoding="utf-8", errors="replace")
    errors: list[str] = []
    if "PlayResX: 1080" not in text or "PlayResY: 1920" not in text:
        errors.append("caption sidecar does not target 1080x1920")
    if "[Events]" not in text:
        errors.append("caption sidecar has no Events section")
    dialogue_lines = [
        candidate for candidate in text.splitlines() if candidate.startswith("Dialogue:")
    ]
    if not dialogue_lines:
        errors.append("caption sidecar has no timed dialogue events")
    for index, line in enumerate(dialogue_lines, start=1):
        payload = line.split(",", 9)[-1]
        if payload.count(r"\N") > 1:
            errors.append(f"caption event {index} exceeds two lines")
        visible = re.sub(r"\{[^}]*\}", "", payload).replace(r"\N", " ")
        word_count = len(visible.split())
        if word_count < QA_MIN_WORDS_PER_EVENT:
            errors.append(
                f"caption event {index} has fewer than "
                f"{QA_MIN_WORDS_PER_EVENT} words"
            )
        if word_count > DEFAULT_MAX_WORDS_PER_CARD:
            errors.append(
                f"caption event {index} exceeds "
                f"{DEFAULT_MAX_WORDS_PER_CARD} words"
            )
    return errors


def _validate_checksum_sidecar(path: Path, actual_sha256: str) -> list[str]:
    if not path.is_file() or path.stat().st_size == 0:
        return [f"checksum sidecar missing or empty: {path}"]
    token = path.read_text(encoding="utf-8", errors="replace").strip().split()
    if not token:
        return ["checksum sidecar contains no digest"]
    recorded = token[0].lower()
    if not re.fullmatch(r"[0-9a-f]{64}", recorded):
        return ["checksum sidecar does not contain a SHA-256 digest"]
    if recorded != actual_sha256:
        return ["checksum sidecar does not match rendered media"]
    return []


def verify_render(
    path: str | Path,
    expected_duration_s: float,
    expected_sha256: str | None = None,
    *,
    captions_path: str | Path | None = None,
    crop_track_path: str | Path | None = None,
    checksum_path: str | Path | None = None,
    ffprobe_path: str | None = None,
    duration_tolerance_s: float = 0.40,
) -> dict[str, Any]:
    """Verify a delivery MP4 and all load-bearing sidecars.

    The return value is always serializable.  Callers must require
    ``result["passed"] is True``; the renderer raises when it is false.
    """
    media = Path(path).expanduser().resolve()
    defaults = sidecar_paths(media)
    captions = Path(captions_path).resolve() if captions_path else defaults["captions"]
    crop_track = (
        Path(crop_track_path).resolve() if crop_track_path else defaults["crop_track"]
    )
    checksum = Path(checksum_path).resolve() if checksum_path else defaults["checksum"]
    errors: list[str] = []
    warnings: list[str] = []
    media_info: dict[str, Any] = {}
    actual_sha256: str | None = None

    expected_duration = float(expected_duration_s)
    if not MIN_DURATION_S <= expected_duration <= MAX_DURATION_S:
        errors.append(
            f"expected duration {expected_duration:.3f}s is outside "
            f"{MIN_DURATION_S:.0f}-{MAX_DURATION_S:.0f}s"
        )
    if duration_tolerance_s < 0:
        errors.append("duration tolerance cannot be negative")

    if not media.is_file():
        errors.append(f"rendered media missing: {media}")
    elif media.stat().st_size <= 1024:
        errors.append("rendered media is empty or implausibly small")
    else:
        actual_sha256 = sha256_file(media)
        if expected_sha256 and actual_sha256.lower() != expected_sha256.lower():
            errors.append("rendered media checksum differs from expected_sha256")
        errors.extend(_validate_checksum_sidecar(checksum, actual_sha256))
        if not _has_faststart(media):
            errors.append("MP4 is not faststart (moov atom does not precede mdat)")
        try:
            probe = _probe(media, ffprobe_path=ffprobe_path)
            streams = probe.get("streams") or []
            video_streams = [s for s in streams if s.get("codec_type") == "video"]
            audio_streams = [s for s in streams if s.get("codec_type") == "audio"]
            if len(video_streams) != 1:
                errors.append(f"expected one video stream, found {len(video_streams)}")
            if len(audio_streams) != 1:
                errors.append(f"expected one audio stream, found {len(audio_streams)}")
            video = video_streams[0] if video_streams else {}
            audio = audio_streams[0] if audio_streams else {}
            duration = float(probe.get("format", {}).get("duration") or 0.0)
            fps = _fraction(video.get("avg_frame_rate")) if video else 0.0
            media_info = {
                "size_bytes": media.stat().st_size,
                "duration_s": duration,
                "width": int(video.get("width") or 0),
                "height": int(video.get("height") or 0),
                "video_codec": video.get("codec_name"),
                "pixel_format": video.get("pix_fmt"),
                "fps": round(fps, 3),
                "audio_codec": audio.get("codec_name"),
                "audio_sample_rate": int(audio.get("sample_rate") or 0),
                "audio_channels": int(audio.get("channels") or 0),
            }
            if media_info["width"] != DELIVERY_WIDTH or media_info["height"] != DELIVERY_HEIGHT:
                errors.append(
                    f"dimensions are {media_info['width']}x{media_info['height']}; "
                    f"expected {DELIVERY_WIDTH}x{DELIVERY_HEIGHT}"
                )
            if media_info["video_codec"] != "h264":
                errors.append(f"video codec is {media_info['video_codec']!r}; expected h264")
            if media_info["pixel_format"] != "yuv420p":
                errors.append(
                    f"pixel format is {media_info['pixel_format']!r}; expected yuv420p"
                )
            if abs(fps - DELIVERY_FPS) > 0.05:
                errors.append(f"frame rate is {fps:.3f}; expected {DELIVERY_FPS:.3f}")
            if media_info["audio_codec"] != "aac":
                errors.append(f"audio codec is {media_info['audio_codec']!r}; expected aac")
            if media_info["audio_sample_rate"] != 48000:
                errors.append(
                    f"audio sample rate is {media_info['audio_sample_rate']}; expected 48000"
                )
            if media_info["audio_channels"] not in {1, 2}:
                errors.append("audio must be mono or stereo")
            if not MIN_DURATION_S <= duration <= MAX_DURATION_S + duration_tolerance_s:
                errors.append(
                    f"render duration {duration:.3f}s is outside "
                    f"{MIN_DURATION_S:.0f}-{MAX_DURATION_S:.0f}s"
                )
            if abs(duration - expected_duration) > duration_tolerance_s:
                errors.append(
                    f"render duration {duration:.3f}s differs from expected "
                    f"{expected_duration:.3f}s by more than {duration_tolerance_s:.3f}s"
                )
        except (OSError, ValueError, subprocess.SubprocessError, json.JSONDecodeError) as exc:
            errors.append(f"ffprobe validation failed: {exc}")

    errors.extend(_validate_captions(captions))
    if not crop_track.is_file() or crop_track.stat().st_size == 0:
        errors.append(f"crop-track sidecar missing or empty: {crop_track}")
    else:
        try:
            crop_payload = json.loads(crop_track.read_text(encoding="utf-8"))
            errors.extend(validate_visual_analysis(crop_payload))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"crop-track sidecar is invalid JSON: {exc}")

    return {
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "path": str(media),
        "sha256": actual_sha256,
        "expected_duration_s": expected_duration,
        "media": media_info,
        "sidecars": {
            "captions": str(captions),
            "crop_track": str(crop_track),
            "checksum": str(checksum),
        },
    }


__all__ = ["sha256_file", "sidecar_paths", "verify_render"]
