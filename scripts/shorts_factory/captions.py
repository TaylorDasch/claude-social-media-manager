"""ASS karaoke captions for 9:16 short-form video.

The renderer keeps captions in an adjacent ``.ass`` sidecar and burns that
exact file into the delivery MP4.  Transcript words may use source-absolute
timestamps or clip-relative timestamps; ``clip_start_s`` selects the former.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Mapping, Sequence


DEFAULT_PLAY_RES_X = 1080
DEFAULT_PLAY_RES_Y = 1920
DEFAULT_SAFE_MARGIN_BOTTOM = 430


def _ass_header(
    *,
    width: int,
    height: int,
    safe_margin_bottom: int,
) -> str:
    # Alignment 2 plus a 430px bottom margin keeps captions above the common
    # TikTok/Reels control and description zones.  Side margins protect text
    # from right-rail UI.  No logo or watermark is introduced here.
    return f"""[Script Info]
ScriptType: v4.00+
PlayResX: {width}
PlayResY: {height}
WrapStyle: 2
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Karaoke,Arial,78,&H00FFFFFF,&H0000D7FF,&H00111111,&H70000000,1,0,0,0,100,100,0,0,1,5,2,2,90,90,{safe_margin_bottom},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def _fmt_ass_time(seconds: float) -> str:
    seconds = max(0.0, seconds)
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    remainder = seconds - hours * 3600 - minutes * 60
    return f"{hours}:{minutes:02d}:{remainder:05.2f}"


def _clean_ass_text(value: object) -> str:
    text = str(value or "").strip()
    # ASS override blocks and explicit line breaks must only come from this
    # module.  Removing them also prevents transcript text from injecting
    # formatting or an accidental watermark-like overlay.
    text = text.replace("\\", "").replace("{", "").replace("}", "")
    return re.sub(r"\s+", " ", text).strip().upper()


def _normalise_words(
    words: Sequence[Mapping[str, Any]],
    *,
    clip_start_s: float,
    clip_end_s: float | None,
) -> list[dict[str, Any]]:
    normalised: list[dict[str, Any]] = []
    for raw in words:
        try:
            start = float(raw["start"])
            end = float(raw["end"])
        except (KeyError, TypeError, ValueError):
            continue
        if end <= start:
            continue
        if clip_end_s is not None and (end <= clip_start_s or start >= clip_end_s):
            continue
        text = _clean_ass_text(raw.get("word", raw.get("text", "")))
        if not text:
            continue
        relative_start = max(0.0, start - clip_start_s)
        relative_end = max(relative_start + 0.01, end - clip_start_s)
        if clip_end_s is not None:
            duration = max(0.0, clip_end_s - clip_start_s)
            relative_start = min(relative_start, duration)
            relative_end = min(relative_end, duration)
        if relative_end <= relative_start:
            continue
        normalised.append(
            {"word": text, "start": relative_start, "end": relative_end}
        )
    normalised.sort(key=lambda item: (item["start"], item["end"]))
    merged: list[dict[str, Any]] = []
    for item in normalised:
        text = str(item["word"])
        previous = merged[-1] if merged else None
        if previous is not None and (
            # Whisper commonly emits "$350" + ",000", "2" + ".39", or
            # "2.39" + "%" as separate timed tokens. They are one readable
            # unit and must never straddle caption cards.
            (
                re.fullmatch(r"[,\.]\d+", text)
                and re.search(r"(?:\$?\d)$", str(previous["word"]))
            )
            or (
                text == "%"
                and re.search(r"\d$", str(previous["word"]))
            )
            or (
                str(previous["word"]) in {"$", "£", "€"}
                and re.fullmatch(r"\d[\d,.]*", text)
            )
        ):
            previous["word"] = f"{previous['word']}{text}"
            previous["end"] = max(float(previous["end"]), float(item["end"]))
            continue
        merged.append(dict(item))
    return merged


