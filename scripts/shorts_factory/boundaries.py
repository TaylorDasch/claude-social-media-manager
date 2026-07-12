"""Sentence/pause boundary construction from normalized word timestamps."""

from __future__ import annotations

import re
from typing import Any

from .errors import ManifestError


_SENTENCE_END = re.compile(r"[.!?][\"')\]]*$")


def build_sentence_units(
    transcript: dict[str, Any],
    *,
    pause_seconds: float = 0.70,
    max_sentence_seconds: float = 20.0,
) -> list[dict[str, Any]]:
    """Snap clip-ready units to punctuation, silence, or a safety duration."""
    words = transcript.get("words")
    if not isinstance(words, list) or not words:
        raise ManifestError("cannot build boundaries without transcript words")
    if pause_seconds <= 0 or max_sentence_seconds <= 0:
        raise ValueError("boundary durations must be positive")

    units: list[dict[str, Any]] = []
    current: list[dict[str, Any]] = []
    gap_before = 0.0
    previous_end: float | None = None

    def flush(reason: str) -> None:
        nonlocal current, gap_before
        if not current:
            return
        unit_id = f"u{len(units) + 1:05d}"
        units.append(
            {
                "id": unit_id,
                "start": float(current[0]["start"]),
                "end": float(current[-1]["end"]),
                "text": " ".join(str(word["text"]) for word in current).strip(),
                "word_ids": [str(word["id"]) for word in current],
                "start_word_id": str(current[0]["id"]),
                "end_word_id": str(current[-1]["id"]),
                "gap_before_s": round(max(0.0, gap_before), 3),
                "boundary_reason": reason,
            }
        )
        current = []
        gap_before = 0.0

    for word in words:
        if not isinstance(word, dict):
            raise ManifestError("transcript words must be objects")
        start = float(word["start"])
        end = float(word["end"])
        gap = max(0.0, start - previous_end) if previous_end is not None else 0.0
        if current and gap >= pause_seconds:
            flush("pause")
        if not current:
            gap_before = gap
        current.append(word)
        elapsed = end - float(current[0]["start"])
        text = str(word.get("text", ""))
        if _SENTENCE_END.search(text):
            flush("punctuation")
        elif elapsed >= max_sentence_seconds:
            flush("max_duration")
        previous_end = end
    flush("eof")
    return units
