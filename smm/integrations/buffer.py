"""Buffer scheduler stub.

If BUFFER_ACCESS_TOKEN is set, live pushes could be wired. Without creds,
returns a no-op.
"""
from __future__ import annotations

import os


def _configured() -> bool:
    return bool(os.environ.get("BUFFER_ACCESS_TOKEN"))


def push(platform: str | None = None, dry_run: bool = True) -> dict:
    if not _configured():
        return {
            "ok": False,
            "mode": "buffer",
            "reason": "BUFFER_ACCESS_TOKEN not set — CSV export is the default",
        }
    return {
        "ok": False,
        "mode": "buffer",
        "dry_run": dry_run,
        "reason": "Buffer live push not yet implemented",
    }
