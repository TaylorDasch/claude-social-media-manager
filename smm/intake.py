"""Intake CRUD — register an idea, property note, transcript, etc."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable

from .db import connect
from .models import Intake


def add_intake(item: Intake) -> str:
    with connect() as conn:
        conn.execute(
            """INSERT INTO intake
               (id, source_type, source_title, source_url, raw_input,
                audience, market, funnel_stage, status, created_at,
                updated_at, notes)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            item.to_row(),
        )
    return item.id


def list_intake(status: str | None = None, audience: str | None = None,
                limit: int = 50) -> list[dict]:
    q = "SELECT * FROM intake"
    clauses, params = [], []
    if status:
        clauses.append("status = ?"); params.append(status)
    if audience:
        clauses.append("audience = ?"); params.append(audience)
    if clauses:
        q += " WHERE " + " AND ".join(clauses)
    q += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)
    with connect() as conn:
        rows = conn.execute(q, params).fetchall()
    return [dict(r) for r in rows]


def get_intake(intake_id: str) -> dict | None:
    with connect() as conn:
        row = conn.execute("SELECT * FROM intake WHERE id = ?", (intake_id,)).fetchone()
    return dict(row) if row else None


def update_intake_status(intake_id: str, status: str) -> bool:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with connect() as conn:
        cur = conn.execute(
            "UPDATE intake SET status = ?, updated_at = ? WHERE id = ?",
            (status, ts, intake_id),
        )
    return cur.rowcount > 0


def delete_intake(intake_id: str) -> bool:
    with connect() as conn:
        cur = conn.execute("DELETE FROM intake WHERE id = ?", (intake_id,))
    return cur.rowcount > 0


def count_by_audience() -> dict[str, int]:
    with connect() as conn:
        rows = conn.execute(
            "SELECT audience, COUNT(*) AS n FROM intake GROUP BY audience"
        ).fetchall()
    return {r["audience"]: r["n"] for r in rows}
