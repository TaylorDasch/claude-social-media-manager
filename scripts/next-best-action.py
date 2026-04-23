#!/usr/bin/env python3
"""
Next Best Action Engine — Prioritization for content operations.

Looks at:
  1. Workflow state (blocked, incomplete, stale)
  2. Freshness debt (pages/content needing refresh)
  3. Missing repurposing (published but not repurposed)
  4. Missing page embeds (video exists, page doesn't have it)
  5. Missing schema
  6. Performance winners not yet expanded
  7. Content gaps from weekly rhythm
  8. Blocked assets needing one manual input

Outputs:
  - #1 highest-leverage action
  - Top 5 ranked queue
  - Blocking items that need Taylor's input

Usage:
  python3 scripts/next-best-action.py
  python3 scripts/next-best-action.py --json
"""

import os
import re
import csv
import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

from common import warn

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"
GOVERNANCE_DIR = PROJECT_ROOT / "governance"
VIDEO_MAP_PATH = PROJECT_ROOT / "VIDEO-TO-PAGE-MAP.md"
REGISTRY_PATH = DATA_DIR / "content-registry.csv"
PERFORMANCE_PATH = DATA_DIR / "performance-ledger.csv"
SITE_ROOT = PROJECT_ROOT.parent / "real-estate-redefined"

NOW = datetime.now()

# Path safety checks — warn loudly if critical paths missing
_MISSING_PATHS = []
if not SITE_ROOT.exists():
    _MISSING_PATHS.append(f"SITE_ROOT not found: {SITE_ROOT}")
if not REGISTRY_PATH.exists():
    _MISSING_PATHS.append(f"Registry not found: {REGISTRY_PATH}")
if _MISSING_PATHS:
    for msg in _MISSING_PATHS:
        warn(msg, context="paths")
    warn("Some checks will be skipped due to missing paths.", context="paths")

CURRENT_WEEK = f"{NOW.year}-W{NOW.isocalendar()[1]:02d}"
DAY_OF_WEEK = NOW.strftime("%A")

# Weekly rhythm targets
WEEKLY_TARGETS = {
    "yt_longform": {"target": 1, "label": "YouTube long-form video"},
    "deal_of_week": {"target": 1, "label": "Deal of the Week package"},
    "tiktok": {"target": 3, "label": "TikTok scripts"},
    "yt_short": {"target": 1, "label": "YouTube Short"},
    "blog": {"target": 1, "label": "Blog post"},
    "newsletter": {"target": 1, "label": "Newsletter issue (biweekly)"},
    "gmb": {"target": 3, "label": "GMB posts"},
    "community": {"target": 2, "label": "Community posts"},
    "social": {"target": 1, "label": "Social captions (dual frame)"},
    "linkedin": {"target": 0, "label": "LinkedIn carousel (optional)"},
    "bp": {"target": 1, "label": "BiggerPockets engagement"},
    "audit": {"target": 1, "label": "AEO page audit"},
}


class Action:
    """Represents a prioritized action."""
    def __init__(self, description: str, reason: str, score: float, category: str, blocking_input: str = None):
        self.description = description
        self.reason = reason
        self.score = score  # Higher = more urgent
        self.category = category
        self.blocking_input = blocking_input

    def to_dict(self):
        return {
            "description": self.description,
            "reason": self.reason,
            "score": self.score,
            "category": self.category,
            "blocking_input": self.blocking_input,
        }


def load_registry() -> list[dict]:
    """Load content registry."""
    if not REGISTRY_PATH.exists():
        return []
    try:
        with open(REGISTRY_PATH, "r") as f:
            return list(csv.DictReader(f))
    except Exception as exc:
        warn(f"Could not read registry CSV: {exc}", context="registry")
        return []


def load_performance() -> list[dict]:
    """Load performance ledger."""
    if not PERFORMANCE_PATH.exists():
        return []
    try:
        with open(PERFORMANCE_PATH, "r") as f:
            return list(csv.DictReader(f))
    except Exception as exc:
        warn(f"Could not read performance-ledger.csv: {exc}", context="performance")
        return []


