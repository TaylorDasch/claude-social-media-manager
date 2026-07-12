"""ASS karaoke captions for 9:16 short-form video.

The renderer keeps captions in an adjacent ``.ass`` sidecar and burns that
exact file into the delivery MP4.  Transcript words may use source-absolute
timestamps or clip-relative timestamps; ``clip_start_s`` selects the former.
"""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping, Sequence


DEFAULT_PLAY_RES_X = 1080
DEFAULT_PLAY_RES_Y = 1920
DEFAULT_SAFE_MARGIN_BOTTOM = 430
CAPTION_FONT = "Avenir Next Condensed Heavy"
CAPTION_FONT_SIZE = 92
CAPTION_MIN_FONT_SIZE = 80
CAPTION_SIDE_MARGIN = 130
CAPTION_OUTLINE = 5
CAPTION_SPACING = 0.4
DEFAULT_MIN_WORDS_PER_CARD = 2
DEFAULT_MAX_WORDS_PER_CARD = 4
QA_MIN_WORDS_PER_EVENT = 1


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
Style: Karaoke,{CAPTION_FONT},{CAPTION_FONT_SIZE},&H00FFFFFF,&H00FFFFFF,&H00111111,&H70000000,0,0,0,0,100,100,{CAPTION_SPACING},0,1,{CAPTION_OUTLINE},2,2,{CAPTION_SIDE_MARGIN},{CAPTION_SIDE_MARGIN},{safe_margin_bottom},1

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
                re.fullmatch(r"[,\.]\d+(?:%?)(?:[,.!?;:]?)", text)
                and re.search(r"(?:\$?\d)$", str(previous["word"]))
            )
            or (
                bool(re.fullmatch(r"%(?:[,.!?;:]?)", text))
                and re.search(r"\d$", str(previous["word"]))
            )
            or (
                str(previous["word"]) in {"$", "£", "€"}
                and re.fullmatch(r"\d[\d,.]*", text)
            )
            or (
                bool(re.fullmatch(r"-[A-Z0-9]+(?:[,.!?;:]?)", text))
                and re.search(r"[A-Z0-9]$", str(previous["word"]))
            )
            or bool(re.fullmatch(r"[,.!?;:]+", text))
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
    safe_width_px: float,
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
        terminal = bool(re.search(r"[.!?;:]$", str(word["word"])))
        soft_punctuation = bool(re.search(r",$", str(word["word"])))
        card_duration = float(word["end"]) - float(current[0]["start"])
        if (
            terminal
            or len(current) >= max_words
            or (
                len(current) >= min_words
                and (soft_punctuation or pause >= 0.30 or card_duration >= 1.35)
            )
        ):
            groups.append(current)
            current = []
    if current:
        groups.append(current)

    # A greedy natural break can leave a one-word orphan. Rebalance the final
    # neighboring cards so normal captions stay strictly 2-4 words.
    index = 1
    while index < len(groups):
        if len(groups[index]) >= min_words:
            index += 1
            continue
        if re.search(r"[.!?;:]$", str(groups[index][-1]["word"])):
            index += 1
            continue
        if re.search(r"[.!?;:]$", str(groups[index - 1][-1]["word"])):
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

    # A fixed four-word card can remain wider than the safe box even with one
    # line break. Split it into two independently wrapped cards instead of
    # trusting word count as a proxy for rendered width.
    refined: list[list[dict[str, Any]]] = []
    for group in groups:
        _, widest = _best_line_break(group, font_size=CAPTION_FONT_SIZE)
        if len(group) == 4 and widest > safe_width_px:
            refined.extend([group[:2], group[2:]])
        else:
            refined.append(group)
    return refined


def _display_width(value: str) -> float:
    """Fallback width units when the exact local font cannot be loaded."""
    width = 0.0
    for character in value:
        if character in "MW@%&$":
            width += 1.35
        elif character in "I1.,:;'!|":
            width += 0.48
        elif character.isspace():
            width += 0.55
        else:
            width += 1.0
    return width


@lru_cache(maxsize=32)
def _caption_font(font_size: int) -> Any | None:
    try:
        from PIL import ImageFont

        # Fontconfig resolves Avenir Next Condensed Heavy to face index 8 on
        # Taylor's Mac, matching the exact family named in the ASS style.
        return ImageFont.truetype(
            "/System/Library/Fonts/Avenir Next Condensed.ttc",
            size=font_size,
            index=8,
        )
    except (ImportError, OSError):
        return None


def _text_width_px(value: str, *, font_size: int = CAPTION_FONT_SIZE) -> float:
    font = _caption_font(font_size)
    if font is not None:
        return float(font.getlength(value)) + max(0, len(value) - 1) * CAPTION_SPACING
    return _display_width(value) * font_size * 0.57


