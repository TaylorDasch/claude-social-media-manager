#!/usr/bin/env python3
"""Pattern Miner — extract winning patterns from performance-ledger.csv.

Reads:
  - data/performance-ledger.csv (CRUSH/SOLID/MEH/MISS ratings)
  - data/content-registry.csv (metadata: pillar, persona, platform, etc.)
  - governance/scoring-rules.json (thresholds + group_by config)

Writes:
  - data/winning-patterns.json (proven + thin patterns with lift metrics)

Consumed by /content-calendar (future: weight next week 60% proven, 30% new,
10% experiment — see calendar_weights in scoring-rules.json).

Usage:
  python3 scripts/pattern-miner.py
  python3 scripts/pattern-miner.py --dry-run   # Print JSON to stdout; don't write

Rollback:
  git checkout -- data/winning-patterns.json
  # or delete: rm data/winning-patterns.json
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from common import (
    DATA_DIR,
    GOVERNANCE_DIR,
    PERFORMANCE_LEDGER_PATH,
    info,
    load_registry,
    load_json_safe,
    warn,
)

SCORING_RULES_PATH = GOVERNANCE_DIR / "scoring-rules.json"
WINNING_PATTERNS_PATH = DATA_DIR / "winning-patterns.json"

NOW = datetime.now(timezone.utc)


def load_ledger() -> list[dict]:
    """Load performance-ledger.csv as list of dicts."""
    if not PERFORMANCE_LEDGER_PATH.exists():
        warn(f"Performance ledger not found at {PERFORMANCE_LEDGER_PATH}",
             context="ledger")
        return []
    try:
        with PERFORMANCE_LEDGER_PATH.open("r", encoding="utf-8") as fh:
            return list(csv.DictReader(fh))
    except Exception as exc:
        warn(f"Could not read ledger: {exc}", context="ledger")
        return []


def day_of_week(date_str: str) -> str:
    """Return 'Monday', 'Tuesday', etc. from YYYY-MM-DD. Empty on fail."""
    if not date_str:
        return ""
    try:
        return datetime.strptime(date_str[:10], "%Y-%m-%d").strftime("%A")
    except ValueError:
        return ""


def enrich_ledger_with_registry(
    ledger: list[dict], registry: list[dict]
) -> list[dict]:
    """Attach registry metadata (pillar, persona, publish_date, etc.) to each
    ledger row by content_id. Returns list of enriched dicts."""
    reg_by_id = {row.get("content_id", ""): row for row in registry if row.get("content_id")}
    enriched = []
    missing = 0
    for row in ledger:
        cid = row.get("content_id", "")
        reg = reg_by_id.get(cid, {})
        if cid and not reg:
            missing += 1
        enriched.append({
            **row,
            "pillar": reg.get("pillar", ""),
            "persona": reg.get("persona", ""),
            "content_type": reg.get("content_type", ""),
            "cta_keyword": reg.get("cta_keyword", ""),
            "lead_magnet": reg.get("lead_magnet", ""),
            "publish_date": reg.get("publish_date", ""),
            "day_of_week": day_of_week(reg.get("publish_date", "")),
            "title": reg.get("title", ""),
            "slug": reg.get("slug", ""),
        })
    if missing:
        warn(f"{missing} ledger row(s) reference content_ids not in registry",
             context="pattern-miner")
    return enriched


def compute_lift(rows: list[dict], rules: dict) -> float:
    """Compute avg view-lift for a cluster vs platform baseline.

    Only works for YouTube rows where impressions column is numeric.
    Returns 0.0 if no usable data.
    """
    numeric = []
    for row in rows:
        try:
            v = float(row.get("impressions", "") or 0)
            if v > 0:
                numeric.append(v)
        except (ValueError, TypeError):
            continue
    if not numeric:
        return 0.0
    avg = sum(numeric) / len(numeric)
    # Platform-specific baseline lookup
    platform = rows[0].get("platform", "")
    yt_rules = rules.get("platforms", {}).get("youtube", {})
    baseline = yt_rules.get("channel_avg_views_living_in_temple", 2000)
    if platform == "youtube" and baseline > 0:
        return round(avg / baseline, 2)
    return 0.0


def group_key(row: dict, dimensions: list[str]) -> tuple:
    """Build a hashable key for the group_by dimensions."""
    return tuple(row.get(dim, "") for dim in dimensions)


def mine_patterns(
    enriched: list[dict], rules: dict
) -> tuple[list[dict], list[dict]]:
    """Return (proven_patterns, thin_patterns).

    Proven = CRUSH count >= min_sample_size.
    Thin = CRUSH count 1..(min_sample_size-1).
    """
    miner_cfg = rules.get("pattern_miner", {})
    dimensions = miner_cfg.get("group_by", [])
    min_sample = rules.get("min_sample_size", 3)
    min_lift = miner_cfg.get("min_lift", 1.5)

    crush_rows = [
        r for r in enriched
        if (r.get("taylor_rating") or "").upper() == "CRUSH"
    ]
    if not crush_rows:
        return [], []

    groups: dict[tuple, list[dict]] = defaultdict(list)
    for row in crush_rows:
        key = group_key(row, dimensions)
        groups[key].append(row)

    proven: list[dict] = []
    thin: list[dict] = []
    for key, rows in groups.items():
        pattern = {
            "dimensions": dict(zip(dimensions, key)),
            "sample_size": len(rows),
            "avg_lift": compute_lift(rows, rules),
            "sample_content_ids": [r.get("content_id", "") for r in rows],
            "sample_titles": [r.get("title", "")[:80] for r in rows if r.get("title")],
        }
        if len(rows) >= min_sample and pattern["avg_lift"] >= min_lift:
            proven.append(pattern)
        else:
            thin.append(pattern)

    # Sort proven by lift desc, thin by sample_size desc
    proven.sort(key=lambda p: (-p["avg_lift"], -p["sample_size"]))
    thin.sort(key=lambda p: -p["sample_size"])
    return proven, thin


def summarize_directional(enriched: list[dict]) -> dict:
    """For thin data, surface directional breakdowns that aren't full patterns."""
    crush = [r for r in enriched if (r.get("taylor_rating") or "").upper() == "CRUSH"]
    solid = [r for r in enriched if (r.get("taylor_rating") or "").upper() == "SOLID"]

    def counter_by(rows: list[dict], key: str) -> dict:
        c = Counter(r.get(key, "") or "(blank)" for r in rows)
        return dict(c.most_common(10))

    return {
        "crush_by_pillar": counter_by(crush, "pillar"),
        "crush_by_persona": counter_by(crush, "persona"),
        "crush_by_platform": counter_by(crush, "platform"),
        "solid_by_pillar": counter_by(solid, "pillar"),
        "total_crush": len(crush),
        "total_solid": len(solid),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print JSON to stdout; don't write winning-patterns.json"
    )
    args = parser.parse_args()

    info("Pattern Miner — mining winning patterns from performance-ledger")
    info("-" * 60)

    rules = load_json_safe(SCORING_RULES_PATH, default={})
    if not rules:
        warn("scoring-rules.json empty or missing; aborting",
             context="pattern-miner")
        return 1

    ledger = load_ledger()
    registry = load_registry()
    if not ledger:
        warn("Ledger empty; nothing to mine", context="pattern-miner")
        return 1

    enriched = enrich_ledger_with_registry(ledger, registry)
    proven, thin = mine_patterns(enriched, rules)
    directional = summarize_directional(enriched)
    min_sample = rules.get("min_sample_size", 3)

    output = {
        "generated_at": NOW.isoformat(),
        "min_sample_size": min_sample,
        "total_ledger_rows": len(ledger),
        "total_crush_rows": directional["total_crush"],
        "total_solid_rows": directional["total_solid"],
        "proven_patterns": proven,
        "thin_patterns": thin,
        "directional_summary": directional,
        "_note": (
            f"Proven = CRUSH count >= {min_sample} AND avg_lift >= "
            f"{rules.get('pattern_miner', {}).get('min_lift', 1.5)}. "
            "Thin patterns are single CRUSH instances — informational. "
            "Re-run weekly as weekly-pull.py builds CRUSH history."
        ),
    }

    info(f"Total ledger rows: {len(ledger)}")
    info(f"CRUSH rows: {directional['total_crush']}")
    info(f"SOLID rows: {directional['total_solid']}")
    info(f"Proven patterns (>= {min_sample} CRUSH): {len(proven)}")
    info(f"Thin patterns (< {min_sample} CRUSH): {len(thin)}")
    if proven:
        info("\nTop proven patterns:")
        for p in proven[:5]:
            info(f"  [{p['avg_lift']}x lift, {p['sample_size']} sample] "
                 f"{p['dimensions']}")
    elif thin:
        info("\nThin patterns (not yet proven):")
        for p in thin[:5]:
            info(f"  [{p['sample_size']} sample] {p['dimensions']}")

    if args.dry_run:
        info("\n--- DRY RUN — would write to " + str(WINNING_PATTERNS_PATH) + " ---")
        print(json.dumps(output, indent=2))
        return 0

    with WINNING_PATTERNS_PATH.open("w", encoding="utf-8") as fh:
        json.dump(output, fh, indent=2)
    info(f"\n✓ Wrote {WINNING_PATTERNS_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
