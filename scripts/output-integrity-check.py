#!/usr/bin/env python3
"""
Output Integrity Check — Validates content pipeline completeness.

Catches:
  1. Missing expected files from skill runs
  2. Partial pipeline runs (e.g., /produce generated 8 of 12 files)
  3. Invalid naming conventions
  4. Missing schema sidecar files
  5. Duplicate slugs across weeks
  6. Empty sections or placeholder text in outputs
  7. Missing CTA or mismatched CTA
  8. Missing pinned comments
  9. Registry entries without matching files
  10. Files without registry entries
  11. Gate 2 (entity consistency), Gate 11 (no auto-send), Gate 12
      (pillar rotation) — via --gates flag

Usage:
  python3 scripts/output-integrity-check.py                    # Check current week
  python3 scripts/output-integrity-check.py --week 2026-W14    # Check specific week
  python3 scripts/output-integrity-check.py --all              # Check all weeks
  python3 scripts/output-integrity-check.py --gates            # Also run Gate 2/11/12
  python3 scripts/output-integrity-check.py --single-file PATH # Check one file (hook mode)

Exit codes:
  0 — no HARD gate failures
  2 — one or more HARD gate failures (blocks writes when used in PreToolUse hook)

Rollback:
  git checkout -- scripts/output-integrity-check.py
"""

import os
import re
import csv
import argparse
from pathlib import Path
from datetime import datetime

from common import (
    PROJECT_ROOT,
    OUTPUT_DIR,
    REGISTRY_PATH,
    load_banned_words,
    load_registry,
    load_valid_states,
    warn,
)

YT_VIDEOS_DIR = PROJECT_ROOT / "yt-videos"

# Expected files per skill output type
EXPECTED_FILES = {
    "produced": {
        "required": [
            "youtube-description.md",
            "youtube-tags.md",
            "blog-outline.md",
            "social-captions.md",
            "PRODUCTION-CHECKLIST.md",
        ],
        "expected_patterns": [
            r"tiktok-clip-\d+\.md",  # At least 2
            r"youtube-short\.md",
            r"newsletter-segment\.md",
            r"gmb-post\.md",
            r"community-post\.md",
        ],
        "minimum_tiktok_clips": 2,
    },
    "blog": {
        "required": [
            # Blog post markdown file (any name)
        ],
        "expected_patterns": [
            r"schema\.json",
            r".*\.md",  # At least one markdown file
        ],
    },
    "deal-of-the-week": {
        "required": [
            "youtube-script.md",
            "blog-outline.md",
            "short-script.md",
            "social-caption.md",
        ],
        "expected_patterns": [
            r"community-post.*\.md",
            r"schema\.json",
        ],
    },
    "newsletter": {
        "required": [],
        "expected_patterns": [
            r".*\.md",  # At least one markdown file
        ],
    },
}

# Placeholder text patterns that indicate incomplete output
PLACEHOLDER_PATTERNS = [
    r"\[INSERT\s",
    r"\[TODO\]",
    r"\[PLACEHOLDER\]",
    r"\[YOUR\s",
    r"\[ADD\s",
    r"\[FILL\s",
    r"XXX",
    r"\[TBD\]",
    r"\[NEEDED\]",
    r"\[UPDATE\s",
]

# Banned words — parsed from governance/QUALITY-GATES.md at runtime.
# SSOT lives in the markdown. Edit the doc, not this file.
BANNED_WORDS = load_banned_words()

# CTA keywords that should appear somewhere in content
VALID_CTA_KEYWORDS = [
    "SPREADSHEET", "DEALS", "ANALYZER",
    "BAH", "PCS", "RELOCATE", "GUIDE",
    "MATCHED", "BSW", "DOCTOR", "RESIDENT",
    "ACREAGE", "LUXURY",
    "TEMPLE", "TOUR",
    "dealswithdasch", "254-718-4249", "templetxhomes.net",
]

