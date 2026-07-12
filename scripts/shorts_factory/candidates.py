"""Overlapping, duration-diverse candidate windows on semantic boundaries."""

from __future__ import annotations

import hashlib
import re
from collections import defaultdict, deque
from typing import Any, Iterable


WINDOW_TARGETS: tuple[tuple[str, float], ...] = (
    ("punchy", 22.0),
    ("standard", 38.0),
    ("explainer", 58.0),
    ("complete", 70.0),
    ("deep", 78.0),
)

_STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "but",
    "by",
    "for",
    "from",
    "i",
    "if",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "so",
    "that",
    "the",
    "this",
    "to",
    "we",
    "with",
    "you",
    "your",
}
_CONTRARIAN = {
    "actually",
    "avoid",
    "but",
    "don't",
    "instead",
    "mistake",
    "never",
    "problem",
    "truth",
    "warning",
    "worst",
}


def _tokens(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9']+", text.lower())
        if len(token) > 2 and token not in _STOPWORDS
    }


def _semantic_coherence(units: list[dict[str, Any]]) -> float:
    if len(units) <= 1:
        return 1.0
    scores: list[float] = []
    for left, right in zip(units, units[1:]):
        a, b = _tokens(str(left["text"])), _tokens(str(right["text"]))
        if not a or not b:
            scores.append(0.35)
        else:
            scores.append(len(a & b) / len(a | b))
    # Consecutive speech often uses pronouns instead of repeated nouns.  A
    # modest floor prevents lexical sparsity from masquerading as incoherence.
    return round(min(1.0, 0.35 + (sum(scores) / len(scores))), 4)


def _hook_signals(text: str) -> list[str]:
    opening = " ".join(text.split()[:18]).lower()
    signals: list[str] = []
    if re.search(r"(?:\$\s?\d|\b\d+(?:\.\d+)?%?\b)", opening):
        signals.append("specific_number")
    if _tokens(opening) & _CONTRARIAN:
        signals.append("contradiction_or_warning")
    if re.search(r"\b(if you|for (?:buyers|families|agents|investors)|moving to)\b", opening):
        signals.append("named_audience")
    if "?" in opening:
        signals.append("question")
    return signals


def _candidate_id(start_word_id: str, end_word_id: str, strategy: str) -> str:
    value = f"{start_word_id}:{end_word_id}:{strategy}".encode("utf-8")
    return f"cand-{hashlib.sha1(value).hexdigest()[:12]}"


def generate_overlapping_candidates(
    units: list[dict[str, Any]],
    *,
    min_seconds: float = 10.0,
    max_seconds: float = 90.0,
    targets: Iterable[tuple[str, float]] = WINDOW_TARGETS,
    topic_pause_seconds: float = 1.40,
) -> list[dict[str, Any]]:
    """Generate windows from every sentence start, not fixed chunks.

    Each start is tested against multiple duration/arc shapes. Endpoints are
    selected from complete sentence/pause units, with penalties for crossing a
    long topic pause. This yields deliberately overlapping alternatives for the
    model to compare while retaining beginning/middle/end diversity.
    """
    if not units:
        return []
    if min_seconds <= 0 or max_seconds <= min_seconds:
        raise ValueError("candidate duration bounds are invalid")

    output: list[dict[str, Any]] = []
    seen_ranges: set[tuple[str, str, str]] = set()
    target_list = list(targets)
    for start_index, start_unit in enumerate(units):
        possible: list[tuple[int, float]] = []
        for end_index in range(start_index, len(units)):
            duration = float(units[end_index]["end"]) - float(start_unit["start"])
            if duration > max_seconds:
                break
            if duration >= min_seconds:
                possible.append((end_index, duration))
        if not possible:
            continue

        for strategy, target in target_list:
            def endpoint_cost(option: tuple[int, float]) -> float:
                end_index, duration = option
                window = units[start_index : end_index + 1]
                long_pauses = sum(
                    1
                    for unit in window[1:]
                    if float(unit.get("gap_before_s", 0)) >= topic_pause_seconds
                )
                end_bonus = (
                    -0.08
                    if units[end_index].get("boundary_reason") in {"punctuation", "eof"}
                    else 0.0
                )
                semantic_bonus = -0.18 * _semantic_coherence(window)
                return abs(duration - target) / max(target, 1.0) + long_pauses * 0.32 + end_bonus + semantic_bonus

            end_index, duration = min(possible, key=endpoint_cost)
            end_unit = units[end_index]
            range_key = (
                str(start_unit["start_word_id"]),
                str(end_unit["end_word_id"]),
                strategy,
            )
            if range_key in seen_ranges:
                continue
            seen_ranges.add(range_key)
            window = units[start_index : end_index + 1]
            text = " ".join(str(unit["text"]) for unit in window).strip()
            output.append(
                {
                    "id": _candidate_id(*range_key),
                    "start": round(float(start_unit["start"]), 3),
                    "end": round(float(end_unit["end"]), 3),
                    "duration_s": round(duration, 3),
                    "start_word_id": start_unit["start_word_id"],
                    "end_word_id": end_unit["end_word_id"],
                    "unit_ids": [unit["id"] for unit in window],
                    "strategy": strategy,
                    "target_duration_s": target,
                    "text": text,
                    "semantic_coherence": _semantic_coherence(window),
                    "hook_signals": _hook_signals(text),
                    "crossed_topic_pauses": sum(
                        1
                        for unit in window[1:]
                        if float(unit.get("gap_before_s", 0)) >= topic_pause_seconds
                    ),
                }
            )
    return output


def preselect_diverse_candidates(
    candidates: list[dict[str, Any]],
    *,
    limit: int = 64,
    timeline_bucket_seconds: float = 60.0,
) -> list[dict[str, Any]]:
    """Round-robin timeline + duration strategies before paid model scoring."""
    if limit <= 0:
        return []
    groups: dict[tuple[int, str], list[dict[str, Any]]] = defaultdict(list)
    for candidate in candidates:
        bucket = int(float(candidate["start"]) // timeline_bucket_seconds)
        groups[(bucket, str(candidate["strategy"]))].append(candidate)
    queues: deque[deque[dict[str, Any]]] = deque()
    for key in sorted(groups):
        ranked = sorted(
            groups[key],
            key=lambda candidate: (
                -len(candidate.get("hook_signals", [])),
                -float(candidate.get("semantic_coherence", 0)),
                abs(
                    float(candidate["duration_s"])
                    - float(candidate["target_duration_s"])
                ),
                float(candidate["start"]),
            ),
        )
        queues.append(deque(ranked))

    selected: list[dict[str, Any]] = []
    while queues and len(selected) < limit:
        queue = queues.popleft()
        if queue:
            selected.append(queue.popleft())
        if queue:
            queues.append(queue)
    return selected


def time_iou(left: dict[str, Any], right: dict[str, Any]) -> float:
    intersection = max(
        0.0,
        min(float(left["end"]), float(right["end"]))
        - max(float(left["start"]), float(right["start"])),
    )
    union = max(float(left["end"]), float(right["end"])) - min(
        float(left["start"]), float(right["start"])
    )
    return intersection / union if union > 0 else 0.0


def text_similarity(left: str, right: str) -> float:
    a, b = _tokens(left), _tokens(right)
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)
