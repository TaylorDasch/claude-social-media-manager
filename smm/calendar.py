"""Weekly calendar view + gap analysis over drafts DB + content-registry.csv."""
from __future__ import annotations

import csv
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

from .drafts import list_drafts

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTENT_REGISTRY = REPO_ROOT / "data" / "content-registry.csv"

# Target weekly mix (configurable)
DEFAULT_WEEKLY_MIX = {
    "investor_education": 0.40,
    "relocation_lifestyle": 0.30,
    "market_authority": 0.15,
    "listing_examples": 0.10,
    "personal_bts": 0.05,
}


def iso_week_key(d: date | None = None) -> str:
    d = d or date.today()
    y, w, _ = d.isocalendar()
    return f"{y}-W{w:02d}"


def drafts_by_platform(status: str | None = None) -> dict[str, int]:
    rows = list_drafts(status=status, limit=10_000)
    return dict(Counter(d.platform for d in rows))


def weekly_snapshot() -> dict:
    """Summarize pending/approved/posted drafts + this week's output/ folder."""
    wk = iso_week_key()
    pending = list_drafts(status="needs_review", limit=10_000) + list_drafts(status="draft", limit=10_000)
    approved = list_drafts(status="approved", limit=10_000)
    scheduled = list_drafts(status="scheduled", limit=10_000)
    posted = list_drafts(status="posted", limit=10_000)

    output_dir = REPO_ROOT / "output" / wk
    output_files = []
    if output_dir.exists():
        for p in sorted(output_dir.rglob("*")):
            if p.is_file():
                output_files.append(str(p.relative_to(REPO_ROOT)))
    return {
        "week": wk,
        "counts": {
            "pending": len(pending),
            "approved": len(approved),
            "scheduled": len(scheduled),
            "posted": len(posted),
        },
        "pending_by_platform": dict(Counter(d.platform for d in pending)),
        "approved_by_platform": dict(Counter(d.platform for d in approved)),
        "output_files_this_week": output_files,
    }


def content_registry_gaps() -> dict:
    """Read content-registry.csv and surface stale/idea rows."""
    gaps = {"idea": [], "refresh_due": [], "draft": []}
    if not CONTENT_REGISTRY.exists():
        return gaps
    with CONTENT_REGISTRY.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        today = date.today()
        for row in reader:
            status = (row.get("status") or "").upper()
            due = row.get("refresh_due_date") or ""
            if status == "IDEA":
                gaps["idea"].append({"id": row["content_id"], "title": row.get("title")})
            elif status == "DRAFT":
                gaps["draft"].append({"id": row["content_id"], "title": row.get("title")})
            if due:
                try:
                    dt = datetime.fromisoformat(due).date()
                    if dt <= today and status == "PUBLISHED":
                        gaps["refresh_due"].append({
                            "id": row["content_id"],
                            "title": row.get("title"),
                            "due": due,
                        })
                except ValueError:
                    pass
    return gaps


def mix_vs_target(weekly_mix: dict | None = None) -> dict:
    """Compute weekly audience mix vs target from current pending+approved drafts."""
    target = weekly_mix or DEFAULT_WEEKLY_MIX
    buckets = defaultdict(int)
    total = 0
    for d in list_drafts(status="approved", limit=10_000):
        total += 1
        buckets[d.platform] += 1
    for d in list_drafts(status="needs_review", limit=10_000):
        total += 1
        buckets[d.platform] += 1
    if not total:
        return {"target": target, "actual_by_platform": {}, "total": 0}
    return {
        "target": target,
        "actual_by_platform": dict(buckets),
        "total": total,
    }