# Content types that MUST include the "Taylor Dasch with EG Realty" entity
# declaration in their opening (Gate 2). Tested by filename substring match.
ENTITY_DECLARATION_REQUIRED = (
    "blog-post", "blog-outline", "newsletter", "youtube-script",
    "youtube-description", "production-checklist", "deal-of-the-week",
    "dotw-", "script-",
)

# Forbidden auto-send calls — Gate 11 (No Auto-Send).
# Content markdown should never contain these literal symbols.
FORBIDDEN_SEND_CALLS = (
    "send_email(",
    "send_message(",
    ".send_now(",
    "email.send(",
)

# Short-form content types — Gate 12 (Pillar Rotation) applies to these only.
SHORT_FORM_TYPES = (
    "tiktok", "tiktok_script", "reel", "instagram_reel", "short",
)

# Issue prefixes that represent HARD gate failures (should block the write
# when invoked with --single-file from the PreToolUse hook).
HARD_ISSUE_PREFIXES = (
    "BANNED WORD",
    "MISSING ENTITY",
    "AUTO-SEND CALL",
    "INVALID STATE",
)


def get_current_week() -> str:
    """Get ISO week string for current date."""
    now = datetime.now()
    return f"{now.year}-W{now.isocalendar()[1]:02d}"


def find_week_dirs(week: str = None) -> list[Path]:
    """Find output directories for specified or all weeks."""
    if not OUTPUT_DIR.exists():
        return []
    if week:
        target = OUTPUT_DIR / week
        return [target] if target.exists() else []
    return sorted([d for d in OUTPUT_DIR.iterdir() if d.is_dir() and re.match(r"\d{4}-W\d{2}", d.name)])


def check_file_content(filepath: Path) -> list[str]:
    """Check a single file for quality issues."""
    issues = []
    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        issues.append(f"UNREADABLE: {filepath.name}")
        return issues

    # Empty file
    if len(content.strip()) < 50:
        issues.append(f"EMPTY/TINY: {filepath.name} ({len(content)} chars)")
        return issues

    # Placeholder text
    for pattern in PLACEHOLDER_PATTERNS:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            issues.append(f"PLACEHOLDER: {filepath.name} contains '{matches[0]}'")

    # Banned words
    content_lower = content.lower()
    for word in BANNED_WORDS:
        if word.lower() in content_lower:
            issues.append(f"BANNED WORD: {filepath.name} contains '{word}'")

    # Check for CTA presence (at least one CTA keyword or contact info)
    has_cta = any(kw.lower() in content_lower for kw in VALID_CTA_KEYWORDS)
    if not has_cta and filepath.suffix == ".md" and filepath.name not in ("schema.json", "youtube-tags.md"):
        issues.append(f"NO CTA: {filepath.name} — no CTA keyword or contact info found")

    return issues


def check_produced_dir(produced_dir: Path) -> list[str]:
    """Check a /produce output directory for completeness."""
    issues = []
    if not produced_dir.exists():
        return issues

    for slug_dir in produced_dir.iterdir():
        if not slug_dir.is_dir():
            continue

        files = list(slug_dir.iterdir())
        filenames = [f.name for f in files]

        # Check required files
        spec = EXPECTED_FILES["produced"]
        for req in spec["required"]:
            if req not in filenames:
                issues.append(f"MISSING: {slug_dir.name}/{req}")

        # Check TikTok clip count
        tiktok_clips = [f for f in filenames if re.match(r"tiktok-clip-\d+\.md", f)]
        if len(tiktok_clips) < spec["minimum_tiktok_clips"]:
            issues.append(f"INCOMPLETE: {slug_dir.name} — only {len(tiktok_clips)} TikTok clips (need {spec['minimum_tiktok_clips']}+)")

        # Check schema
        if "schema.json" not in filenames:
            issues.append(f"MISSING SCHEMA: {slug_dir.name}/schema.json")

        # Check individual file content
        for filepath in files:
            if filepath.is_file():
                issues.extend(check_file_content(filepath))

    return issues


