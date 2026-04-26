"""Draft CRUD + state transitions + compliance hook."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from . import DRAFT_STATUSES
from .db import connect
from .models import Draft


def add_draft(draft: Draft) -> str:
    # Always pass compliance BEFORE storing so flags are visible in listings.
    from .compliance import check_draft
    draft.compliance_flags = [f.to_dict() for f in check_draft(draft)]
    with connect() as conn:
        conn.execute(
            """INSERT INTO drafts
               (id, intake_id, platform, body, hook_options, selected_hook,
                cta, hashtags, suggested_asset, suggested_broll,
                repurpose_ideas, compliance_flags, status, approval_notes,
                source_path, created_at, updated_at)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            draft.to_row(),
        )
        conn.execute(
            """INSERT INTO approval_events
               (draft_id, from_status, to_status, actor, note, created_at)
               VALUES (?,?,?,?,?,?)""",
            (draft.id, None, draft.status, "cli", "created", draft.created_at),
        )
    return draft.id


def get_draft(draft_id: str) -> Draft | None:
    with connect() as conn:
        row = conn.execute("SELECT * FROM drafts WHERE id = ?", (draft_id,)).fetchone()
    return Draft.from_row(row) if row else None


def list_drafts(status: str | None = None, platform: str | None = None,
                intake_id: str | None = None, limit: int = 100) -> list[Draft]:
    q = "SELECT * FROM drafts"
    clauses, params = [], []
    if status:
        clauses.append("status = ?"); params.append(status)
    if platform:
        clauses.append("platform = ?"); params.append(platform)
    if intake_id:
        clauses.append("intake_id = ?"); params.append(intake_id)
    if clauses:
        q += " WHERE " + " AND ".join(clauses)
    q += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)
    with connect() as conn:
        rows = conn.execute(q, params).fetchall()
    return [Draft.from_row(r) for r in rows]


def set_status(draft_id: str, new_status: str, note: str | None = None,
               actor: str = "taylor") -> bool:
    if new_status not in DRAFT_STATUSES:
        raise ValueError(f"invalid status {new_status!r}; allowed: {DRAFT_STATUSES}")
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with connect() as conn:
        row = conn.execute(
            "SELECT status FROM drafts WHERE id = ?", (draft_id,)
        ).fetchone()
        if not row:
            return False
        old = row["status"]
        conn.execute(
            "UPDATE drafts SET status = ?, updated_at = ?, approval_notes = COALESCE(?, approval_notes) WHERE id = ?",
            (new_status, ts, note, draft_id),
        )
        conn.execute(
            """INSERT INTO approval_events
               (draft_id, from_status, to_status, actor, note, created_at)
               VALUES (?,?,?,?,?,?)""",
            (draft_id, old, new_status, actor, note, ts),
        )
    return True


def edit_draft(draft_id: str, **fields) -> bool:
    """Update arbitrary fields. Re-runs compliance after body/platform change."""
    if not fields:
        return False
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    serializable = {}
    for k, v in fields.items():
        if isinstance(v, (list, dict)):
            serializable[k] = json.dumps(v)
        else:
            serializable[k] = v
    allowed = {
        "body", "platform", "selected_hook", "cta", "hashtags",
        "suggested_asset", "suggested_broll", "repurpose_ideas",
        "approval_notes", "source_path", "hook_options",
    }
    filtered = {k: v for k, v in serializable.items() if k in allowed}
    if not filtered:
        return False
    sets = ", ".join(f"{k} = ?" for k in filtered)
    params = list(filtered.values()) + [ts, draft_id]
    with connect() as conn:
        cur = conn.execute(
            f"UPDATE drafts SET {sets}, updated_at = ? WHERE id = ?", params
        )
        changed = cur.rowcount > 0
    if changed and ("body" in fields or "platform" in fields):
        # rerun compliance
        d = get_draft(draft_id)
        if d:
            from .compliance import check_draft
            flags = [f.to_dict() for f in check_draft(d)]
            with connect() as conn:
                conn.execute(
                    "UPDATE drafts SET compliance_flags = ?, updated_at = ? WHERE id = ?",
                    (json.dumps(flags), ts, draft_id),
                )
    return changed


def import_file_as_draft(path: Path, platform: str,
                         intake_id: str | None = None) -> str:
    """Load a file from output/ or anywhere and stage it as a draft."""
    text = path.read_text(encoding="utf-8")
    d = Draft(
        intake_id=intake_id,
        platform=platform,
        body=text,
        source_path=str(path),
        status="needs_review",
    )
    return add_draft(d)


def delete_draft(draft_id: str) -> bool:
    with connect() as conn:
        cur = conn.execute("DELETE FROM drafts WHERE id = ?", (draft_id,))
    return cur.rowcount > 0


def approval_history(draft_id: str) -> list[dict]:
    with connect() as conn:
        rows = conn.execute(
            "SELECT * FROM approval_events WHERE draft_id = ? ORDER BY id ASC",
            (draft_id,),
        ).fetchall()
    return [dict(r) for r in rows]