def _balanced_sizes(total: int, *, minimum: int = 3, maximum: int = 5) -> list[int]:
    """Return group sizes in [minimum, maximum] whenever mathematically possible."""
    if total <= maximum:
        return [total]
    for groups in range((total + maximum - 1) // maximum, total // minimum + 1):
        base, remainder = divmod(total, groups)
        sizes = [base + (1 if index < remainder else 0) for index in range(groups)]
        if min(sizes) >= minimum and max(sizes) <= maximum:
            return sizes
    # Only totals of one or two cannot be represented with 3-5 word cards.
    return [min(maximum, total), *(_balanced_sizes(total - maximum) if total > maximum else [])]


def _group_words(
    words: Sequence[dict[str, Any]],
    *,
    min_words: int,
    max_words: int,
) -> list[list[dict[str, Any]]]:
    if not words:
        return []

    # First preserve natural punctuation/pauses where a valid card can end.
    groups: list[list[dict[str, Any]]] = []
    current: list[dict[str, Any]] = []
    for index, word in enumerate(words):
        current.append(word)
        next_word = words[index + 1] if index + 1 < len(words) else None
        pause = (
            float(next_word["start"]) - float(word["end"])
            if next_word is not None
            else 0.0
        )
        punctuation = bool(re.search(r"[.!?,;:]$", str(word["word"])))
        if len(current) >= max_words or (
            len(current) >= min_words and (punctuation or pause >= 0.55)
        ):
            groups.append(current)
            current = []
    if current:
        groups.append(current)

    # A greedy natural break can leave a one/two-word orphan.  Rebalance the
    # final neighboring cards so normal captions stay strictly 3-5 words.
    index = 1
    while index < len(groups):
        if len(groups[index]) >= min_words:
            index += 1
            continue
        combined = groups[index - 1] + groups[index]
        sizes = _balanced_sizes(len(combined), minimum=min_words, maximum=max_words)
        replacement: list[list[dict[str, Any]]] = []
        cursor = 0
        for size in sizes:
            replacement.append(combined[cursor : cursor + size])
            cursor += size
        groups[index - 1 : index + 1] = replacement
        index = max(1, index - 1)

    return groups


def _karaoke_text(group: Sequence[dict[str, Any]], *, max_lines: int) -> str:
    pieces: list[str] = []
    line_break_at = 0
    if max_lines >= 2 and len(group) >= 4:
        line_break_at = (len(group) + 1) // 2

    for index, word in enumerate(group):
        if index + 1 < len(group):
            # Include inter-word silence so highlighting remains aligned with
            # absolute word timestamps instead of running early after pauses.
            highlight_end = max(float(word["end"]), float(group[index + 1]["start"]))
        else:
            highlight_end = float(word["end"])
        duration_cs = max(1, round((highlight_end - float(word["start"])) * 100))
        prefix = r"\N" if line_break_at and index == line_break_at else ""
        pieces.append(f"{prefix}{{\\kf{duration_cs}}}{word['word']}")
    return " ".join(pieces).replace(r"\N ", r"\N")


def build_ass_captions(
    words: Sequence[Mapping[str, Any]],
    output_path: str | Path,
    *,
    clip_start_s: float = 0.0,
    clip_end_s: float | None = None,
    width: int = DEFAULT_PLAY_RES_X,
    height: int = DEFAULT_PLAY_RES_Y,
    min_words: int = 3,
    max_words: int = 5,
    max_lines: int = 2,
    safe_margin_bottom: int = DEFAULT_SAFE_MARGIN_BOTTOM,
) -> dict[str, Any]:
    """Write a safe-zone ASS karaoke sidecar and return serializable metadata.

    Typical transcript input uses source-absolute ``start``/``end`` seconds.
    Pass the exact clip span so captions are shifted to zero for the render.
    """
    if not 1 <= min_words <= max_words:
        raise ValueError("min_words must be between 1 and max_words")
    if max_words > 5:
        raise ValueError("short-form caption cards are limited to five words")
    if not 1 <= max_lines <= 2:
        raise ValueError("short-form captions support one or two lines")
    if width <= 0 or height <= 0:
        raise ValueError("caption play resolution must be positive")
    if safe_margin_bottom < 0 or safe_margin_bottom >= height:
        raise ValueError("safe_margin_bottom must fit inside the play resolution")

    destination = Path(output_path).expanduser().resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    prepared = _normalise_words(
        words,
        clip_start_s=float(clip_start_s),
        clip_end_s=float(clip_end_s) if clip_end_s is not None else None,
    )
    groups = _group_words(prepared, min_words=min_words, max_words=max_words)

    events: list[str] = []
    for group in groups:
        start = float(group[0]["start"])
        end = max(start + 0.20, float(group[-1]["end"]))
        text = _karaoke_text(group, max_lines=max_lines)
        events.append(
            f"Dialogue: 0,{_fmt_ass_time(start)},{_fmt_ass_time(end)},"
            f"Karaoke,,0,0,0,,{text}"
        )

    destination.write_text(
        _ass_header(
            width=width,
            height=height,
            safe_margin_bottom=safe_margin_bottom,
        )
        + "\n".join(events)
        + "\n",
        encoding="utf-8",
    )
    return {
        "path": str(destination),
        "event_count": len(events),
        "word_count": len(prepared),
        "min_words_per_card": min_words,
        "max_words_per_card": max_words,
        "max_lines": max_lines,
        "play_resolution": {"width": width, "height": height},
        "safe_margin_bottom": safe_margin_bottom,
    }


__all__ = ["build_ass_captions"]
