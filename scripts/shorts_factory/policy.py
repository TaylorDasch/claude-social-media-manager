"""Taylor-specific thresholds, claims, dedupe, and platform eligibility."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .candidates import text_similarity, time_iou


PROJECT_ROOT = Path(__file__).resolve().parents[2]
QUALITY_GATES_PATH = PROJECT_ROOT / "governance" / "QUALITY-GATES.md"
MIN_TOPIC_PURITY = 90

_NUMBER_CLAIM = re.compile(
    r"(?:\$\s?\d[\d,.]*|\b\d+(?:\.\d+)?\s?(?:%|percent|minutes?|miles?|"
    r"dollars?|homes?|years?|months?|days?)\b)",
    re.IGNORECASE,
)
_HIGH_CERTAINTY = re.compile(
    r"\b(?:best|safest|cheapest|always|never|guaranteed|everyone|nobody)\b",
    re.IGNORECASE,
)
_SENSITIVE = re.compile(
    r"\b(?:crime|safe|school district|school rating|interest rate|tax rate|hoa)\b",
    re.IGNORECASE,
)
_GENERIC_OPENERS = (
    "hey guys",
    "what's up",
    "welcome to",
    "today we're",
    "today we are",
    "in this video",
)
_STRUCTURAL_WARNING = re.compile(
    r"\b(?:cuts? off|mid[- ]thought|midstream|starts? mid(?:stream|-thought)?|"
    r"depends? on prior context|needs? prior context|ends? before|stops? before|"
    r"ends? on (?:a )?(?:tease|cliffhanger)|"
    r"incomplete|unfinished|truncat(?:ed|ion)|continues? beyond|"
    r"only (?:the )?setup|no payoff|lacks? (?:a )?(?:payoff|conclusion)|"
    r"does not (?:reach|include).*?payoff|(?:payoff|answer|arc) is partial|"
    r"partial (?:payoff|answer|arc)|too broad for (?:a |one )?single short|"
    r"needs? (?:more )?trimm?ing|without trimm?ing)\b",
    re.IGNORECASE,
)


def load_banned_phrases(path: Path = QUALITY_GATES_PATH) -> list[str]:
    """Read Gate 1 at runtime; governance remains the source of truth."""
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8", errors="ignore")
    match = re.search(r"## GATE 1:.*?(?=\n## GATE 2:|\Z)", text, re.DOTALL)
    if not match:
        return []
    phrases: list[str] = []
    for line in match.group(0).splitlines():
        table = re.match(r"\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|", line)
        if not table:
            continue
        banned, replacement = table.group(1).strip(), table.group(2).strip()
        if banned.lower() == "banned" or set(banned) <= set("-: "):
            continue
        if banned.casefold() == replacement.casefold():
            continue
        phrases.append(banned.casefold())
    phrases.extend(
        value.casefold()
        for value in re.findall(
            r'^-\s*"([^"]+)"', match.group(0), flags=re.MULTILINE
        )
    )
    # Entity consistency: Taylor is an agent, not a broker.
    phrases.append("broker")
    return sorted(set(phrases))


def find_banned_phrases(text: str, phrases: list[str] | None = None) -> list[str]:
    lowered = text.casefold()
    found: list[str] = []
    for phrase in phrases if phrases is not None else load_banned_phrases():
        pattern = rf"(?<!\w){re.escape(phrase)}(?!\w)"
        if re.search(pattern, lowered):
            found.append(phrase)
    return found


def publication_copy(clip: dict[str, Any]) -> tuple[str, str]:
    """Return the exact caption/title pair that approval must checksum-lock."""
    caption = next(
        (
            value.strip()
            for field in ("social_caption", "caption", "post_copy", "summary", "hook")
            if isinstance((value := clip.get(field)), str) and value.strip()
        ),
        "",
    )
    title = next(
        (
            value.strip()[:100]
            for field in ("youtube_title", "hook", "summary")
            if isinstance((value := clip.get(field)), str) and len(value.strip()) >= 2
        ),
        "",
    )
    if not caption or not title:
        raise ValueError("clip has no usable publication caption/title")
    return caption, title


def unresolved_claims(clip: dict[str, Any]) -> list[dict[str, Any]]:
    claims = clip.get("claims")
    if not isinstance(claims, list):
        return []
    unresolved: list[dict[str, Any]] = []
    for claim in claims:
        if not isinstance(claim, dict):
            continue
        severity = str(claim.get("severity", "review"))
        source_status = str(claim.get("source_status", "unverified"))
        if severity in {"verify", "high_risk"} and source_status not in {
            "verified",
            "waived_by_taylor",
        }:
            unresolved.append(claim)
    return unresolved


def heuristic_claim_flags(text: str) -> list[dict[str, str]]:
    """Surface verification work deterministically even if Claude misses it."""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    flags: list[dict[str, str]] = []
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        if _NUMBER_CLAIM.search(sentence):
            flags.append(
                {
                    "text": sentence,
                    "type": "numeric_claim",
                    "severity": "verify",
                    "source_status": "unverified",
                }
            )
        if _SENSITIVE.search(sentence):
            flags.append(
                {
                    "text": sentence,
                    "type": "sensitive_local_claim",
                    "severity": "high_risk",
                    "source_status": "unverified",
                }
            )
        elif _HIGH_CERTAINTY.search(sentence):
            flags.append(
                {
                    "text": sentence,
                    "type": "absolute_or_comparative_claim",
                    "severity": "review",
                    "source_status": "unverified",
                }
            )
    unique: dict[tuple[str, str], dict[str, str]] = {}
    for flag in flags:
        unique[(flag["text"].casefold(), flag["type"])] = flag
    return list(unique.values())


def platform_eligibility(
    *,
    duration_s: float,
    lane: str,
    source_kind: str,
    hard_rejections: list[str],
) -> dict[str, dict[str, Any]]:
    base_reasons = list(hard_rejections)

    def result(eligible: bool, reasons: list[str]) -> dict[str, Any]:
        return {"eligible": eligible, "reasons": reasons}

    instagram_reasons = list(base_reasons)
    if not 10 <= duration_s <= 60:
        instagram_reasons.append("Factory review duration must be 10-60 seconds.")
    youtube_reasons = list(base_reasons)
    if not 10 <= duration_s <= 60:
        youtube_reasons.append("Factory YouTube Short duration must be 10-60 seconds.")
    facebook_reasons = list(base_reasons)
    if not 10 <= duration_s <= 60:
        facebook_reasons.append("Factory Facebook Reel duration must be 10-60 seconds.")

    tiktok_reasons = list(base_reasons)
    if source_kind == "youtube_long":
        tiktok_reasons.append(
            "Repository Gate 14 prohibits repurposing long-form YouTube content to TikTok."
        )
    if lane == "investor":
        tiktok_reasons.append("Investor content is prohibited on TikTok outputs.")
    if not 10 <= duration_s <= 60:
        tiktok_reasons.append("Repository TikTok format requires 10-60 seconds.")

    return {
        "instagram_reels": result(not instagram_reasons, instagram_reasons),
        "youtube_shorts": result(not youtube_reasons, youtube_reasons),
        "facebook_reels": result(not facebook_reasons, facebook_reasons),
        "tiktok": result(not tiktok_reasons, tiktok_reasons),
    }


def assess_ranked_candidate(
    ranked: dict[str, Any],
    *,
    source_kind: str,
) -> dict[str, Any]:
    candidate = ranked["candidate"]
    evaluation = ranked["evaluation"]
    rerank = ranked["rerank"]
    text = str(candidate["text"])
    duration = float(candidate["duration_s"])
    hard_rejections: list[str] = []
    if not 10 <= duration <= 60:
        hard_rejections.append("Duration is outside the 10-60 second review range.")
    if not text.strip():
        hard_rejections.append("Transcript is empty.")
    banned = find_banned_phrases(text)
    if banned:
        hard_rejections.append(f"Governance-banned language: {', '.join(banned)}")

    warnings = list(evaluation.get("warnings", []))
    structural_evidence = [
        *warnings,
        *evaluation.get("reasons", []),
        rerank.get("selection_reason", ""),
    ]
    structural_warnings = [
        evidence
        for evidence in structural_evidence
        if _STRUCTURAL_WARNING.search(str(evidence))
    ]
    if structural_warnings:
        hard_rejections.append(
            "Semantic evaluator flagged an incomplete or context-dependent cut: "
            + " | ".join(str(warning) for warning in structural_warnings)
        )
    topic_axes = evaluation.get("topic_axes")
    topic_purity = int(evaluation.get("topic_purity", 0))
    if not isinstance(topic_axes, list) or len(topic_axes) != 1:
        labels = ", ".join(str(value) for value in topic_axes or []) or "none"
        hard_rejections.append(
            f"One-subject gate requires exactly one topic axis; found: {labels}."
        )
    if topic_purity < MIN_TOPIC_PURITY:
        hard_rejections.append(
            f"Topic purity {topic_purity} is below the required {MIN_TOPIC_PURITY}."
        )
    if evaluation.get("payoff_complete") is not True:
        hard_rejections.append(
            "The clip does not complete its stated promise and payoff."
        )
    opening = " ".join(text.split()[:12]).casefold()
    if opening.startswith(_GENERIC_OPENERS):
        warnings.append("Generic setup opener weakens the first three seconds.")

    model_claims = [
        {**claim, "source_status": "unverified", "origin": "claude"}
        for claim in evaluation.get("claim_flags", [])
    ]
    claims = heuristic_claim_flags(text) + model_claims
    unique_claims: dict[tuple[str, str], dict[str, Any]] = {}
    for claim in claims:
        unique_claims[(str(claim.get("text", "")).casefold(), str(claim.get("type")))] = claim
    claims = list(unique_claims.values())
    if claims:
        warnings.append(f"{len(claims)} factual claim(s) require source verification.")

    lane = str(evaluation["lane"])
    return {
        **ranked,
        "hard_rejections": hard_rejections,
        "warnings": sorted(set(warnings)),
        "claims": claims,
        "platform_eligibility": platform_eligibility(
            duration_s=duration,
            lane=lane,
            source_kind=source_kind,
            hard_rejections=hard_rejections,
        ),
        "passes_threshold": not hard_rejections and bool(evaluation["standalone"]),
        "model_keep": bool(rerank["keep"]),
    }


def deduplicate_ranked(
    ranked: list[dict[str, Any]],
    *,
    source_kind: str,
    minimum_score: int = 60,
    top_n: int = 8,
    time_iou_threshold: float = 0.20,
    text_similarity_threshold: float = 0.75,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Apply hard thresholds, then keep the best non-duplicate moments."""
    assessed = [
        assess_ranked_candidate(item, source_kind=source_kind) for item in ranked
    ]
    assessed.sort(
        key=lambda item: (
            item["rerank"]["final_score"],
            item["evaluation"]["scores"]["arc_payoff"],
            item["evaluation"]["total_score"],
            item["evaluation"]["scores"]["hook_strength"],
        ),
        reverse=True,
    )
    selected: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    for position, item in enumerate(assessed):
        score = int(item["rerank"]["final_score"])
        reasons: list[str] = []
        if score < minimum_score:
            reasons.append(f"Final score {score} is below threshold {minimum_score}.")
        if not item["passes_threshold"]:
            reasons.extend(item["hard_rejections"] or ["Clip is not standalone."])
        if not item["model_keep"]:
            reasons.append("Independent reranker marked this candidate as not keepable.")

        duplicate_of: str | None = None
        if not reasons:
            for keeper in selected:
                overlap = time_iou(item["candidate"], keeper["candidate"])
                similarity = text_similarity(
                    str(item["candidate"]["text"]),
                    str(keeper["candidate"]["text"]),
                )
                if overlap >= time_iou_threshold or similarity >= text_similarity_threshold:
                    duplicate_of = str(keeper["candidate"]["id"])
                    reasons.append(
                        f"Duplicate of {duplicate_of} (time IoU={overlap:.2f}, "
                        f"text similarity={similarity:.2f})."
                    )
                    break
        if reasons:
            rejected.append({**item, "selection_reasons": reasons, "duplicate_of": duplicate_of})
            continue
        selected.append({**item, "selection_reasons": [], "duplicate_of": None})
        if len(selected) >= top_n:
            # Preserve the rest in the audit instead of silently dropping them.
            rejected.extend(
                {**value, "selection_reasons": [f"Top-{top_n} review limit reached."], "duplicate_of": None}
                for value in assessed[position + 1 :]
            )
            break
    return selected, rejected
