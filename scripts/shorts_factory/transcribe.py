"""Pluggable word-timestamp transcription with normalized JSON reuse."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any, Protocol

from .errors import ManifestError, ShortsFactoryError
from .storage import atomic_write_json, read_json, utc_now


TRANSCRIPT_SCHEMA_VERSION = "shorts-transcript/v1"


class Transcriber(Protocol):
    name: str

    def transcribe(
        self,
        audio_path: Path,
        *,
        model_name: str,
        language: str | None,
    ) -> dict[str, Any]: ...


class FasterWhisperTranscriber:
    name = "faster-whisper"

    def __init__(self, *, device: str = "auto", compute_type: str = "int8") -> None:
        self.device = device
        self.compute_type = compute_type

    def transcribe(
        self,
        audio_path: Path,
        *,
        model_name: str,
        language: str | None,
    ) -> dict[str, Any]:
        try:
            from faster_whisper import WhisperModel
        except ImportError as exc:
            raise ShortsFactoryError(
                "faster-whisper is not installed in this Python runtime. "
                "Use the existing Vega clipper virtualenv or pass --transcript-json."
            ) from exc

        model = WhisperModel(
            model_name,
            device=self.device,
            compute_type=self.compute_type,
        )
        segment_iter, info = model.transcribe(
            str(audio_path),
            language=language,
            word_timestamps=True,
            vad_filter=True,
            beam_size=5,
        )
        segments: list[dict[str, Any]] = []
        for segment in segment_iter:
            segments.append(
                {
                    "start": float(segment.start),
                    "end": float(segment.end),
                    "text": segment.text.strip(),
                    "words": [
                        {
                            "start": float(word.start),
                            "end": float(word.end),
                            "text": str(word.word).strip(),
                            "probability": float(word.probability or 0.0),
                        }
                        for word in (segment.words or [])
                        if word.start is not None and word.end is not None
                    ],
                }
            )
        return {
            "language": getattr(info, "language", language or "unknown"),
            "duration_s": float(getattr(info, "duration", 0.0) or 0.0),
            "segments": segments,
        }


_TRANSCRIBERS: dict[str, Transcriber] = {
    "faster-whisper": FasterWhisperTranscriber(),
}


def register_transcriber(name: str, transcriber: Transcriber) -> None:
    if not name.strip():
        raise ValueError("transcriber name cannot be empty")
    _TRANSCRIBERS[name] = transcriber


def get_transcriber(name: str) -> Transcriber:
    try:
        return _TRANSCRIBERS[name]
    except KeyError as exc:
        raise ShortsFactoryError(
            f"unknown transcriber {name!r}; available: {sorted(_TRANSCRIBERS)}"
        ) from exc


def _finite_number(value: Any, field: str) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ManifestError(f"transcript {field} must be numeric, got {value!r}") from exc
    if not math.isfinite(number) or number < 0:
        raise ManifestError(f"transcript {field} must be finite and >= 0")
    return number


def _word_text(value: dict[str, Any]) -> str:
    text = value.get("text", value.get("word", ""))
    return str(text).strip()


def _synthetic_words(segment: dict[str, Any]) -> list[dict[str, Any]]:
    text_words = str(segment.get("text", "")).split()
    if not text_words:
        return []
    start = _finite_number(segment.get("start", 0), "segment.start")
    end = _finite_number(segment.get("end", start), "segment.end")
    if end <= start:
        end = start + max(0.2, len(text_words) * 0.25)
    step = (end - start) / len(text_words)
    return [
        {
            "start": start + index * step,
            "end": start + (index + 1) * step,
            "text": text,
            "probability": None,
            "synthetic_timing": True,
        }
        for index, text in enumerate(text_words)
    ]


def normalize_transcript(
    raw: dict[str, Any],
    *,
    audio_sha256: str,
    provider: str,
    model_name: str,
    reused_from: str | None = None,
) -> dict[str, Any]:
    """Normalize common Whisper JSON shapes into stable word IDs/timestamps."""
    raw_segments = raw.get("segments")
    if raw_segments is None and isinstance(raw.get("words"), list):
        raw_segments = [
            {
                "start": raw["words"][0].get("start", 0) if raw["words"] else 0,
                "end": raw["words"][-1].get("end", 0) if raw["words"] else 0,
                "text": raw.get("text", ""),
                "words": raw["words"],
            }
        ]
    if not isinstance(raw_segments, list) or not raw_segments:
        raise ManifestError("transcript must contain at least one segment")

    normalized_segments: list[dict[str, Any]] = []
    normalized_words: list[dict[str, Any]] = []
    previous_end = 0.0
    for segment_index, segment_value in enumerate(raw_segments, start=1):
        if not isinstance(segment_value, dict):
            raise ManifestError("every transcript segment must be an object")
        segment_words = segment_value.get("words")
        if not isinstance(segment_words, list) or not segment_words:
            segment_words = _synthetic_words(segment_value)
        segment_id = f"s{segment_index:05d}"
        word_ids: list[str] = []
        for raw_word in segment_words:
            if not isinstance(raw_word, dict):
                raise ManifestError("every transcript word must be an object")
            text = _word_text(raw_word)
            if not text:
                continue
            start = _finite_number(raw_word.get("start"), "word.start")
            end = _finite_number(raw_word.get("end"), "word.end")
            if end < start:
                raise ManifestError(f"word end precedes start for {text!r}")
            if start + 0.001 < previous_end:
                overlap = previous_end - start
                if overlap > 0.25:
                    raise ManifestError(
                        f"word timestamps are not monotonic near {text!r}: "
                        f"{start} < {previous_end}"
                    )
                # Whisper occasionally overlaps adjacent word boxes by a few
                # frames. Snap only that small overlap; never reorder words.
                start = previous_end
                end = max(end, start)
            word_id = f"w{len(normalized_words) + 1:07d}"
            probability = raw_word.get("probability")
            normalized = {
                "id": word_id,
                "segment_id": segment_id,
                "start": round(start, 3),
                "end": round(end, 3),
                "text": text,
                "probability": (
                    round(float(probability), 5) if probability is not None else None
                ),
                "synthetic_timing": bool(raw_word.get("synthetic_timing", False)),
            }
            normalized_words.append(normalized)
            word_ids.append(word_id)
            previous_end = end
        if not word_ids:
            continue
        first = normalized_words[-len(word_ids)]
        last = normalized_words[-1]
        normalized_segments.append(
            {
                "id": segment_id,
                "start": first["start"],
                "end": last["end"],
                "text": " ".join(
                    word["text"] for word in normalized_words[-len(word_ids) :]
                ),
                "word_ids": word_ids,
            }
        )

    if not normalized_words:
        raise ManifestError("transcript contained no usable words")
    duration = max(
        _finite_number(raw.get("duration_s", raw.get("duration", 0)), "duration"),
        normalized_words[-1]["end"],
    )
    return {
        "schema_version": TRANSCRIPT_SCHEMA_VERSION,
        "created_at": utc_now(),
        "provider": provider,
        "model": model_name,
        "language": str(raw.get("language", "unknown")),
        "audio_sha256": audio_sha256,
        "reused_from": reused_from,
        "duration_s": round(duration, 3),
        "text": " ".join(word["text"] for word in normalized_words),
        "segments": normalized_segments,
        "words": normalized_words,
    }


def validate_normalized_transcript(transcript: dict[str, Any]) -> None:
    if transcript.get("schema_version") != TRANSCRIPT_SCHEMA_VERSION:
        raise ManifestError(
            f"unsupported transcript schema: {transcript.get('schema_version')!r}"
        )
    words = transcript.get("words")
    if not isinstance(words, list) or not words:
        raise ManifestError("normalized transcript has no words")
    expected_ids = [f"w{index:07d}" for index in range(1, len(words) + 1)]
    actual_ids = [word.get("id") for word in words if isinstance(word, dict)]
    if actual_ids != expected_ids:
        raise ManifestError("normalized transcript word IDs are not contiguous")


def transcribe_or_reuse(
    *,
    audio_path: Path,
    audio_sha256: str,
    destination: Path,
    backend_name: str = "faster-whisper",
    model_name: str = "large-v3-turbo",
    language: str | None = "en",
    transcript_json: Path | None = None,
    force: bool = False,
) -> tuple[dict[str, Any], bool]:
    """Return `(transcript, reused)` and persist a normalized artifact."""
    if destination.exists() and not force and transcript_json is None:
        existing = read_json(destination)
        validate_normalized_transcript(existing)
        if existing.get("audio_sha256") == audio_sha256:
            return existing, True

    if transcript_json is not None:
        transcript_json = transcript_json.expanduser().resolve()
        raw = read_json(transcript_json)
        if raw.get("schema_version") == TRANSCRIPT_SCHEMA_VERSION:
            # Re-normalize to ensure IDs/timestamps follow this version's contract.
            word_by_id = {
                word.get("id"): word
                for word in raw.get("words", [])
                if isinstance(word, dict)
            }
            raw_for_normalize = {
                **raw,
                "segments": [
                    {
                        **segment,
                        "words": [
                            word_by_id[word_id]
                            for word_id in segment.get("word_ids", [])
                            if word_id in word_by_id
                        ],
                    }
                    for segment in raw.get("segments", [])
                ],
            }
        else:
            raw_for_normalize = raw
        normalized = normalize_transcript(
            raw_for_normalize,
            audio_sha256=audio_sha256,
            provider="transcript-json",
            model_name=str(raw.get("model", model_name)),
            reused_from=str(transcript_json),
        )
        atomic_write_json(destination, normalized)
        return normalized, True

    backend = get_transcriber(backend_name)
    raw = backend.transcribe(
        audio_path,
        model_name=model_name,
        language=language,
    )
    normalized = normalize_transcript(
        raw,
        audio_sha256=audio_sha256,
        provider=backend.name,
        model_name=model_name,
    )
    atomic_write_json(destination, normalized)
    return normalized, False
