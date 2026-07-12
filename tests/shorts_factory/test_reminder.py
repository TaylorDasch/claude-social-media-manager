from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from shorts_factory.reminder import run_reminder, scan_pending


def write_job(root: Path, *, statuses: list[str]) -> None:
    directory = root / "jobs" / "temple-vs-belton"
    directory.mkdir(parents=True)
    payload = {
        "schema_version": "shorts-job/v1",
        "revision": 1,
        "job_id": "temple-vs-belton",
        "title": "Temple vs. Belton",
        "updated_at": "2026-07-12T16:00:00+00:00",
        "clips": [
            {"id": f"clip-{index}", "status": status, "score": 90 - index}
            for index, status in enumerate(statuses, start=1)
        ],
    }
    (directory / "job.json").write_text(json.dumps(payload), encoding="utf-8")


def test_scan_only_returns_awaiting_review(tmp_path: Path) -> None:
    write_job(tmp_path, statuses=["awaiting_review", "approved", "declined"])
    pending, errors = scan_pending(tmp_path)
    assert not errors
    assert [item.clip_id for item in pending] == ["clip-1"]


def test_reminder_notifies_once_then_deduplicates(tmp_path: Path) -> None:
    write_job(tmp_path, statuses=["awaiting_review", "awaiting_review"])
    sent: list[tuple[str, str]] = []
    now = datetime(2026, 7, 12, 16, tzinfo=timezone.utc)
    first = run_reminder(
        root=tmp_path,
        notify=True,
        notifier=lambda title, message: sent.append((title, message)),
        now=now,
    )
    assert first["sent"] is True
    assert first["pending_count"] == 2
    assert len(sent) == 1

    second = run_reminder(
        root=tmp_path,
        notify=True,
        notifier=lambda title, message: sent.append((title, message)),
        now=now + timedelta(hours=2),
    )
    assert second["due"] is False
    assert second["sent"] is False
    assert len(sent) == 1

    third = run_reminder(
        root=tmp_path,
        notify=True,
        notifier=lambda title, message: sent.append((title, message)),
        now=now + timedelta(hours=25),
    )
    assert third["sent"] is True
    assert len(sent) == 2


def test_dry_run_never_updates_ledger(tmp_path: Path) -> None:
    write_job(tmp_path, statuses=["awaiting_review"])
    result = run_reminder(root=tmp_path, notify=False)
    assert result["due"] is True
    assert result["sent"] is False
    assert not (tmp_path / "reminders" / "ledger.json").exists()


def test_failed_job_produces_one_deduplicated_attention_alert(tmp_path: Path) -> None:
    directory = tmp_path / "jobs" / "failed-job"
    directory.mkdir(parents=True)
    (directory / "job.json").write_text(
        json.dumps(
            {
                "schema_version": "shorts-job/v1",
                "revision": 3,
                "job_id": "failed-job",
                "title": "Failed job",
                "status": "failed",
                "clips": [],
                "error": {"message": "Ranking provider unavailable"},
            }
        ),
        encoding="utf-8",
    )
    alerts, errors = scan_pending(tmp_path)
    assert not errors
    assert len(alerts) == 1
    assert alerts[0].status == "failed"
    result = run_reminder(root=tmp_path, notify=False)
    assert result["due"] is True
    assert "failed" in result["notification"]["title"].lower()
