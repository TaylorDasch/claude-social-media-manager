"""Ayrshare scheduler stub.

If AYRSHARE_API_KEY is set, live pushes could be wired via urllib. Without
creds, returns a no-op.
"""
from __future__ import annotations

import os


def _configured() -> bool:
    return bool(os.environ.get("AYRSHARE_API_KEY"))


def push(platform: str | None = None, dry_run: bool = True) -> dict:
    if not _configured():
        return {
            "ok": False,
            "mode": "ayrshare",
            "reason": "AYRSHARE_API_KEY not set — CSV export is the default",
        }
    return {
        "ok": False,
        "mode": "ayrshare",
        "dry_run": dry_run,
        "reason": "Ayrshare live push not yet implemented",
    }