def _best_line_break(
    group: Sequence[dict[str, Any]],
    *,
    font_size: int,
) -> tuple[int, float]:
    words = [str(item["word"]) for item in group]
    full_width = _text_width_px(" ".join(words), font_size=font_size)
    if len(group) < 2:
        return 0, full_width
    options: list[tuple[float, float, int]] = []
    for index in range(1, len(words)):
        left = _text_width_px(" ".join(words[:index]), font_size=font_size)
        right = _text_width_px(" ".join(words[index:]), font_size=font_size)
        widest = max(left, right)
        cost = widest + abs(left - right) * 0.12
        options.append((cost, widest, index))
    _, widest, index = min(options)
    return index, min(full_width, widest)


def _line_break_index(
    group: Sequence[dict[str, Any]],
    *,
    max_lines: int,
    font_size: int,
    safe_width_px: float,
) -> int:
    if max_lines < 2 or len(group) < 2:
        return 0
    full_width = _text_width_px(
        " ".join(str(item["word"]) for item in group),
        font_size=font_size,
    )
    if len(group) < 4 and full_width <= safe_width_px:
        return 0
    return _best_line_break(group, font_size=font_size)[0]


def _caption_layout(
    group: Sequence[dict[str, Any]],
    *,
    max_lines: int,
    safe_width_px: float,
) -> tuple[int, int]:
    _, widest = _best_line_break(group, font_size=CAPTION_FONT_SIZE)
    font_size = CAPTION_FONT_SIZE
    if widest > safe_width_px:
        font_size = max(
            CAPTION_MIN_FONT_SIZE,
            int(CAPTION_FONT_SIZE * safe_width_px / widest),
        )
    line_break_at = _line_break_index(
        group,
        max_lines=max_lines,
        font_size=font_size,
        safe_width_px=safe_width_px,
    )
    return font_size, line_break_at


def _highlighted_text(
    group: Sequence[dict[str, Any]],
    *,
    active_index: int,
    font_size: int,
    line_break_at: int,
) -> str:
    pieces: list[str] = []

    for index, word in enumerate(group):
        prefix = r"\N" if line_break_at and index == line_break_at else ""
        if index == 0 and font_size != CAPTION_FONT_SIZE:
            prefix = f"{{\\fs{font_size}}}" + prefix
        color = r"{\c&H0000D7FF&}" if index == active_index else r"{\c&H00FFFFFF&}"
        pieces.append(f"{prefix}{color}{word['word']}")
    return " ".join(pieces).replace(r"\N ", r"\N")


def build_ass_captions(
    words: Sequence[Mapping[str, Any]],
    output_path: str | Path,
    *,
    clip_start_s: float = 0.0,
    clip_end_s: float | None = None,
    width: int = DEFAULT_PLAY_RES_X,
    height: int = DEFAULT_PLAY_RES_Y,
    min_words: int = DEFAULT_MIN_WORDS_PER_CARD,
    max_words: int = DEFAULT_MAX_WORDS_PER_CARD,
    max_lines: int = 2,
    safe_margin_bottom: int = DEFAULT_SAFE_MARGIN_BOTTOM,
) -> dict[str, Any]:
    """Write a safe-zone ASS karaoke sidecar and return serializable metadata.

    Typical transcript input uses source-absolute ``start``/``end`` seconds.
    Pass the exact clip span so captions are shifted to zero for the render.
    """
    if not 1 <= min_words <= max_words:
        raise ValueError("min_words must be between 1 and max_words")
    if max_words > 4:
        raise ValueError("premium short-form caption cards are limited to four words")
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
    safe_width_px = float(width - 2 * CAPTION_SIDE_MARGIN - 2 * CAPTION_OUTLINE)
    if safe_width_px <= 0:
        raise ValueError("caption side margins leave no readable width")
    groups = _group_words(
        prepared,
        min_words=min_words,
        max_words=max_words,
        safe_width_px=safe_width_px,
    )

    events: list[str] = []
    for group in groups:
        font_size, line_break_at = _caption_layout(
            group,
            max_lines=max_lines,
            safe_width_px=safe_width_px,
        )
        for active_index, word in enumerate(group):
            start = float(word["start"])
            if active_index + 1 < len(group):
                end = max(start + 0.01, float(group[active_index + 1]["start"]))
            else:
                end = max(start + 0.08, float(word["end"]))
            text = _highlighted_text(
                group,
                active_index=active_index,
                font_size=font_size,
                line_break_at=line_break_at,
            )
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
        "card_count": len(groups),
        "word_count": len(prepared),
        "min_words_per_card": min_words,
        "max_words_per_card": max_words,
        "max_lines": max_lines,
        "play_resolution": {"width": width, "height": height},
        "safe_margin_bottom": safe_margin_bottom,
        "style": {
            "font": CAPTION_FONT,
            "font_size": CAPTION_FONT_SIZE,
            "active_word_color": "#FFD700",
            "case": "uppercase",
            "safe_text_width_px": safe_width_px,
        },
    }


__all__ = ["build_ass_captions"]
