"""CSV + JSON exporters for approved drafts."""
from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path

from .drafts import list_drafts

REPO_ROOT = Path(__file__).resolve().parent.parent
EXPORT_DIR = REPO_ROOT / "exports"

CSV_FIELDS = [
    "id", "intake_id", "platform", "status", "selected_hook", "body",
    "cta", "hashtags", "suggested_asset", "suggested_broll",
    "created_at", "updated_at", "source_path",
]


def _iso_date() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d")


def _ensure_export_dir() -> Path:
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    return EXPORT_DIR


def export_approved_csv(platform: str | None = None,
                        out_path: Path | None = None) -> Path:
    _ensure_export_dir()
    if out_path is None:
        suffix = f"-{platform}" if platform else ""
        out_path = EXPORT_DIR / f"{_iso_date()}-approved{suffix}.csv"
    drafts = list_drafts(status="approved", platform=platform, limit=10_000)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        w.writeheader()
        for d in drafts:
            row = {k: getattr(d, k) for k in CSV_FIELDS if hasattr(d, k)}
            # serialize list fields
            if isinstance(row.get("hashtags"), list):
                row["hashtags"] = " ".join(row["hashtags"])
            w.writerow(row)
    return out_path


def export_approved_json(platform: str | None = None,
                         out_path: Path | None = None) -> Path:
    _ensure_export_dir()
    if out_path is None:
        suffix = f"-{platform}" if platform else ""
        out_path = EXPORT_DIR / f"{_iso_date()}-approved{suffix}.json"
    drafts = list_drafts(status="approved", platform=platform, limit=10_000)
    payload = []
    for d in drafts:
        payload.append({
            "id": d.id, "intake_id": d.intake_id, "platform": d.platform,
            "status": d.status, "selected_hook": d.selected_hook,
            "body": d.body, "cta": d.cta, "hashtags": d.hashtags,
            "suggested_asset": d.suggested_asset,
            "suggested_broll": d.suggested_broll,
            "repurpose_ideas": d.repurpose_ideas,
            "compliance_flags": d.compliance_flags,
            "created_at": d.created_at, "updated_at": d.updated_at,
            "source_path": d.source_path,
        })
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return out_path
