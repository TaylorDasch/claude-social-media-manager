#!/usr/bin/env python3
"""Generate a local command-center snapshot for the 3x social OS.

The script is intentionally read-only unless --out is provided. It pulls from
the local content registry, weekly output folders, governance state machine,
and market-monitor CSV freshness so the social plan starts from evidence.

Usage:
  python3 scripts/social-os-snapshot.py
  python3 scripts/social-os-snapshot.py --json
  python3 scripts/social-os-snapshot.py --out projects/real-estate-social-os-3x/snapshots/latest.md
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

from common import OUTPUT_DIR, PROJECT_ROOT, load_registry, load_valid_states

HOME = PROJECT_ROOT.parent
MARKET_MONITOR = HOME / "market-monitor"
CURRENT_WEEK = f"{datetime.now().year}-W{datetime.now().isocalendar()[1]:02d}"

WEEKLY_TARGETS = {
    "yt_longform": 1,
    "deal_of_week": 1,
    "tiktok": 3,
    "yt_short": 1,
    "blog": 1,
    "newsletter": 1,
    "gmb": 3,
    "community": 2,
    "social": 1,
    "bp": 1,
    "audit": 1,
}


def parse_date(value: str) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return None


def count_week_output(week: str) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    week_dir = OUTPUT_DIR / week
    if not week_dir.exists():
        return dict(counts)

    produced = week_dir / "produced"
    if produced.exists():
        for slug_dir in produced.iterdir():
            if not slug_dir.is_dir():
                continue
            files = {f.name for f in slug_dir.iterdir() if f.is_file()}
            if "youtube-description.md" in files:
                counts["yt_longform"] += 1
            counts["tiktok"] += len([name for name in files if name.startswith("tiktok-clip")])
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

    for dirname, key in [
        ("deal-of-the-week", "deal_of_week"),
        ("blog", "blog"),
        ("newsletter", "newsletter"),
        ("gmb", "gmb"),
        ("community", "community"),
        ("bp", "bp"),
        ("audit", "audit"),
        ("tiktok", "tiktok"),
    ]:
        folder = week_dir / dirname
        if folder.exists():
            files = [f for f in folder.rglob("*") if f.is_file()]
            if files:
                counts[key] = max(counts[key], len(files) if key in {"tiktok", "gmb", "community"} else 1)
    return dict(counts)


def latest_market_files(limit: int = 8) -> list[dict[str, Any]]:
    if not MARKET_MONITOR.exists():
        return []
    rows = []
    for path in MARKET_MONITOR.rglob("*.csv"):
        try:
            stat = path.stat()
        except OSError:
            continue
        rows.append({
            "path": str(path),
            "modified": stat.st_mtime,
            "modified_date": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d"),
            "bytes": stat.st_size,
        })
    rows.sort(key=lambda item: item["modified"], reverse=True)
    return rows[:limit]


def registry_summary(rows: list[dict[str, str]]) -> dict[str, Any]:
    valid_states = load_valid_states()
    now = datetime.now()
    status_counts = Counter(row.get("status", "") or "UNKNOWN" for row in rows)
    platform_counts = Counter(row.get("platform", "") or "UNKNOWN" for row in rows)
    persona_counts = Counter(row.get("persona", "") or "UNKNOWN" for row in rows)
    invalid_states = [
        {"title": row.get("title", ""), "status": row.get("status", "")}
        for row in rows
        if row.get("status") and row.get("status") not in valid_states
    ]
    missing_page_links = [
        row.get("title", "")
        for row in rows
        if row.get("status") == "PUBLISHED"
        and row.get("content_type") in {"video", "youtube_longform"}
        and not row.get("related_page_slug")
    ]
    stuck = []
    for row in rows:
        if row.get("status") not in {"SCRIPTED", "FILMED", "EDITED", "READY_TO_PUBLISH", "REPURPOSING"}:
            continue
        created = parse_date(row.get("created_date", ""))
        days = (now - created).days if created else None
        if days is None or days > 3:
            stuck.append({
                "title": row.get("title", ""),
                "status": row.get("status", ""),
                "days": days,
            })
    stuck.sort(key=lambda item: item["days"] or 9999, reverse=True)
    refresh_due = []
    for row in rows:
        due = parse_date(row.get("refresh_due_date", ""))
        if due and due < now:
            refresh_due.append({
                "title": row.get("title", ""),
                "days_overdue": (now - due).days,
                "related_page_slug": row.get("related_page_slug", ""),
            })
    refresh_due.sort(key=lambda item: item["days_overdue"], reverse=True)
    return {
        "total_rows": len(rows),
        "status_counts": dict(status_counts),
        "platform_counts": dict(platform_counts),
        "persona_counts": dict(persona_counts),
        "invalid_states": invalid_states,
        "missing_page_links": missing_page_links,
        "stuck": stuck[:12],
        "refresh_due": refresh_due[:12],
    }


def production_gaps(counts: dict[str, int]) -> list[dict[str, Any]]:
    gaps = []
    for key, target in WEEKLY_TARGETS.items():
        produced = counts.get(key, 0)
        if produced < target:
            gaps.append({"asset": key, "target": target, "produced": produced, "remaining": target - produced})
    return gaps


def build_snapshot(week: str) -> dict[str, Any]:
    rows = load_registry()
    week_counts = count_week_output(week)
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "project_root": str(PROJECT_ROOT),
        "week": week,
        "registry": registry_summary(rows),
        "weekly_output": {
            "counts": week_counts,
            "gaps": production_gaps(week_counts),
        },
        "market_monitor": {
            "root": str(MARKET_MONITOR),
            "latest_csv_files": latest_market_files(),
        },
        "approval_rule": "All social outputs remain drafts until Taylor approves posting, sending, scheduling, CRM writes, or site changes.",
    }


def render_markdown(snapshot: dict[str, Any]) -> str:
    reg = snapshot["registry"]
    output = snapshot["weekly_output"]
    market_files = snapshot["market_monitor"]["latest_csv_files"]
    lines = [
        "# Social OS Snapshot",
        "",
        f"Generated: {snapshot['generated_at']}",
        f"Week: {snapshot['week']}",
        "",
        "## Registry",
        f"- Assets: {reg['total_rows']}",
        f"- Status counts: {json.dumps(reg['status_counts'], sort_keys=True)}",
        f"- Platform counts: {json.dumps(reg['platform_counts'], sort_keys=True)}",
        f"- Persona counts: {json.dumps(reg['persona_counts'], sort_keys=True)}",
        f"- Invalid states: {len(reg['invalid_states'])}",
        f"- Published videos missing page links: {len(reg['missing_page_links'])}",
        f"- Stuck active assets surfaced: {len(reg['stuck'])}",
        f"- Refresh-due assets surfaced: {len(reg['refresh_due'])}",
        "",
        "## This Week",
        f"- Output counts: {json.dumps(output['counts'], sort_keys=True)}",
        f"- Gaps: {len(output['gaps'])}",
    ]
    for gap in output["gaps"][:12]:
        lines.append(f"  - {gap['asset']}: {gap['produced']}/{gap['target']} done")
    lines.extend([
        "",
        "## Priority Queue",
    ])
    for item in reg["stuck"][:5]:
        age = "unknown age" if item["days"] is None else f"{item['days']} days"
        lines.append(f"- Complete: {item['title']} ({item['status']}, {age})")
    for item in reg["refresh_due"][:3]:
        lines.append(f"- Refresh: {item['title']} ({item['days_overdue']} days overdue)")
    if output["gaps"]:
        top_gap = output["gaps"][0]
        lines.append(f"- Fill weekly gap: {top_gap['asset']} ({top_gap['remaining']} remaining)")
    lines.extend([
        "",
        "## Fresh Market Inputs",
    ])
    for file in market_files[:5]:
        lines.append(f"- {file['modified_date']}: {file['path']}")
    lines.extend([
        "",
        "## Approval Gate",
        f"- {snapshot['approval_rule']}",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a local social OS command-center snapshot.")
    parser.add_argument("--week", default=CURRENT_WEEK)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--out", help="Optional output path for markdown or JSON.")
    args = parser.parse_args()

    snapshot = build_snapshot(args.week)
    body = json.dumps(snapshot, indent=2) if args.json else render_markdown(snapshot)

    if args.out:
        out_path = Path(args.out)
        if not out_path.is_absolute():
            out_path = PROJECT_ROOT / out_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(body + "\n", encoding="utf-8")
        print(str(out_path))
    else:
        print(body)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
