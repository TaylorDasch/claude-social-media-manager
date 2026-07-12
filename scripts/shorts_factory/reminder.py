"""Deduplicated local reminders for shorts awaiting Taylor's review."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import plistlib
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Sequence

from .errors import ManifestError
from .storage import DEFAULT_ROOT, atomic_write_json, read_json, utc_now


LABEL = "com.taylor.shorts-review-reminder"
DEFAULT_INTERVAL_SECONDS = 4 * 60 * 60
DEFAULT_REPEAT_HOURS = 24.0


@dataclass(frozen=True)
class PendingReview:
    job_id: str
    job_title: str
    clip_id: str
    score: float | None
    updated_at: str | None
    status: str
    version: int
    render_sha256: str | None


Notifier = Callable[[str, str], None]


def scan_pending(root: Path) -> tuple[list[PendingReview], list[str]]:
    jobs_dir = root.expanduser() / "jobs"
    if not jobs_dir.is_dir():
        return [], []
    pending: list[PendingReview] = []
    errors: list[str] = []
    for manifest_path in sorted(jobs_dir.glob("*/job.json")):
        try:
            job = read_json(manifest_path)
            clips = job.get("clips")
            if not isinstance(clips, list):
                raise ValueError("clips is not a list")
            for clip in clips:
                if not isinstance(clip, dict) or clip.get("status") != "awaiting_review":
                    continue
                raw_score = clip.get("score")
                pending.append(
                    PendingReview(
                        job_id=str(job.get("job_id", manifest_path.parent.name)),
                        job_title=str(job.get("title") or job.get("job_id") or "Shorts job"),
                        clip_id=str(clip.get("id", "unknown")),
                        score=float(raw_score) if isinstance(raw_score, (int, float)) else None,
                        updated_at=str(job.get("updated_at")) if job.get("updated_at") else None,
                        status="awaiting_review",
                        version=int(clip.get("version", 1)),
                        render_sha256=(
                            str(clip.get("render", {}).get("sha256"))
                            if isinstance(clip.get("render"), dict)
                            and clip.get("render", {}).get("sha256")
                            else None
                        ),
                    )
                )
            if job.get("status") == "failed":
                error = job.get("error") if isinstance(job.get("error"), dict) else {}
                pending.append(
                    PendingReview(
                        job_id=str(job.get("job_id", manifest_path.parent.name)),
                        job_title=str(job.get("title") or job.get("job_id") or "Shorts job"),
                        clip_id="job-failure",
                        score=None,
                        updated_at=str(job.get("updated_at")) if job.get("updated_at") else None,
                        status="failed",
                        version=int(job.get("revision", 0)),
                        render_sha256=hashlib.sha256(
                            str(error.get("message", "failed")).encode("utf-8")
                        ).hexdigest(),
                    )
                )
        except (OSError, ValueError, TypeError, ManifestError) as exc:
            errors.append(f"{manifest_path}: {exc}")
    pending.sort(key=lambda item: (-(item.score or 0), item.job_id, item.clip_id))
    return pending, errors


def _fingerprint(pending: list[PendingReview]) -> str:
    payload = "\n".join(
        f"{item.job_id}:{item.clip_id}:{item.version}:{item.render_sha256}:{item.status}:{item.score}"
        for item in pending
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _parse_time(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        return None


def notification_copy(pending: list[PendingReview]) -> tuple[str, str]:
    count = len(pending)
    projects = len({item.job_id for item in pending})
    failures = sum(item.status == "failed" for item in pending)
    review_count = count - failures
    title = (
        f"Shorts Factory needs attention ({failures} failed)"
        if failures
        else f"{review_count} short{'s' if review_count != 1 else ''} need your review"
    )
    best = pending[0].score if pending else None
    score_note = f" Best hook score: {best:.0f}." if best is not None else ""
    message = (
        f"{projects} video project{'s' if projects != 1 else ''} waiting."
        f"{score_note} Open Command Center → Shorts Review to approve, revise, or decline."
    )
    return title, message


def macos_notify(title: str, message: str) -> None:
    def literal(value: str) -> str:
        return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'

    subprocess.run(
        [
            "/usr/bin/osascript",
            "-e",
            f"display notification {literal(message)} with title {literal(title)}",
        ],
        check=True,
        capture_output=True,
        text=True,
    )


def run_reminder(
    *,
    root: Path,
    notify: bool,
    repeat_hours: float = DEFAULT_REPEAT_HOURS,
    notifier: Notifier = macos_notify,
    now: datetime | None = None,
) -> dict[str, Any]:
    pending, errors = scan_pending(root)
    ledger_path = root.expanduser() / "reminders" / "ledger.json"
    timestamp = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    fingerprint = _fingerprint(pending)
    previous: dict[str, Any] = {}
    if ledger_path.exists():
        try:
            previous = read_json(ledger_path)
        except Exception:
            previous = {}
    last_sent = _parse_time(previous.get("sent_at"))
    unchanged = previous.get("fingerprint") == fingerprint
    too_soon = bool(
        last_sent and timestamp - last_sent < timedelta(hours=max(0.0, repeat_hours))
    )
    due = bool(pending) and not (unchanged and too_soon)
    sent = False
    title = message = None
    if due:
        title, message = notification_copy(pending)
        if notify:
            notifier(title, message)
            sent = True
            atomic_write_json(
                ledger_path,
                {
                    "schema_version": "shorts-reminder-ledger/v1",
                    "fingerprint": fingerprint,
                    "sent_at": timestamp.isoformat(),
                    "pending_count": len(pending),
                    "job_ids": sorted({item.job_id for item in pending}),
                },
            )
    return {
        "ok": not errors,
        "checked_at": timestamp.isoformat(),
        "pending_count": len(pending),
        "project_count": len({item.job_id for item in pending}),
        "due": due,
        "sent": sent,
        "notification": {"title": title, "message": message} if title else None,
        "errors": errors,
    }


def launch_agent_path() -> Path:
    return Path.home() / "Library" / "LaunchAgents" / f"{LABEL}.plist"


def install_launch_agent(
    *, root: Path, interval_seconds: int = DEFAULT_INTERVAL_SECONDS
) -> Path:
    if interval_seconds < 900:
        raise ValueError("reminder interval must be at least 15 minutes")
    plist_path = launch_agent_path()
    plist_path.parent.mkdir(parents=True, exist_ok=True)
    logs = root.expanduser() / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    scripts_root = Path(__file__).resolve().parents[1]
    payload = {
        "Label": LABEL,
        "ProgramArguments": [
            sys.executable,
            "-m",
            "shorts_factory.reminder",
            "run",
            "--root",
            str(root.expanduser().resolve()),
            "--notify",
        ],
        "EnvironmentVariables": {"PYTHONPATH": str(scripts_root)},
        "StartInterval": int(interval_seconds),
        "RunAtLoad": True,
        "ProcessType": "Background",
        "StandardOutPath": str(logs / "review-reminder.out.log"),
        "StandardErrorPath": str(logs / "review-reminder.err.log"),
    }
    temporary = plist_path.with_suffix(".plist.tmp")
    with temporary.open("wb") as handle:
        plistlib.dump(payload, handle, sort_keys=True)
    os.replace(temporary, plist_path)
    domain = f"gui/{os.getuid()}"
    subprocess.run(
        ["/bin/launchctl", "bootout", domain, str(plist_path)],
        check=False,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["/bin/launchctl", "bootstrap", domain, str(plist_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["/bin/launchctl", "enable", f"{domain}/{LABEL}"],
        check=True,
        capture_output=True,
        text=True,
    )
    return plist_path


def uninstall_launch_agent() -> Path:
    plist_path = launch_agent_path()
    domain = f"gui/{os.getuid()}"
    subprocess.run(
        ["/bin/launchctl", "bootout", domain, str(plist_path)],
        check=False,
        capture_output=True,
        text=True,
    )
    plist_path.unlink(missing_ok=True)
    return plist_path


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    run = subparsers.add_parser("run", help="Check the queue once")
    run.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    run.add_argument("--notify", action="store_true")
    run.add_argument("--repeat-hours", type=float, default=DEFAULT_REPEAT_HOURS)
    install = subparsers.add_parser("install", help="Install the local launchd reminder")
    install.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    install.add_argument("--interval-seconds", type=int, default=DEFAULT_INTERVAL_SECONDS)
    subparsers.add_parser("uninstall", help="Remove the local launchd reminder")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "run":
        result = run_reminder(
            root=args.root,
            notify=args.notify,
            repeat_hours=args.repeat_hours,
        )
        print(json.dumps(result, indent=2))
        return 0 if result["ok"] else 1
    if args.command == "install":
        path = install_launch_agent(
            root=args.root, interval_seconds=args.interval_seconds
        )
        print(json.dumps({"ok": True, "installed": str(path)}, indent=2))
        return 0
    path = uninstall_launch_agent()
    print(json.dumps({"ok": True, "removed": str(path)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
