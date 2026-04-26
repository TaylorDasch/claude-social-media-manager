"""Dataclasses for intake, draft, and compliance objects."""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _gen_id(prefix: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    import secrets
    return f"{prefix}_{ts}_{secrets.token_hex(3)}"


@dataclass
class Intake:
    id: str = field(default_factory=lambda: _gen_id("intk"))
    source_type: str = "manual"
    source_title: str | None = None
    source_url: str | None = None
    raw_input: str = ""
    audience: str = "general_local"
    market: str = "Temple, TX"
    funnel_stage: str = "awareness"
    status: str = "new"
    created_at: str = field(default_factory=_now)
    updated_at: str = field(default_factory=_now)
    notes: str | None = None

    def to_row(self) -> tuple:
        return (
            self.id, self.source_type, self.source_title, self.source_url,
            self.raw_input, self.audience, self.market, self.funnel_stage,
            self.status, self.created_at, self.updated_at, self.notes,
        )


@dataclass
class Draft:
    id: str = field(default_factory=lambda: _gen_id("drft"))
    intake_id: str | None = None
    platform: str = ""
    body: str = ""
    hook_options: list[str] = field(default_factory=list)
    selected_hook: str | None = None
    cta: str | None = None
    hashtags: list[str] = field(default_factory=list)
    suggested_asset: str | None = None
    suggested_broll: str | None = None
    repurpose_ideas: list[str] = field(default_factory=list)
    compliance_flags: list[dict[str, Any]] = field(default_factory=list)
    status: str = "draft"
    approval_notes: str | None = None
    source_path: str | None = None
    created_at: str = field(default_factory=_now)
    updated_at: str = field(default_factory=_now)

    def to_row(self) -> tuple:
        return (
            self.id, self.intake_id, self.platform, self.body,
            json.dumps(self.hook_options), self.selected_hook, self.cta,
            json.dumps(self.hashtags), self.suggested_asset,
            self.suggested_broll, json.dumps(self.repurpose_ideas),
            json.dumps(self.compliance_flags), self.status,
            self.approval_notes, self.source_path,
            self.created_at, self.updated_at,
        )

    @classmethod
    def from_row(cls, row) -> "Draft":
        return cls(
            id=row["id"],
            intake_id=row["intake_id"],
            platform=row["platform"],
            body=row["body"],
            hook_options=json.loads(row["hook_options"] or "[]"),
            selected_hook=row["selected_hook"],
            cta=row["cta"],
            hashtags=json.loads(row["hashtags"] or "[]"),
            suggested_asset=row["suggested_asset"],
            suggested_broll=row["suggested_broll"],
            repurpose_ideas=json.loads(row["repurpose_ideas"] or "[]"),
            compliance_flags=json.loads(row["compliance_flags"] or "[]"),
            status=row["status"],
            approval_notes=row["approval_notes"],
            source_path=row["source_path"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )


@dataclass
class ComplianceFlag:
    rule: str
    severity: str  # "hard" | "soft"
    message: str
    match: str | None = None
    line: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
