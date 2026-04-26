"""SQLite helpers for the drafts/intake/approval queue.

Stores state in `data/drafts.db` by default. Schema is idempotent; safe
to call `init_db()` on every CLI invocation.
"""
from __future__ import annotations

import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = REPO_ROOT / "data" / "drafts.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS intake (
    id           TEXT PRIMARY KEY,
    source_type  TEXT NOT NULL,
    source_title TEXT,
    source_url   TEXT,
    raw_input    TEXT,
    audience     TEXT,
    market       TEXT,
    funnel_stage TEXT,
    status       TEXT DEFAULT 'new',
    created_at   TEXT NOT NULL,
    updated_at   TEXT NOT NULL,
    notes        TEXT
);

CREATE TABLE IF NOT EXISTS drafts (
    id               TEXT PRIMARY KEY,
    intake_id        TEXT,
    platform         TEXT NOT NULL,
    body             TEXT NOT NULL,
    hook_options     TEXT,
    selected_hook    TEXT,
    cta              TEXT,
    hashtags         TEXT,
    suggested_asset  TEXT,
    suggested_broll  TEXT,
    repurpose_ideas  TEXT,
    compliance_flags TEXT,
    status           TEXT DEFAULT 'draft',
    approval_notes   TEXT,
    source_path      TEXT,
    created_at       TEXT NOT NULL,
    updated_at       TEXT NOT NULL,
    FOREIGN KEY (intake_id) REFERENCES intake(id)
);

CREATE TABLE IF NOT EXISTS approval_events (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    draft_id    TEXT NOT NULL,
    from_status TEXT,
    to_status   TEXT NOT NULL,
    actor       TEXT,
    note        TEXT,
    created_at  TEXT NOT NULL,
    FOREIGN KEY (draft_id) REFERENCES drafts(id)
);

CREATE INDEX IF NOT EXISTS idx_intake_status    ON intake(status);
CREATE INDEX IF NOT EXISTS idx_intake_audience  ON intake(audience);
CREATE INDEX IF NOT EXISTS idx_drafts_status    ON drafts(status);
CREATE INDEX IF NOT EXISTS idx_drafts_platform  ON drafts(platform);
CREATE INDEX IF NOT EXISTS idx_drafts_intake    ON drafts(intake_id);
CREATE INDEX IF NOT EXISTS idx_approval_draft   ON approval_events(draft_id);
"""


def db_path() -> Path:
    env = os.environ.get("SMM_DB_PATH")
    return Path(env).expanduser().resolve() if env else DEFAULT_DB_PATH


_SCHEMA_READY: set[str] = set()


def init_db(path: Path | None = None) -> Path:
    p = path or db_path()
    key = str(p)
    if key in _SCHEMA_READY:
        return p
    p.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(p)
    try:
        conn.executescript(SCHEMA)
        conn.commit()
    finally:
        conn.close()
    _SCHEMA_READY.add(key)
    return p


@contextmanager
def connect(path: Path | None = None) -> Iterator[sqlite3.Connection]:
    p = init_db(path)
    conn = sqlite3.connect(p)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()
