"""Lightweight shot and subject analysis for vertical reframing.

The analyzer deliberately uses OpenCV's bundled face cascade and image
statistics instead of downloading a model.  When OpenCV is unavailable it
returns a bounded centered plan; rendering remains deterministic and safe.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


VALID_MODES = {"face_crop", "saliency_crop", "center_crop", "contain"}


def _probe_video(path: Path, *, ffprobe_path: str | None = None) -> dict[str, Any]:
    executable = ffprobe_path or shutil.which("ffprobe")
    if not executable:
        raise RuntimeError("ffprobe is required for visual analysis")
    result = subprocess.run(
        [
            executable,
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height,duration:format=duration",
            "-of",
            "json",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)
    streams = payload.get("streams") or []
    if not streams:
        raise ValueError(f"no video stream found in {path}")
    stream = streams[0]
    duration = stream.get("duration") or payload.get("format", {}).get("duration") or 0
    return {
        "width": int(stream["width"]),
        "height": int(stream["height"]),
        "duration": float(duration),
    }


def _crop_geometry(
    width: int,
    height: int,
    center_x: float,
    center_y: float,
) -> dict[str, float]:
    """Return a bounded normalized 9:16 crop around a normalized center."""
    source_ratio = width / height
    target_ratio = 9 / 16
    if source_ratio >= target_ratio:
        crop_w = target_ratio / source_ratio
        crop_h = 1.0
    else:
        crop_w = 1.0
        crop_h = source_ratio / target_ratio
    crop_x = min(max(center_x - crop_w / 2, 0.0), 1.0 - crop_w)
    crop_y = min(max(center_y - crop_h / 2, 0.0), 1.0 - crop_h)
    return {
        "x": round(crop_x, 6),
        "y": round(crop_y, 6),
        "width": round(crop_w, 6),
        "height": round(crop_h, 6),
    }


def _bounded_point(
    *,
    time_s: float,
    center_x: float,
    center_y: float,
    width: int,
    height: int,
    confidence: float,
    source: str,
    shot_index: int = 0,
) -> dict[str, Any]:
    crop = _crop_geometry(width, height, center_x, center_y)
    # Store the actual bounded center after crop-edge clamping.  That makes
    # the sidecar independently verifiable instead of relying on FFmpeg to
    # repair an out-of-range tracking point.
    bounded_x = crop["x"] + crop["width"] / 2
    bounded_y = crop["y"] + crop["height"] / 2
    return {
        "time_s": round(max(0.0, time_s), 3),
        "center_x": round(bounded_x, 6),
        "center_y": round(bounded_y, 6),
        "confidence": round(min(max(confidence, 0.0), 1.0), 4),
        "source": source,
        "shot_index": int(shot_index),
        "crop": crop,
    }


def build_static_analysis(
    *,
    width: int,
    height: int,
    duration_s: float,
    mode: str = "center_crop",
    center_x: float = 0.5,
    center_y: float = 0.5,
) -> dict[str, Any]:
    """Create a serializable, bounded one-shot analysis plan."""
    if mode not in VALID_MODES:
        raise ValueError(f"unsupported reframe mode: {mode}")
    if duration_s <= 0:
        raise ValueError("duration_s must be positive")
    points = [
        _bounded_point(
            time_s=0.0,
            center_x=center_x,
            center_y=center_y,
            width=width,
            height=height,
            confidence=1.0,
            source="static",
        ),
        _bounded_point(
            time_s=duration_s,
            center_x=center_x,
            center_y=center_y,
            width=width,
            height=height,
            confidence=1.0,
            source="static",
        ),
    ]
    return {
        "version": 1,
        "source": {"width": width, "height": height},
        "duration_s": round(duration_s, 3),
        "sample_period_s": None,
        "dominant_mode": mode,
        "segments": [
            {
                "start_s": 0.0,
                "end_s": round(duration_s, 3),
                "mode": mode,
                "shot_index": 0,
                "crop_track": points,
            }
        ],
        "crop_track": points,
        "analysis_backend": "static",
        "warnings": [],
    }


def _face_candidate(
    frame: Any,
    detector: Any,
    eye_detector: Any,
    cv2: Any,
) -> dict[str, float] | None:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    frame_h, frame_w = gray.shape[:2]
    faces = detector.detectMultiScale(
        gray,
        scaleFactor=1.12,
        minNeighbors=5,
        minSize=(max(24, frame_w // 20), max(24, frame_h // 20)),
    )
    if len(faces) == 0:
        return None
    # A speaking face is normally the largest face; its size also provides a
    # useful confidence signal without claiming identity recognition.
    x, y, width, height = max(faces, key=lambda box: int(box[2]) * int(box[3]))
    face_roi = gray[y : y + height, x : x + width]
    eyes = eye_detector.detectMultiScale(
        face_roi,
        scaleFactor=1.10,
        minNeighbors=4,
        minSize=(max(8, width // 9), max(6, height // 12)),
    )
    # Numbers, charts, and house windows can trigger the frontal-face cascade.
    # Requiring at least one eye signal prevents those false positives from
    # turning a graphic-safe contain segment into a destructive face crop.
    if len(eyes) == 0:
        return None
    area_ratio = float(width * height) / float(frame_w * frame_h)
    return {
        "center_x": float(x + width / 2) / frame_w,
        # A slight downward bias keeps shoulders in the 9:16 composition.
        "center_y": min(0.9, float(y + height * 0.78) / frame_h),
        "confidence": min(1.0, 0.45 + area_ratio * 4.5),
        "area_ratio": area_ratio,
    }


def _frame_metrics(frame: Any, cv2: Any, np: Any) -> dict[str, float]:
    small = cv2.resize(frame, (320, 180), interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)
    sobel_x = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
    energy = cv2.magnitude(sobel_x, sobel_y)
    energy_sum = float(energy.sum())

    if energy_sum > 1e-6:
        yy, xx = np.indices(energy.shape)
        center_x = float((energy * xx).sum() / energy_sum) / energy.shape[1]
        center_y = float((energy * yy).sum() / energy_sum) / energy.shape[0]
    else:
        center_x = center_y = 0.5

    target_crop_width = max(1, round(gray.shape[0] * 9 / 16))
    left = max(0, (gray.shape[1] - target_crop_width) // 2)
    right = min(gray.shape[1], left + target_crop_width)
    center_energy = float(energy[:, left:right].sum())
    outside_ratio = 0.0 if energy_sum <= 1e-6 else 1.0 - center_energy / energy_sum
    edges = cv2.Canny(gray, 80, 180)
    edge_density = float(np.count_nonzero(edges)) / float(edges.size)
    mean_saturation = float(hsv[:, :, 1].mean()) / 255.0
    contrast = min(1.0, float(gray.std()) / 64.0)
    dark_ratio = float(np.count_nonzero(gray < 60)) / float(gray.size)

    # Graphics/slides/maps are dangerous to center-crop when much of their
    # structure sits outside the narrow 9:16 window.  Low saturation and a
    # high edge density are secondary signals, never sole triggers.
    graphic_score = (
        max(0.0, min(1.0, (outside_ratio - 0.42) / 0.40)) * 0.62
        + max(0.0, min(1.0, (edge_density - 0.06) / 0.18)) * 0.23
        + max(0.0, min(1.0, (0.35 - mean_saturation) / 0.35)) * 0.10
        + max(0.0, min(1.0, (contrast - 0.30) / 0.70)) * 0.05
    )
    # Branded stat cards in Taylor's edits often use a nearly uniform navy
    # background with sparse centered type. Their edge energy sits *inside*
    # the 9:16 center, so the outside-energy heuristic alone misses them.
    dark_slide_score = max(0.0, min(1.0, (dark_ratio - 0.72) / 0.20)) * (
        0.75 + min(0.25, edge_density / 0.08 * 0.25)
    )
    graphic_score = max(graphic_score, dark_slide_score)
    return {
        "saliency_x": min(max(center_x, 0.08), 0.92),
        "saliency_y": min(max(center_y, 0.12), 0.88),
        "graphic_score": min(max(graphic_score, 0.0), 1.0),
        "outside_energy_ratio": min(max(outside_ratio, 0.0), 1.0),
        "edge_density": edge_density,
        "dark_ratio": dark_ratio,
    }


def _histogram(frame: Any, cv2: Any) -> Any:
    hsv = cv2.cvtColor(cv2.resize(frame, (160, 90)), cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv], [0, 1], None, [32, 16], [0, 180, 0, 256])
    cv2.normalize(hist, hist)
    return hist


def _majority_mode(samples: Sequence[dict[str, Any]], index: int) -> str:
    if samples[index].get("scene_cut"):
        return str(samples[index]["mode"])
    start = max(0, index - 1)
    end = min(len(samples), index + 2)
    modes = [str(sample["mode"]) for sample in samples[start:end]]
    counts = Counter(modes)
    winner, count = counts.most_common(1)[0]
    return winner if count >= 2 else str(samples[index]["mode"])


def _smooth_samples(
    samples: Sequence[dict[str, Any]],
    *,
    width: int,
    height: int,
) -> list[dict[str, Any]]:
    smoothed: list[dict[str, Any]] = []
    prior_x = prior_y = 0.5
    prior_shot = -1
    alpha = 0.38
    for index, raw in enumerate(samples):
        shot = int(raw["shot_index"])
        mode = _majority_mode(samples, index)
        if shot != prior_shot or mode == "contain":
            prior_x = float(raw["center_x"])
            prior_y = float(raw["center_y"])
        else:
            prior_x += alpha * (float(raw["center_x"]) - prior_x)
            prior_y += alpha * (float(raw["center_y"]) - prior_y)
        prior_shot = shot
        point = _bounded_point(
            time_s=float(raw["time_s"]),
            center_x=prior_x,
            center_y=prior_y,
            width=width,
            height=height,
            confidence=float(raw["confidence"]),
            source=str(raw["source"]),
            shot_index=shot,
        )
        point["mode"] = mode
        point["graphic_score"] = round(float(raw["graphic_score"]), 4)
        smoothed.append(point)
    return smoothed


def _segment_track(
    track: Sequence[dict[str, Any]],
    *,
    duration_s: float,
) -> list[dict[str, Any]]:
    if not track:
        return []
    segments: list[dict[str, Any]] = []
    start_index = 0
    for index in range(1, len(track)):
        changed_mode = track[index]["mode"] != track[index - 1]["mode"]
        changed_shot = track[index]["shot_index"] != track[index - 1]["shot_index"]
        if not (changed_mode or changed_shot):
            continue
        boundary = (float(track[index - 1]["time_s"]) + float(track[index]["time_s"])) / 2
        segments.append(
            {
                "start_s": 0.0 if not segments else segments[-1]["end_s"],
                "end_s": round(boundary, 3),
                "mode": track[start_index]["mode"],
                "shot_index": track[start_index]["shot_index"],
                "crop_track": list(track[start_index:index]),
            }
        )
        start_index = index
    segments.append(
        {
            "start_s": 0.0 if not segments else segments[-1]["end_s"],
            "end_s": round(duration_s, 3),
            "mode": track[start_index]["mode"],
            "shot_index": track[start_index]["shot_index"],
            "crop_track": list(track[start_index:]),
        }
    )
    return [segment for segment in segments if segment["end_s"] > segment["start_s"]]


def _mode_for_metrics(
    face: Mapping[str, float] | None,
    metrics: Mapping[str, float],
) -> tuple[str, float, float, float, str]:
    if face is not None and float(face.get("confidence", 0.0)) >= 0.48:
        return (
            "face_crop",
            float(face["center_x"]),
            float(face["center_y"]),
            float(face["confidence"]),
            "face",
        )
    if float(metrics["graphic_score"]) >= 0.56:
        return "contain", 0.5, 0.5, float(metrics["graphic_score"]), "graphic_safe"
    return (
        "saliency_crop",
        float(metrics["saliency_x"]),
        float(metrics["saliency_y"]),
        max(0.35, 1.0 - float(metrics["graphic_score"])),
        "saliency",
    )


def run_visual_analysis(
    source_path: str | Path,
    start_s: float,
    end_s: float,
    *,
    sample_period_s: float = 1.0,
    max_samples: int = 90,
    ffprobe_path: str | None = None,
) -> dict[str, Any]:
    """Analyze an exact source span and return a shot-aware reframe plan.

    Modes are ``face_crop`` (smoothed subject tracking), ``saliency_crop``
    (B-roll), and ``contain`` (graphic-safe blurred-background composition).
    """
    path = Path(source_path).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(path)
    start = float(start_s)
    end = float(end_s)
    if start < 0 or end <= start:
        raise ValueError("visual analysis requires 0 <= start_s < end_s")
    if sample_period_s <= 0 or max_samples <= 0:
        raise ValueError("sample_period_s and max_samples must be positive")

    probe = _probe_video(path, ffprobe_path=ffprobe_path)
    if end > probe["duration"] + 0.10:
        raise ValueError(
            f"analysis span ends at {end:.3f}s but source is {probe['duration']:.3f}s"
        )
    duration = end - start

    try:
        import cv2  # type: ignore[import-not-found]
        import numpy as np  # type: ignore[import-not-found]
    except ImportError:
        fallback = build_static_analysis(
            width=probe["width"],
            height=probe["height"],
            duration_s=duration,
            mode="center_crop",
        )
        fallback["analysis_backend"] = "center_fallback"
        fallback["warnings"] = [
            "OpenCV unavailable; used bounded center crop instead of subject tracking."
        ]
        return fallback

    detector = cv2.CascadeClassifier(
        str(Path(cv2.data.haarcascades) / "haarcascade_frontalface_default.xml")
    )
    if detector.empty():
        raise RuntimeError("OpenCV face cascade could not be loaded")
    eye_detector = cv2.CascadeClassifier(
        str(Path(cv2.data.haarcascades) / "haarcascade_eye.xml")
    )
    if eye_detector.empty():
        raise RuntimeError("OpenCV eye cascade could not be loaded")

    capture = cv2.VideoCapture(str(path))
    if not capture.isOpened():
        raise RuntimeError(f"OpenCV could not open {path}")
    sample_count = min(max_samples, max(2, int(duration / sample_period_s) + 1))
    if sample_count <= 1:
        times: Iterable[float] = [0.0]
    else:
        step = duration / (sample_count - 1)
        times = (min(duration - 0.001, index * step) for index in range(sample_count))

    raw_samples: list[dict[str, Any]] = []
    previous_hist = None
    shot_index = 0
    try:
        for relative_time in times:
            capture.set(cv2.CAP_PROP_POS_MSEC, (start + relative_time) * 1000.0)
            ok, frame = capture.read()
            if not ok or frame is None:
                continue
            hist = _histogram(frame, cv2)
            scene_cut = False
            if previous_hist is not None:
                correlation = float(
                    cv2.compareHist(previous_hist, hist, cv2.HISTCMP_CORREL)
                )
                scene_cut = correlation < 0.45
                if scene_cut:
                    shot_index += 1
            previous_hist = hist
            face = _face_candidate(frame, detector, eye_detector, cv2)
            metrics = _frame_metrics(frame, cv2, np)
            mode, center_x, center_y, confidence, source = _mode_for_metrics(
                face, metrics
            )
            raw_samples.append(
                {
                    "time_s": relative_time,
                    "mode": mode,
                    "center_x": center_x,
                    "center_y": center_y,
                    "confidence": confidence,
                    "source": source,
                    "graphic_score": metrics["graphic_score"],
                    "scene_cut": scene_cut,
                    "shot_index": shot_index,
                }
            )
    finally:
        capture.release()

    if not raw_samples:
        fallback = build_static_analysis(
            width=probe["width"],
            height=probe["height"],
            duration_s=duration,
            mode="center_crop",
        )
        fallback["analysis_backend"] = "decode_fallback"
        fallback["warnings"] = ["No sample frames decoded; used bounded center crop."]
        return fallback

    track = _smooth_samples(raw_samples, width=probe["width"], height=probe["height"])
    # Anchor interpolation at exact clip boundaries.
    if float(track[0]["time_s"]) > 0:
        first = dict(track[0])
        first["time_s"] = 0.0
        track.insert(0, first)
    last = dict(track[-1])
    last["time_s"] = round(duration, 3)
    if float(track[-1]["time_s"]) < duration - 0.001:
        track.append(last)
    else:
        track[-1] = last

    segments = _segment_track(track, duration_s=duration)
    counts = Counter(str(point["mode"]) for point in track)
    dominant = counts.most_common(1)[0][0]
    return {
        "version": 1,
        "source": {"width": probe["width"], "height": probe["height"]},
        "duration_s": round(duration, 3),
        "source_span": {"start_s": start, "end_s": end},
        "sample_period_s": sample_period_s,
        "dominant_mode": dominant,
        "segments": segments,
        "crop_track": track,
        "analysis_backend": "opencv-haar-saliency",
        "warnings": [],
    }


def validate_visual_analysis(analysis: Mapping[str, Any]) -> list[str]:
    """Return crop-plan validation errors; an empty list means safe to render."""
    errors: list[str] = []
    try:
        width = int(analysis["source"]["width"])
        height = int(analysis["source"]["height"])
        duration = float(analysis["duration_s"])
    except (KeyError, TypeError, ValueError):
        return ["crop plan is missing valid source dimensions or duration"]
    if width <= 0 or height <= 0 or duration <= 0:
        errors.append("crop plan dimensions and duration must be positive")

    segments = analysis.get("segments")
    if not isinstance(segments, Sequence) or not segments:
        errors.append("crop plan has no segments")
        return errors
    previous_end = 0.0
    for index, segment in enumerate(segments):
        if not isinstance(segment, Mapping):
            errors.append(f"segment {index} is not an object")
            continue
        mode = segment.get("mode")
        if mode not in VALID_MODES:
            errors.append(f"segment {index} has unsupported mode {mode!r}")
        try:
            start = float(segment["start_s"])
            end = float(segment["end_s"])
        except (KeyError, TypeError, ValueError):
            errors.append(f"segment {index} has invalid bounds")
            continue
        if start < -0.001 or end <= start or end > duration + 0.05:
            errors.append(f"segment {index} lies outside the clip duration")
        if abs(start - previous_end) > 0.05:
            errors.append(f"segment {index} leaves a gap or overlap")
        previous_end = end
    if abs(previous_end - duration) > 0.05:
        errors.append("segments do not cover the complete clip")

    track = analysis.get("crop_track")
    if not isinstance(track, Sequence) or not track:
        errors.append("crop plan has no crop_track")
        return errors
    previous_time = -1.0
    for index, point in enumerate(track):
        if not isinstance(point, Mapping):
            errors.append(f"crop point {index} is not an object")
            continue
        try:
            time_s = float(point["time_s"])
            center_x = float(point["center_x"])
            center_y = float(point["center_y"])
            crop = point["crop"]
            crop_x = float(crop["x"])
            crop_y = float(crop["y"])
            crop_w = float(crop["width"])
            crop_h = float(crop["height"])
        except (KeyError, TypeError, ValueError):
            errors.append(f"crop point {index} is malformed")
            continue
        if time_s < previous_time - 0.001 or time_s < 0 or time_s > duration + 0.05:
            errors.append(f"crop point {index} has an out-of-range timestamp")
        previous_time = time_s
        if not (0 <= center_x <= 1 and 0 <= center_y <= 1):
            errors.append(f"crop point {index} has an out-of-range center")
        if crop_w <= 0 or crop_h <= 0 or crop_x < 0 or crop_y < 0:
            errors.append(f"crop point {index} has invalid crop dimensions")
        if crop_x + crop_w > 1.00001 or crop_y + crop_h > 1.00001:
            errors.append(f"crop point {index} leaves source bounds")
    return errors


def write_visual_analysis(
    analysis: Mapping[str, Any], output_path: str | Path
) -> Path:
    errors = validate_visual_analysis(analysis)
    if errors:
        raise ValueError("invalid visual analysis: " + "; ".join(errors))
    destination = Path(output_path).expanduser().resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(dict(analysis), indent=2), encoding="utf-8")
    return destination


__all__ = [
    "VALID_MODES",
    "build_static_analysis",
    "run_visual_analysis",
    "validate_visual_analysis",
    "write_visual_analysis",
]
