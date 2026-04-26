"""Compliance + voice filters.

Codifies (a subset of) governance/QUALITY-GATES.md as Python checks. Reads
`data/voice-rubric.json` at runtime so banned-word updates propagate.

Severity: "hard" (blocks approval) | "soft" (warns only).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from .models import ComplianceFlag, Draft

REPO_ROOT = Path(__file__).resolve().parent.parent
VOICE_RUBRIC = REPO_ROOT / "data" / "voice-rubric.json"

# Hardcoded HARD gates from QUALITY-GATES.md (Gate 1, 2, 14, etc.)
HARD_BANNED_PHRASES = {
    "turnkey", "dream home", "white glove", "nestled", "charming",
    "stunning", "sought-after", "boasts", "utilize", "comprehensive",
    "furthermore", "moreover", "leverage", "unparalleled",
    "in today's market", "vibrant community", "hidden gem",
    "welcome home", "turn-key",
    # Banned hooks/openers
    "let me tell you about", "in this article we'll explore", "in conclusion",
    # Location naming
    "fort cavazos",
}

# Guaranteed-return language (real estate compliance risk)
GUARANTEE_TERMS = {
    "guaranteed return", "guaranteed appreciation", "guaranteed profit",
    "risk-free", "riskless", "100% safe investment", "can't lose",
    "always appreciates", "always goes up",
}

# Fair-housing steering flags (SOFT — needs context review)
STEERING_PATTERNS = (
    r"\bperfect (?:for|neighborhood for)\s+(?:families|kids|professionals|young)",
    r"\bbest (?:for|neighborhood for)\s+(?:families|kids|professionals|young)",
    r"\bfamily[- ]friendly\s+neighborhood",
    r"\bsafest\s+(?:neighborhood|area|part of town)",
    r"\b(?:ideal|suited)\s+for\s+young\s+(?:families|professionals)",
)

# TikTok-investor leak (Gate 14): never investor content on TikTok outputs
TIKTOK_INVESTOR_TERMS = (
    "cap rate", "dscr", "cash-on-cash", "cash on cash", "rental comp",
    "1% rule", "one percent rule", "brrrr", "pro forma", "proforma",
    "rental income", "roi on rental", "cash flow analysis",
    "buy-and-hold", "long-term rental", "mtr analysis", "ltr analysis",
)

# School claims without verification language (SOFT)
SCHOOL_CLAIM_PATTERNS = (
    r"\b(?:great|best|top|excellent|amazing|incredible)\s+schools?\b",
    r"\bschool\s+district\s+is\s+(?:great|amazing|excellent)",
)
SCHOOL_DISCLAIMER_CUES = ("verify by address", "schools by address", "check boundaries")

# Tax claims without "verify current" cue (SOFT)
TAX_RATE_PATTERN = r"\b(?:tax\s+rate|property\s+tax|effective\s+tax)\b"
TAX_DISCLAIMER_CUES = ("verify current", "check current rate", "varies by", "verify with appraisal")

ENTITY_REQUIRED_PHRASES = ("Taylor Dasch with EG Realty",)
BROKER_RULE_BAD = re.compile(r"\bTaylor\s+(?:is|as)\s+(?:a\s+)?broker\b", re.IGNORECASE)


def _load_voice_rubric() -> dict:
    if VOICE_RUBRIC.exists():
        try:
            return json.loads(VOICE_RUBRIC.read_text())
        except Exception:
            return {}
    return {}


def _find_all(text: str, phrase: str) -> list[int]:
    """Return 1-based line numbers where phrase appears (case-insensitive)."""
    hits = []
    low = text.lower()
    needle = phrase.lower()
    for i, line in enumerate(low.split("\n"), start=1):
        if needle in line:
            hits.append(i)
    return hits


def check_text(text: str, platform: str | None = None,
               public_facing: bool = True) -> list[ComplianceFlag]:
    """Run all checks against a raw text body. Returns list of flags.

    `public_facing` controls entity-declaration check (SKIP for SMS/DM).
    """
    flags: list[ComplianceFlag] = []
    if not text:
        return flags

    rubric = _load_voice_rubric()

    # 1. Banned phrases (HARD) — union of hardcoded + rubric
    banned = set(HARD_BANNED_PHRASES)
    for p in rubric.get("banned_phrases", []):
        banned.add(p.lower())
    for phrase in banned:
        for ln in _find_all(text, phrase):
            flags.append(ComplianceFlag(
                rule="banned_phrase",
                severity="hard",
                message=f"Banned phrase: '{phrase}' (line {ln})",
                match=phrase, line=ln,
            ))

    # 2. Guarantee language (HARD)
    for phrase in GUARANTEE_TERMS:
        for ln in _find_all(text, phrase):
            flags.append(ComplianceFlag(
                rule="guaranteed_return",
                severity="hard",
                message=f"Implies guarantee: '{phrase}' — rephrase with 'based on current' or 'historically'",
                match=phrase, line=ln,
            ))

    # 3. Broker rule (HARD)
    if BROKER_RULE_BAD.search(text):
        flags.append(ComplianceFlag(
            rule="broker_rule",
            severity="hard",
            message="Taylor is a real estate AGENT, not a broker.",
        ))

    # 4. Audience-lane leaks (HARD, platform-specific)
    #    TikTok + Temple Insider newsletter = buyer/relocator lane — no investor terms.
    low = text.lower()
    lane_gated = ("tiktok", "newsletter_temple_insider")
    if platform and platform.lower() in lane_gated:
        for term in TIKTOK_INVESTOR_TERMS:
            if term in low:
                flags.append(ComplianceFlag(
                    rule="audience_lane_leak",
                    severity="hard",
                    message=f"{platform} is buyer/relocator lane — investor term found: '{term}'",
                    match=term,
                ))

    # 5. Steering language (SOFT)
    for pattern in STEERING_PATTERNS:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            flags.append(ComplianceFlag(
                rule="fair_housing_steering",
                severity="soft",
                message=f"Potential steering language: '{m.group(0)}' — rephrase with data, not demographic fit",
                match=m.group(0),
            ))

    # 6. School claims without disclaimer (SOFT)
    low = text.lower()
    school_hit = any(re.search(p, text, re.IGNORECASE) for p in SCHOOL_CLAIM_PATTERNS)
    if school_hit and not any(cue in low for cue in SCHOOL_DISCLAIMER_CUES):
        flags.append(ComplianceFlag(
            rule="school_claim_unverified",
            severity="soft",
            message="School quality claim without 'verify by address' disclaimer.",
        ))

    # 7. Tax rate mentioned without verify disclaimer (SOFT)
    if re.search(TAX_RATE_PATTERN, text, re.IGNORECASE) and not any(c in low for c in TAX_DISCLAIMER_CUES):
        flags.append(ComplianceFlag(
            rule="tax_claim_unverified",
            severity="soft",
            message="Tax rate mentioned without 'verify current rate' disclaimer.",
        ))

    # 8. Entity declaration missing (SOFT, only for public-facing long form)
    # Only flag on public-facing drafts with body >= 200 chars (not short captions/SMS)
    if public_facing and len(text) >= 200:
        if not any(p.lower() in low for p in ENTITY_REQUIRED_PHRASES):
            flags.append(ComplianceFlag(
                rule="entity_missing",
                severity="soft",
                message="No 'Taylor Dasch with EG Realty' declaration found. Include in first 3 sentences of scripts / first paragraph of blogs.",
            ))

    return flags


def check_draft(draft: Draft) -> list[ComplianceFlag]:
    # SMS/DM aren't public-facing; skip entity rule
    public = draft.platform not in ("sms", "email")
    return check_text(draft.body, platform=draft.platform, public_facing=public)


def has_hard_violation(flags: list[ComplianceFlag] | list[dict]) -> bool:
    for f in flags:
        sev = f.severity if hasattr(f, "severity") else f.get("severity")
        if sev == "hard":
            return True
    return False


def summarize(flags: list[ComplianceFlag] | list[dict]) -> str:
    if not flags:
        return "OK — 0 flags"
    hard = sum(1 for f in flags if (f.severity if hasattr(f, "severity") else f.get("severity")) == "hard")
    soft = sum(1 for f in flags if (f.severity if hasattr(f, "severity") else f.get("severity")) == "soft")
    return f"{hard} HARD, {soft} SOFT"
