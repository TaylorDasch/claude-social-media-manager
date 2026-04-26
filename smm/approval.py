"""Approval workflow helpers.

Transitions draft.status with compliance-gate enforcement.
"""
from __future__ import annotations

from . import DRAFT_STATUSES
from .compliance import has_hard_violation
from .drafts import get_draft, set_status


class ComplianceError(RuntimeError):
    pass


def approve(draft_id: str, note: str | None = None,
            force: bool = False) -> tuple[bool, str]:
    """Mark a draft approved. Refuses if HARD compliance flags exist unless --force."""
    d = get_draft(draft_id)
    if not d:
        return False, f"Draft {draft_id} not found"
    if has_hard_violation(d.compliance_flags) and not force:
        msg = f"Blocked — HARD compliance flags on {draft_id}. Fix or re-run with --force."
        return False, msg
    ok = set_status(draft_id, "approved", note=note, actor="taylor")
    return ok, "approved" if ok else "no-op"


def reject(draft_id: str, note: str | None = None) -> tuple[bool, str]:
    ok = set_status(draft_id, "rejected", note=note, actor="taylor")
    return ok, "rejected" if ok else "no-op"


def request_revision(draft_id: str, note: str | None = None) -> tuple[bool, str]:
    ok = set_status(draft_id, "needs_review", note=note, actor="taylor")
    return ok, "marked needs_review" if ok else "no-op"


def mark_scheduled(draft_id: str, note: str | None = None) -> tuple[bool, str]:
    ok = set_status(draft_id, "scheduled", note=note, actor="taylor")
    return ok, "scheduled" if ok else "no-op"


def mark_posted(draft_id: str, note: str | None = None) -> tuple[bool, str]:
    ok = set_status(draft_id, "posted", note=note, actor="taylor")
    return ok, "posted" if ok else "no-op"


def pending_drafts(platform: str | None = None) -> list:
    from .drafts import list_drafts
    out = []
    for s in ("needs_review", "draft"):
        out.extend(list_drafts(status=s, platform=platform))
    return out


def approved_not_exported(platform: str | None = None) -> list:
    from .drafts import list_drafts
    return list_drafts(status="approved", platform=platform)
