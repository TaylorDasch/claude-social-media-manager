"""CSV-export scheduler — always available, zero creds.

Writes approved drafts to `exports/` as CSV rows that can be uploaded to
Meta Business Suite / Postiz / Ayrshare / Buffer manually.
"""
from __future__ import annotations

from pathlib import Path

from ..exporters import export_approved_csv


def push(platform: str | None = None,
         out_path: Path | None = None) -> dict:
    p = export_approved_csv(platform=platform, out_path=out_path)
    return {"ok": True, "mode": "csv", "path": str(p)}