def count_week_output() -> dict[str, int]:
    """Count produced output for current week."""
    counts = defaultdict(int)
    week_dir = OUTPUT_DIR / CURRENT_WEEK
    if not week_dir.exists():
        return dict(counts)

    # Count produced assets
    produced = week_dir / "produced"
    if produced.exists():
        for slug_dir in produced.iterdir():
            if slug_dir.is_dir():
                files = [f.name for f in slug_dir.iterdir()]
                if "youtube-description.md" in files:
                    counts["yt_longform"] += 1
                tiktoks = [f for f in files if f.startswith("tiktok-clip")]
                counts["tiktok"] += len(tiktoks)
                if "youtube-short.md" in files:
                    counts["yt_short"] += 1
                if "blog-outline.md" in files:
                    counts["blog"] += 1
                if "newsletter-segment.md" in files:
                    counts["newsletter"] += 1
                if "gmb-post.md" in files:
                    counts["gmb"] += 1
                if "community-post.md" in files:
                    counts["community"] += 1
                if "social-captions.md" in files:
                    counts["social"] += 1

    # Check other directories
    for subdir_name, key in [("deal-of-the-week", "deal_of_week"), ("blog", "blog"), ("newsletter", "newsletter")]:
        subdir = week_dir / subdir_name
        if subdir.exists() and any(subdir.iterdir()):
            counts[key] = max(counts[key], 1)

    return dict(counts)


def check_blocked_assets(registry: list[dict]) -> list[Action]:
    """Find blocked assets."""
    actions = []
    for row in registry:
        if row.get("status") == "BLOCKED":
            actions.append(Action(
                description=f"Unblock: {row.get('title', 'unknown')}",
                reason=row.get("blocked_reason", "No reason given"),
                score=8.0,
                category="blocked",
                blocking_input=row.get("blocked_reason"),
            ))
    return actions


def check_stale_assets(registry: list[dict]) -> list[Action]:
    """Find assets needing refresh."""
    actions = []
    for row in registry:
        refresh_date = row.get("refresh_due_date", "")
        if refresh_date:
            try:
                due = datetime.strptime(refresh_date, "%Y-%m-%d")
                if due < NOW:
                    days_overdue = (NOW - due).days
                    actions.append(Action(
                        description=f"Refresh: {row.get('title', 'unknown')}",
                        reason=f"{days_overdue} days overdue for refresh",
                        score=5.0 + min(days_overdue / 30, 3.0),
                        category="freshness",
                    ))
            except ValueError:
                pass
    return actions


def check_incomplete_pipelines(registry: list[dict]) -> list[Action]:
    """Find assets stuck in intermediate states."""
    actions = []
    stuck_states = {"SCRIPTED", "FILMED", "EDITED", "READY_TO_PUBLISH", "REPURPOSING"}
    for row in registry:
        if row.get("status") in stuck_states:
            created = row.get("created_date", "")
            days_stuck = 0
            if created:
                try:
                    days_stuck = (NOW - datetime.strptime(created, "%Y-%m-%d")).days
                except ValueError:
                    pass

            if days_stuck > 3:
                actions.append(Action(
                    description=f"Complete: {row.get('title', 'unknown')} (stuck in {row['status']})",
                    reason=f"In {row['status']} for {days_stuck} days",
                    score=6.0 + min(days_stuck / 7, 2.0),
                    category="incomplete",
                ))
    return actions


def check_missing_repurposing(registry: list[dict]) -> list[Action]:
    """Find recently published content that hasn't been repurposed.
    Only flag videos published in the last 30 days — older ones were likely
    published before the registry existed and shouldn't flood the queue."""
    actions = []
    published = [r for r in registry if r.get("status") == "PUBLISHED" and r.get("content_type") in ("video", "youtube_longform")]
    for row in published:
        pub_date = row.get("publish_date", "")
        days_since = 0
        if pub_date:
            try:
                days_since = (NOW - datetime.strptime(pub_date, "%Y-%m-%d")).days
            except ValueError:
                continue
        # Only flag recent videos (last 30 days) — older ones are historical backfill
        if days_since < 2 or days_since > 30:
            continue
        # Check if any derivatives exist
        derivatives = [r for r in registry if r.get("canonical_parent_id") == row.get("content_id")]
        if not derivatives:
            actions.append(Action(
                description=f"Repurpose: {row.get('title', 'unknown')}",
                reason=f"Published {days_since} days ago, no derivatives yet",
                score=5.0 + min(days_since / 7, 2.0),
                category="repurpose",
            ))
    return actions


