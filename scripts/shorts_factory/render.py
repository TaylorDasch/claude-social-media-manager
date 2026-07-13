"""Deterministic 1080x1920 short-form rendering with technical QA."""

from __future__ import annotations

import json
import hashlib
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any, Mapping, Sequence

from .captions import build_ass_captions
from .graphics import (
    build_applied_graphics_plan,
    validate_applied_graphics_plan,
)
from .qa import sha256_file, sidecar_paths, verify_render
from .vision import (
    VALID_MODES,
    build_static_analysis,
    run_visual_analysis,
    validate_visual_analysis,
    write_visual_analysis,
)


OUTPUT_WIDTH = 1080
OUTPUT_HEIGHT = 1920
OUTPUT_FPS = 30
MIN_DURATION_S = 10.0
MAX_DURATION_S = 60.0
RENDERER_SCHEMA_VERSION = 3
REFRAME_ALGORITHM_VERSION = "opencv-haar-eye-dark-slide-v2"
CAPTION_STYLE_VERSION = "active-amber-v4-avenir-condensed-heavy"
GRAPHICS_COMPOSITOR_VERSION = "source-timeline-overlay-v1"


class RenderError(RuntimeError):
    """The media command could not produce a delivery candidate."""


class RenderValidationError(RenderError):
    """The render completed but did not pass the fail-closed QA gate."""

    def __init__(self, message: str, qa: Mapping[str, Any]):
        super().__init__(message)
        self.qa = dict(qa)


def _graphics_fingerprint(
    replacements: object,
) -> list[dict[str, Any]]:
    if replacements is None:
        return []
    if not isinstance(replacements, list):
        raise ValueError("metadata.visual_replacements must be a list")
    result: list[dict[str, Any]] = []
    for raw in replacements:
        if not isinstance(raw, Mapping):
            raise ValueError("metadata.visual_replacements entries must be objects")
        result.append(
            {
                "id": str(raw.get("id") or ""),
                "timeline_start_s": round(float(raw.get("timeline_start_s", 0)), 6),
                "timeline_end_s": round(float(raw.get("timeline_end_s", 0)), 6),
                "source_start_s": round(float(raw.get("source_start_s", 0)), 6),
                "source_end_s": round(float(raw.get("source_end_s", 0)), 6),
                "clip_start_s": round(float(raw.get("clip_start_s", 0)), 6),
                "clip_end_s": round(float(raw.get("clip_end_s", 0)), 6),
                "asset_start_s": round(float(raw.get("asset_start_s", 0)), 6),
                "asset_sha256": str(raw.get("asset_sha256") or ""),
                "timing_mode": str(raw.get("timing_mode") or ""),
            }
        )
    return result