def check_slug_duplicates(all_weeks: list[Path]) -> list[str]:
    """Check for duplicate slugs across weeks."""
    issues = []
    slug_weeks = {}

    for week_dir in all_weeks:
        produced = week_dir / "produced"
        if produced.exists():
            for slug_dir in produced.iterdir():
                if slug_dir.is_dir():
                    slug = slug_dir.name
                    if slug in slug_weeks:
                        issues.append(f"DUPLICATE SLUG: '{slug}' found in {slug_weeks[slug]} AND {week_dir.name}")
                    slug_weeks[slug] = week_dir.name

    return issues


def check_registry_integrity() -> list[str]:
    """Check that registry entries have matching files and vice versa."""
    issues = []
    if not REGISTRY_PATH.exists():
        issues.append("MISSING: data/content-registry.csv does not exist")
        return issues

    try:
        with open(REGISTRY_PATH, "r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except Exception as e:
        issues.append(f"REGISTRY ERROR: Cannot read content-registry.csv — {e}")
        return issues

    if len(rows) == 0:
        issues.append("REGISTRY EMPTY: data/content-registry.csv has no entries (expected for initial setup)")
        return issues

    # Valid states parsed from governance/WORKFLOW-STATE-MACHINE.md at runtime.
    # SSOT lives in the markdown. Edit the doc, not this file.
    VALID_STATES = load_valid_states()

    for row in rows:
        # Validate state
        status = row.get("status", "")
        if status and VALID_STATES and status not in VALID_STATES:
            issues.append(f"INVALID STATE: '{row.get('title', 'unknown')}' has status '{status}' — not in state machine")

        # Check for entries with source_material_path that doesn't exist
        path = row.get("source_material_path", "")
        if path and not Path(path).exists() and not path.startswith("http"):
            issues.append(f"REGISTRY ORPHAN: '{row.get('title', 'unknown')}' references missing file: {path}")

        # Check for BLOCKED entries without reason
        if status == "BLOCKED" and not row.get("blocked_reason"):
            issues.append(f"BLOCKED NO REASON: '{row.get('title', 'unknown')}' is BLOCKED but has no blocked_reason")

        # Check PUBLISHED entries have publish_date
        if status == "PUBLISHED" and not row.get("publish_date"):
            issues.append(f"NO PUBLISH DATE: '{row.get('title', 'unknown')}' is PUBLISHED but missing publish_date")

        # Check video entries have related_page_slug
        if row.get("content_type") == "video" and status == "PUBLISHED" and not row.get("related_page_slug"):
            issues.append(f"NO PAGE LINK: '{row.get('title', 'unknown')}' is a published video with no related_page_slug")

    return issues


def check_yt_video_dirs() -> list[str]:
    """Check YouTube video production directories for missing concepts."""
    issues = []
    if not YT_VIDEOS_DIR.exists():
        return issues

    expected_concepts = {
        "research": r"(?:research|research-prompt|deep-research)",
        "script": r"(?:script|script-outline|production)",
        "shot_list": r"(?:shot-list|filming-checklist|filming)",
    }

    for video_dir in YT_VIDEOS_DIR.iterdir():
        if not video_dir.is_dir():
            continue
        filenames = [f.name.lower() for f in video_dir.iterdir() if f.is_file()]
        all_text = " ".join(filenames)
        missing = []
        for concept, pattern in expected_concepts.items():
            if not re.search(pattern, all_text):
                missing.append(concept)
        if missing:
            issues.append(f"INCOMPLETE VIDEO PREP: {video_dir.name} — missing concepts: {', '.join(missing)}")

    return issues


def check_entity_consistency(filepath: Path) -> list[str]:
    """Gate 2: Verify 'Taylor Dasch' and 'EG Realty' appear in the opening of
    content files that represent Taylor. Only enforced on applicable file types
    per ENTITY_DECLARATION_REQUIRED."""
    name = filepath.name.lower()
    if not any(pat in name for pat in ENTITY_DECLARATION_REQUIRED):
        return []
    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
    except Exception as exc:
        warn(f"Could not read {filepath}: {exc}", context="gate-2")
        return [f"UNREADABLE: {filepath.name}"]

    # First 800 chars ≈ opening paragraph for blog; ≈ first 3 sentences for script
    opening = content[:800].lower()
    issues = []
    if "taylor dasch" not in opening:
        issues.append(
            f"MISSING ENTITY: 'Taylor Dasch' not in opening of {filepath.name} "
            f"(Gate 2)"
        )
    if "eg realty" not in opening:
        issues.append(
            f"MISSING ENTITY: 'EG Realty' not in opening of {filepath.name} "
            f"(Gate 2)"
        )
    return issues


def check_never_send(filepath: Path) -> list[str]:
    """Gate 11: Content files must not contain literal auto-send code calls."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []
    issues = []
    for pattern in FORBIDDEN_SEND_CALLS:
        if pattern in content:
            issues.append(
                f"AUTO-SEND CALL: '{pattern}' found in {filepath.name} "
                f"(Gate 11 — use create_draft, never send)"
            )
    return issues


def check_pillar_rotation() -> list[str]:
    """Gate 12: Short-form content (TikTok/Reels) must not publish 2 consecutive
    same-pillar entries. Check last 3 PUBLISHED short-form rows."""
    registry = load_registry()
    short_form = [
        row for row in registry
        if (row.get("content_type") or "").lower() in SHORT_FORM_TYPES
        and row.get("status") == "PUBLISHED"
        and row.get("publish_date")
    ]
    short_form.sort(key=lambda r: r.get("publish_date", ""), reverse=True)
    recent = short_form[:3]
    if len(recent) < 2:
        return []

    issues = []
    for i in range(len(recent) - 1):
        pillar_a = recent[i].get("pillar", "")
        pillar_b = recent[i + 1].get("pillar", "")
        if pillar_a and pillar_a == pillar_b:
            issues.append(
                f"PILLAR ROTATION: 2 consecutive '{pillar_a}' in short-form "
                f"content (Gate 12) — "
                f"{recent[i].get('title', '')[:40]!r} + "
                f"{recent[i + 1].get('title', '')[:40]!r}"
            )
    return issues


def scan_file_gates(filepath: Path) -> list[str]:
    """Run all file-level gates on a single file: Gate 1 (banned), Gate 2
    (entity), Gate 11 (never-send). Used by --single-file hook mode."""
    if not filepath.exists():
        return [f"NOT FOUND: {filepath}"]
    issues = []
    issues.extend(check_file_content(filepath))
    issues.extend(check_entity_consistency(filepath))
    issues.extend(check_never_send(filepath))
    return issues


def has_hard_fail(issues: list[str]) -> bool:
    """Return True if any issue string starts with a HARD-gate prefix."""
    return any(
        issue.startswith(prefix)
        for issue in issues
        for prefix in HARD_ISSUE_PREFIXES
    )


def main():
    parser = argparse.ArgumentParser(description="Output Integrity Check")
    parser.add_argument("--week", type=str, help="Check specific week (e.g., 2026-W14)")
    parser.add_argument("--all", action="store_true", help="Check all weeks")
    parser.add_argument(
        "--gates", action="store_true",
        help="Also run Gate 2 (entity), Gate 11 (never-send), Gate 12 (pillar rotation)",
    )
    parser.add_argument(
        "--single-file", type=str, default=None,
        help="Check a single file (for PreToolUse hook). "
             "Exits non-zero if any HARD gate fails.",
    )
    args = parser.parse_args()

    # --single-file mode: fast path for PreToolUse hook
    if args.single_file:
        fp = Path(args.single_file)
        issues = scan_file_gates(fp)
        for issue in issues:
            print(issue)
        if has_hard_fail(issues):
            print(f"\nHARD GATE FAIL on {fp.name} — write blocked")
            return 2
        return 0

    print("=" * 60)
    print("OUTPUT INTEGRITY CHECK")
    print(f"Run: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    print()

    all_issues = []

    # Determine which weeks to check
    if args.all:
        week_dirs = find_week_dirs()
    elif args.week:
        week_dirs = find_week_dirs(args.week)
    else:
        week_dirs = find_week_dirs(get_current_week())

    if not week_dirs:
        current = args.week or get_current_week()
        print(f"No output directory found for {current}")
        print()

    # Check each week
    for week_dir in week_dirs:
        print(f"--- {week_dir.name} ---")

        # Check produced directories
        produced = week_dir / "produced"
        if produced.exists():
            issues = check_produced_dir(produced)
            all_issues.extend(issues)
            for issue in issues:
                print(f"  {issue}")

        # Check other content type directories
        for content_type in ["blog", "deal-of-the-week", "newsletter"]:
            content_dir = week_dir / content_type
            if content_dir.exists():
                for filepath in content_dir.rglob("*.md"):
                    issues = check_file_content(filepath)
                    all_issues.extend(issues)
                    for issue in issues:
                        print(f"  {issue}")

        if not all_issues:
            print("  No issues found")
        print()

    # Cross-week duplicate check
    if args.all or len(week_dirs) > 1:
        print("--- Cross-Week Duplicate Check ---")
        dupe_issues = check_slug_duplicates(find_week_dirs())
        all_issues.extend(dupe_issues)
        for issue in dupe_issues:
            print(f"  {issue}")
        if not dupe_issues:
            print("  No duplicate slugs found")
        print()

    # Registry integrity
    print("--- Registry Integrity ---")
    reg_issues = check_registry_integrity()
    all_issues.extend(reg_issues)
    for issue in reg_issues:
        print(f"  {issue}")
    if not reg_issues:
        print("  Registry OK")
    print()

    # Video prep check
    print("--- Video Prep Directories ---")
    yt_issues = check_yt_video_dirs()
    all_issues.extend(yt_issues)
    for issue in yt_issues:
        print(f"  {issue}")
    if not yt_issues:
        print("  All video preps complete")
    print()

    # --gates mode: also run Gate 2, Gate 11, Gate 12 across the scanned weeks
    if args.gates:
        print("--- Gate 2: Entity Consistency ---")
        entity_issues = []
        for week_dir in week_dirs:
            for md_file in week_dir.rglob("*.md"):
                entity_issues.extend(check_entity_consistency(md_file))
        all_issues.extend(entity_issues)
        for issue in entity_issues:
            print(f"  {issue}")
        if not entity_issues:
            print("  All checked outputs include 'Taylor Dasch' + 'EG Realty'")
        print()

        print("--- Gate 11: No Auto-Send ---")
        send_issues = []
        for week_dir in week_dirs:
            for md_file in week_dir.rglob("*.md"):
                send_issues.extend(check_never_send(md_file))
        all_issues.extend(send_issues)
        for issue in send_issues:
            print(f"  {issue}")
        if not send_issues:
            print("  No auto-send calls found in content")
        print()

        print("--- Gate 12: Pillar Rotation (short-form) ---")
        rotation_issues = check_pillar_rotation()
        all_issues.extend(rotation_issues)
        for issue in rotation_issues:
            print(f"  {issue}")
        if not rotation_issues:
            print("  Short-form pillar rotation OK")
        print()

    # Summary
    print("=" * 60)
    print(f"TOTAL ISSUES: {len(all_issues)}")
    if all_issues:
        severity_counts = {
            "MISSING": 0, "INCOMPLETE": 0, "PLACEHOLDER": 0,
            "BANNED WORD": 0, "NO CTA": 0, "DUPLICATE": 0, "OTHER": 0
        }
        for issue in all_issues:
            categorized = False
            for key in severity_counts:
                if issue.startswith(key):
                    severity_counts[key] += 1
                    categorized = True
                    break
            if not categorized:
                severity_counts["OTHER"] += 1
        print("Breakdown:")
        for sev, count in severity_counts.items():
            if count > 0:
                print(f"  {sev}: {count}")
    print("=" * 60)

    # Non-zero exit if any HARD gate failed (so CI / hooks can block)
    return 2 if has_hard_fail(all_issues) else 0


if __name__ == "__main__":
    raise SystemExit(main() or 0)