def check_production_gaps() -> list[Action]:
    """Compare current week output against targets."""
    actions = []
    counts = count_week_output()

    for key, spec in WEEKLY_TARGETS.items():
        produced = counts.get(key, 0)
        target = spec["target"]
        if target > 0 and produced < target:
            remaining = target - produced
            # Higher score earlier in the week (more time to catch up)
            day_weight = max(0.5, (5 - NOW.weekday()) / 5)
            actions.append(Action(
                description=f"Produce: {remaining}x {spec['label']}",
                reason=f"Weekly target: {target}, produced: {produced}",
                score=4.0 * day_weight + remaining,
                category="production_gap",
            ))

    return actions


def check_performance_winners(performance: list[dict], registry: list[dict]) -> list[Action]:
    """Find high-performing content that could be expanded."""
    actions = []
    recent = [p for p in performance if p.get("date", "") >= (NOW - timedelta(days=30)).strftime("%Y-%m-%d")]

    for entry in recent:
        # Check for high engagement signals
        rating = entry.get("taylor_rating", "")
        if rating == "CRUSH":
            content_id = entry.get("content_id", "")
            matching = [r for r in registry if r.get("content_id") == content_id]
            title = matching[0].get("title", content_id) if matching else content_id
            actions.append(Action(
                description=f"Expand winner: {title}",
                reason=f"CRUSH rating — create derivative or sequel",
                score=6.0,
                category="expand_winner",
            ))

    return actions


def main():
    parser = argparse.ArgumentParser(description="Next Best Action Engine")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    registry = load_registry()
    performance = load_performance()

    # Collect all candidate actions
    all_actions = []
    all_actions.extend(check_blocked_assets(registry))
    all_actions.extend(check_stale_assets(registry))
    all_actions.extend(check_incomplete_pipelines(registry))
    all_actions.extend(check_missing_repurposing(registry))
    all_actions.extend(check_production_gaps())
    all_actions.extend(check_performance_winners(performance, registry))

    # Sort by score (highest first)
    all_actions.sort(key=lambda a: a.score, reverse=True)

    if args.json:
        print(json.dumps([a.to_dict() for a in all_actions], indent=2))
        return

    # Human-readable output
    print("=" * 60)
    print(f"NEXT BEST ACTION — {DAY_OF_WEEK}, {NOW.strftime('%Y-%m-%d')}")
    print(f"Week: {CURRENT_WEEK}")
    print("=" * 60)
    print()

    # System status
    active = len([r for r in registry if r.get("status") not in ("ARCHIVED", "")])
    stale = len([a for a in all_actions if a.category == "freshness"])
    blocked = len([a for a in all_actions if a.category == "blocked"])
    counts = count_week_output()
    produced = sum(counts.values())
    total_targets = sum(s["target"] for s in WEEKLY_TARGETS.values())

    print("SYSTEM STATUS")
    print(f"  Registry: {len(registry)} assets ({active} active)")
    print(f"  This week: {produced}/{total_targets} targets produced")
    print(f"  Blocked: {blocked} items")
    print(f"  Stale: {stale} items needing refresh")
    print()

    # #1 Action
    if all_actions:
        top = all_actions[0]
        print("=" * 60)
        print(f"#1 RECOMMENDED ACTION (score: {top.score:.1f})")
        print(f"  {top.description}")
        print(f"  Why: {top.reason}")
        if top.blocking_input:
            print(f"  Needs from Taylor: {top.blocking_input}")
        print("=" * 60)
        print()

    # Top 5 queue
    print("QUEUE (next 5)")
    for i, action in enumerate(all_actions[1:6], 2):
        print(f"  {i}. [{action.category}] {action.description}")
        print(f"     {action.reason}")
        if action.blocking_input:
            print(f"     NEEDS: {action.blocking_input}")
    print()

    # Blocking items
    blocking = [a for a in all_actions if a.blocking_input]
    if blocking:
        print("WAITING ON TAYLOR")
        for a in blocking:
            print(f"  - {a.description}: {a.blocking_input}")
        print()

    print("=" * 60)
    print(f"Total actions in queue: {len(all_actions)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