def render_input_fingerprint(
    source_path: str | Path,
    start_s: float,
    end_s: float,
    words: Sequence[Mapping[str, Any]],
    mode: str,
    metadata: Mapping[str, Any] | None = None,
) -> str:
    """Hash every input that can materially change burned delivery bytes."""
    source = Path(source_path).expanduser().resolve()
    options = dict(metadata or {})
    source_stat = source.stat()
    source_identity = options.get("source_sha256") or {
        "size": source_stat.st_size,
        "mtime_ns": source_stat.st_mtime_ns,
    }
    relevant_words = [
        {
            "text": str(word.get("text", word.get("word", ""))),
            "start": round(float(word.get("start", 0)), 3),
            "end": round(float(word.get("end", 0)), 3),
        }
        for word in words
        if float(word.get("end", 0)) >= float(start_s)
        and float(word.get("start", 0)) <= float(end_s)
    ]
    supplied_analysis = options.get("visual_analysis")
    visual_replacements = _graphics_fingerprint(
        options.get("visual_replacements")
    )
    payload = {
        "renderer_schema": RENDERER_SCHEMA_VERSION,
        "reframe_algorithm": REFRAME_ALGORITHM_VERSION,
        "caption_style": CAPTION_STYLE_VERSION,
        "graphics_compositor": GRAPHICS_COMPOSITOR_VERSION,
        "source": source_identity,
        "start_s": round(float(start_s), 6),
        "end_s": round(float(end_s), 6),
        "words": relevant_words,
        "mode": mode,
        "sample_period_s": float(options.get("sample_period_s", 1.0)),
        "center_x": float(options.get("center_x", 0.5)),
        "center_y": float(options.get("center_y", 0.5)),
        "preset": str(options.get("preset", "fast")),
        "crf": int(options.get("crf", 20)),
        "visual_analysis": supplied_analysis,
        "visual_replacements": visual_replacements,
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _probe_source(path: Path, *, ffprobe_path: str | None = None) -> dict[str, Any]:
    executable = ffprobe_path or shutil.which("ffprobe")
    if not executable:
        raise RenderError("ffprobe is required for rendering")
    result = subprocess.run(
        [
            executable,
            "-v",
            "error",
            "-show_entries",
            "stream=index,codec_type,width,height:format=duration",
            "-of",
            "json",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)
    video = next(
        (stream for stream in payload.get("streams", []) if stream.get("codec_type") == "video"),
        None,
    )
    audio = next(
        (stream for stream in payload.get("streams", []) if stream.get("codec_type") == "audio"),
        None,
    )
    if not video:
        raise RenderError(f"source has no video stream: {path}")
    if not audio:
        raise RenderError(f"source has no audio stream: {path}")
    return {
        "width": int(video["width"]),
        "height": int(video["height"]),
        "duration": float(payload.get("format", {}).get("duration") or 0.0),
    }


def _has_ass_filter(executable: str) -> bool:
    try:
        result = subprocess.run(
            [executable, "-hide_banner", "-filters"],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    return any(" ass " in line or " subtitles " in line for line in result.stdout.splitlines())


def _ffmpeg_candidates(explicit: str | None = None) -> list[str]:
    candidates: list[str] = []
    for candidate in (explicit, os.getenv("SHORTS_FACTORY_FFMPEG")):
        if candidate and candidate not in candidates:
            candidates.append(candidate)
    try:
        import imageio_ffmpeg  # type: ignore[import-not-found]

        candidate = imageio_ffmpeg.get_ffmpeg_exe()
        if candidate not in candidates:
            candidates.append(candidate)
    except ImportError:
        pass

    # The machine's existing Vega environment owns a known libass-enabled
    # imageio binary.  Discover it without importing that environment into a
    # different Python interpreter.
    vega_binaries = sorted(
        Path("/Users/taylordasch_1/dasch-command/agents/vega/clipper/.venv").glob(
            "lib/python*/site-packages/imageio_ffmpeg/binaries/ffmpeg-*"
        )
    )
    for path in vega_binaries:
        candidate = str(path)
        if candidate not in candidates:
            candidates.append(candidate)
    system = shutil.which("ffmpeg")
    if system and system not in candidates:
        candidates.append(system)
    return candidates


def _resolve_ffmpeg(*, require_ass: bool, explicit: str | None = None) -> str:
    for candidate in _ffmpeg_candidates(explicit):
        if not Path(candidate).is_file() and not shutil.which(candidate):
            continue
        if not require_ass or _has_ass_filter(candidate):
            return candidate
    detail = " with libass/ASS support" if require_ass else ""
    raise RenderError(f"no usable ffmpeg{detail} was found")


def _escape_filter_path(path: Path) -> str:
    return (
        str(path)
        .replace("\\", "\\\\")
        .replace(":", r"\:")
        .replace("'", r"\'")
        .replace("[", r"\[")
        .replace("]", r"\]")
    )


def _interpolate_point(
    points: Sequence[Mapping[str, Any]], time_s: float
) -> tuple[float, float]:
    ordered = sorted(points, key=lambda point: float(point["time_s"]))
    if not ordered:
        return 0.5, 0.5
    if time_s <= float(ordered[0]["time_s"]):
        return float(ordered[0]["center_x"]), float(ordered[0]["center_y"])
    for left, right in zip(ordered, ordered[1:]):
        left_time = float(left["time_s"])
        right_time = float(right["time_s"])
        if time_s <= right_time:
            span = max(0.001, right_time - left_time)
            weight = (time_s - left_time) / span
            return (
                float(left["center_x"])
                + weight * (float(right["center_x"]) - float(left["center_x"])),
                float(left["center_y"])
                + weight * (float(right["center_y"]) - float(left["center_y"])),
            )
    return float(ordered[-1]["center_x"]), float(ordered[-1]["center_y"])


def _points_for_segment(
    all_points: Sequence[Mapping[str, Any]], start_s: float, end_s: float
) -> list[dict[str, float]]:
    start_x, start_y = _interpolate_point(all_points, start_s)
    end_x, end_y = _interpolate_point(all_points, end_s)
    points: list[dict[str, float]] = [
        {"time_s": 0.0, "center_x": start_x, "center_y": start_y}
    ]
    for point in all_points:
        timestamp = float(point["time_s"])
        if start_s < timestamp < end_s:
            points.append(
                {
                    "time_s": timestamp - start_s,
                    "center_x": float(point["center_x"]),
                    "center_y": float(point["center_y"]),
                }
            )
    points.append(
        {"time_s": end_s - start_s, "center_x": end_x, "center_y": end_y}
    )
    return points


def _piecewise_expression(points: Sequence[Mapping[str, float]], axis: str) -> str:
    if not points:
        return "0.5"
    if len(points) == 1:
        return f"{float(points[0][axis]):.6f}"
    expression = f"{float(points[-1][axis]):.6f}"
    for left, right in reversed(list(zip(points, points[1:]))):
        left_t = float(left["time_s"])
        right_t = float(right["time_s"])
        left_value = float(left[axis])
        right_value = float(right[axis])
        span = max(0.001, right_t - left_t)
        interpolation = (
            f"{left_value:.6f}+({right_value - left_value:.6f})"
            f"*(t-{left_t:.3f})/{span:.3f}"
        )
        expression = f"if(lt(t,{right_t:.3f}),{interpolation},{expression})"
    return expression


def _crop_filter(points: Sequence[Mapping[str, float]]) -> str:
    center_x = _piecewise_expression(points, "center_x")
    center_y = _piecewise_expression(points, "center_y")
    crop_w = "floor(min(iw,ih*9/16)/2)*2"
    crop_h = "floor(min(ih,iw*16/9)/2)*2"
    crop_x = f"floor(max(0,min(iw-ow,({center_x})*iw-ow/2))/2)*2"
    crop_y = f"floor(max(0,min(ih-oh,({center_y})*ih-oh/2))/2)*2"
    return (
        f"crop=w='{crop_w}':h='{crop_h}':x='{crop_x}':y='{crop_y}',"
        f"scale={OUTPUT_WIDTH}:{OUTPUT_HEIGHT}:flags=lanczos,setsar=1"
    )


def _normalise_segments(
    analysis: Mapping[str, Any], duration_s: float
) -> list[dict[str, Any]]:
    raw_segments = analysis.get("segments") or []
    track = analysis.get("crop_track") or []
    segments: list[dict[str, Any]] = []
    for raw in raw_segments:
        start = max(0.0, float(raw["start_s"]))
        end = min(duration_s, float(raw["end_s"]))
        if end - start < 0.001:
            continue
        mode = str(raw["mode"])
        if mode not in VALID_MODES:
            raise RenderError(f"unsupported reframe mode in crop plan: {mode}")
        segments.append(
            {
                "start_s": start,
                "end_s": end,
                "mode": mode,
                "points": _points_for_segment(track, start, end),
            }
        )
    if not segments:
        raise RenderError("visual analysis produced no renderable segments")
    return segments


def _build_filter_graph(
    analysis: Mapping[str, Any],
    duration_s: float,
    captions_path: Path,
    burn_captions: bool,
    visual_replacements: Sequence[Mapping[str, Any]] = (),
) -> str:
    segments = _normalise_segments(analysis, duration_s)
    graph: list[str] = []
    if len(segments) == 1:
        graph.append("[0:v:0]setpts=PTS-STARTPTS[src0]")
    else:
        labels = "".join(f"[src{index}]" for index in range(len(segments)))
        graph.append(
            f"[0:v:0]setpts=PTS-STARTPTS,split={len(segments)}{labels}"
        )

    output_labels: list[str] = []
    for index, segment in enumerate(segments):
        start = float(segment["start_s"])
        end = float(segment["end_s"])
        prefix = f"[src{index}]trim=start={start:.3f}:end={end:.3f},setpts=PTS-STARTPTS"
        output = f"seg{index}"
        mode = segment["mode"]
        if mode == "contain":
            graph.append(f"{prefix},split=2[bg{index}][fg{index}]")
            graph.append(
                f"[bg{index}]scale={OUTPUT_WIDTH}:{OUTPUT_HEIGHT}:"
                "force_original_aspect_ratio=increase,"
                f"crop={OUTPUT_WIDTH}:{OUTPUT_HEIGHT},gblur=sigma=28,"
                f"eq=brightness=-0.16:saturation=0.78[blur{index}]"
            )
            graph.append(
                f"[fg{index}]scale=1000:1700:force_original_aspect_ratio=decrease:"
                f"flags=lanczos,setsar=1[main{index}]"
            )
            graph.append(
                f"[blur{index}][main{index}]overlay=(W-w)/2:(H-h)/2:shortest=1,"
                f"format=yuv420p,setsar=1[{output}]"
            )
        else:
            graph.append(
                f"{prefix},{_crop_filter(segment['points'])},"
                f"format=yuv420p[{output}]"
            )
        output_labels.append(f"[{output}]")

    if len(output_labels) == 1:
        base = output_labels[0]
    else:
        graph.append(
            "".join(output_labels)
            + f"concat=n={len(output_labels)}:v=1:a=0[joined]"
        )
        base = "[joined]"

    # Frame-rate conversion belongs after concat. Applying it independently to
    # many short visual-mode segments rounds each boundary down by up to one
    # frame and can cumulatively shorten a real clip by almost half a second.
    graph.append(f"{base}fps={OUTPUT_FPS},format=yuv420p,setsar=1[vbase]")
    base = "[vbase]"

    # Replacement inputs are native vertical graphics bound to exact absolute
    # source ranges. They replace pixels only; source input 0 remains the sole
    # audio source. Captions are intentionally applied after every replacement.
    for index, replacement in enumerate(visual_replacements):
        input_index = index + 1
        local_start = float(replacement["clip_start_s"])
        local_end = float(replacement["clip_end_s"])
        asset_start = float(replacement["asset_start_s"])
        asset_duration = float(replacement["asset"]["duration_s"])
        timeline_duration = float(replacement["timeline_end_s"]) - float(
            replacement["timeline_start_s"]
        )
        hold_duration = max(0.0, timeline_duration - asset_duration) + 0.10
        overlap_duration = local_end - local_start
        graphic_label = f"graphic{index}"
        replaced_label = f"replaced{index}"
        graph.append(
            f"[{input_index}:v:0]settb=AVTB,setpts=PTS-STARTPTS,"
            f"fps={OUTPUT_FPS},scale={OUTPUT_WIDTH}:{OUTPUT_HEIGHT}:flags=lanczos,"
            f"setsar=1,format=yuv420p,"
            f"tpad=stop_mode=clone:stop_duration={hold_duration:.6f},"
            f"trim=start={asset_start:.6f}:duration={overlap_duration:.6f},"
            f"setpts=PTS-STARTPTS+{local_start:.6f}/TB[{graphic_label}]"
        )
        graph.append(
            f"{base}[{graphic_label}]overlay=x=0:y=0:eof_action=pass:"
            f"repeatlast=0:shortest=0:"
            f"enable='gte(t,{local_start:.6f})*lt(t,{local_end:.6f})'"
            f"[{replaced_label}]"
        )
        base = f"[{replaced_label}]"

    if burn_captions:
        escaped = _escape_filter_path(captions_path)
        graph.append(f"{base}ass=filename='{escaped}'[vout]")
    else:
        graph.append(f"{base}null[vout]")
    return ";".join(graph)


def _select_analysis(
    *,
    source_path: Path,
    start_s: float,
    end_s: float,
    mode: str,
    source_info: Mapping[str, Any],
    metadata: Mapping[str, Any],
) -> dict[str, Any]:
    supplied = metadata.get("visual_analysis")
    if supplied is not None:
        if not isinstance(supplied, Mapping):
            raise RenderError("metadata.visual_analysis must be an object")
        analysis = dict(supplied)
    elif mode == "auto":
        analysis = run_visual_analysis(
            source_path,
            start_s,
            end_s,
            sample_period_s=float(metadata.get("sample_period_s", 1.0)),
            ffprobe_path=metadata.get("ffprobe_path"),
        )
    else:
        aliases = {
            "talking_head": "face_crop",
            "b_roll": "saliency_crop",
            "graphic_safe": "contain",
        }
        selected_mode = aliases.get(mode, mode)
        if selected_mode not in VALID_MODES:
            raise RenderError(
                f"mode must be auto, talking_head, b_roll, graphic_safe, or one of "
                f"{sorted(VALID_MODES)}"
            )
        analysis = build_static_analysis(
            width=int(source_info["width"]),
            height=int(source_info["height"]),
            duration_s=end_s - start_s,
            mode=selected_mode,
            center_x=float(metadata.get("center_x", 0.5)),
            center_y=float(metadata.get("center_y", 0.5)),
        )
    errors = validate_visual_analysis(analysis)
    if errors:
        raise RenderError("visual analysis failed validation: " + "; ".join(errors))
    if abs(float(analysis["duration_s"]) - (end_s - start_s)) > 0.05:
        raise RenderError("visual analysis duration does not match requested source span")
    return analysis


def render_clip(
    source_path: str | Path,
    output_path: str | Path,
    start_s: float,
    end_s: float,
    words: Sequence[Mapping[str, Any]] | None = None,
    mode: str = "auto",
    metadata: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Render one exact source span and return a QA-gated artifact record.

    ``metadata`` accepts operational overrides used by tests/integration:
    ``visual_analysis``, ``ffmpeg_path``, ``ffprobe_path``, ``preset``,
    ``crf``, ``sample_period_s``, ``center_x``, ``center_y`` and validated
    ``visual_replacements``.
    """
    source = Path(source_path).expanduser().resolve()
    destination = Path(output_path).expanduser().resolve()
    if not source.is_file():
        raise FileNotFoundError(source)
    start = float(start_s)
    end = float(end_s)
    duration = end - start
    if start < 0 or end <= start:
        raise ValueError("render span requires 0 <= start_s < end_s")
    if not MIN_DURATION_S <= duration <= MAX_DURATION_S:
        raise ValueError(
            f"short duration must be {MIN_DURATION_S:.0f}-{MAX_DURATION_S:.0f}s; "
            f"received {duration:.3f}s"
        )
    if destination.suffix.lower() != ".mp4":
        raise ValueError("short-form delivery path must end in .mp4")
    if not words:
        raise RenderError(
            "word-level transcript timings are required for captioned delivery"
        )

    options = dict(metadata or {})
    raw_replacements = options.get("visual_replacements") or []
    if not isinstance(raw_replacements, list) or not all(
        isinstance(replacement, Mapping) for replacement in raw_replacements
    ):
        raise ValueError("metadata.visual_replacements must be a list of objects")
    visual_replacements = [dict(replacement) for replacement in raw_replacements]
    input_fingerprint = render_input_fingerprint(
        source,
        start,
        end,
        words,
        mode,
        options,
    )
    source_info = _probe_source(source, ffprobe_path=options.get("ffprobe_path"))
    if end > float(source_info["duration"]) + 0.10:
        raise ValueError(
            f"render span ends at {end:.3f}s but source is "
            f"{source_info['duration']:.3f}s"
        )
    destination.parent.mkdir(parents=True, exist_ok=True)
    sidecars = sidecar_paths(destination)

    captions = build_ass_captions(
        words,
        sidecars["captions"],
        clip_start_s=start,
        clip_end_s=end,
        width=OUTPUT_WIDTH,
        height=OUTPUT_HEIGHT,
    )
    if int(captions["event_count"]) == 0:
        raise RenderError("caption words were supplied but none overlap the source span")

    analysis = _select_analysis(
        source_path=source,
        start_s=start,
        end_s=end,
        mode=mode,
        source_info=source_info,
        metadata=options,
    )
    write_visual_analysis(analysis, sidecars["crop_track"])
    graphics_plan = build_applied_graphics_plan(
        source_sha256=options.get("source_sha256"),
        clip_start_s=start,
        clip_end_s=end,
        replacements=visual_replacements,
    )
    sidecars["graphics"].write_text(
        json.dumps(graphics_plan, indent=2), encoding="utf-8"
    )
    graphics_errors = validate_applied_graphics_plan(sidecars["graphics"])
    if graphics_errors:
        raise RenderError(
            "visual replacement plan failed validation: "
            + "; ".join(graphics_errors)
        )

    burn_captions = True
    ffmpeg = _resolve_ffmpeg(
        require_ass=burn_captions,
        explicit=options.get("ffmpeg_path"),
    )
    filter_graph = _build_filter_graph(
        analysis,
        duration,
        sidecars["captions"],
        burn_captions,
        visual_replacements,
    )
    preset = str(options.get("preset", "fast"))
    crf = int(options.get("crf", 20))
    if not 0 <= crf <= 51:
        raise ValueError("crf must be between 0 and 51")

    command = [
        ffmpeg,
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-ss",
        f"{start:.6f}",
        "-i",
        str(source),
    ]
    for replacement in visual_replacements:
        command.extend(["-i", str(replacement["asset_path"])])
    command.extend(
        [
            "-filter_complex",
            filter_graph,
            "-map",
            "[vout]",
            "-map",
            "0:a:0",
            "-af",
            (
                "asetpts=PTS-STARTPTS,loudnorm=I=-16:LRA=11:TP=-1.5,"
                f"apad=whole_dur={duration:.6f},atrim=duration={duration:.6f}"
            ),
            "-c:v",
            "libx264",
            "-preset",
            preset,
            "-crf",
            str(crf),
            "-profile:v",
            "high",
            "-pix_fmt",
            "yuv420p",
            "-r",
            str(OUTPUT_FPS),
            "-c:a",
            "aac",
            "-b:a",
            "160k",
            "-ar",
            "48000",
            "-ac",
            "2",
            "-movflags",
            "+faststart",
            "-shortest",
            str(destination),
        ]
    )
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout or str(exc))[-5000:]
        raise RenderError(f"ffmpeg render failed: {detail}") from exc

    checksum = sha256_file(destination)
    sidecars["checksum"].write_text(
        f"{checksum}  {destination.name}\n", encoding="utf-8"
    )
    qa = verify_render(
        destination,
        duration,
        checksum,
        captions_path=sidecars["captions"],
        crop_track_path=sidecars["crop_track"],
        graphics_plan_path=sidecars["graphics"],
        checksum_path=sidecars["checksum"],
        ffprobe_path=options.get("ffprobe_path"),
    )

    manifest = {
        "version": RENDERER_SCHEMA_VERSION,
        "input_fingerprint": input_fingerprint,
        "status": "verified" if qa["passed"] else "qa_failed",
        "source_path": str(source),
        "source_span": {"start_s": start, "end_s": end, "duration_s": duration},
        "output_path": str(destination),
        "sha256": checksum,
        "dimensions": {"width": OUTPUT_WIDTH, "height": OUTPUT_HEIGHT},
        "fps": OUTPUT_FPS,
        "video_codec": "h264",
        "audio_codec": "aac",
        "pixel_format": "yuv420p",
        "faststart": True,
        "watermark": False,
        "dominant_mode": analysis.get("dominant_mode"),
        "segment_count": len(analysis.get("segments") or []),
        "visual_replacements": graphics_plan,
        "captions": captions,
        "sidecars": {key: str(value) for key, value in sidecars.items()},
        "qa": qa,
    }
    sidecars["manifest"].write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    if not qa["passed"]:
        raise RenderValidationError(
            "render failed technical QA: " + "; ".join(qa["errors"]), qa
        )
    return manifest


__all__ = [
    "RenderError",
    "RenderValidationError",
    "render_input_fingerprint",
    "render_clip",
]
