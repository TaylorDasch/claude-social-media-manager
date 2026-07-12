"""Checksum-locked, idempotent Postiz draft handoff.

This module never schedules or publishes a post.  Its only network mutation is
creating a Postiz *draft*, and that path requires an approved render, the exact
approved SHA-256 supplied again by the operator, an eligible platform, and the
explicit ``--create-draft`` switch.
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterator, Sequence

from .errors import ManifestError
from .policy import find_banned_phrases, unresolved_claims
from .state import APPROVED, READY_TO_PUBLISH, aggregate_job_state, transition
from .storage import (
    DEFAULT_ROOT,
    atomic_write_json,
    manifest_lock,
    read_json,
    resolve_job_path,
    sha256_file,
    utc_now,
)


PLATFORM_IDENTIFIERS = {
    "instagram_reels": "instagram",
    "instagram": "instagram",
    "facebook_reels": "facebook",
    "facebook": "facebook",
    "youtube_shorts": "youtube",
    "youtube": "youtube",
    "tiktok": "tiktok",
}
PLATFORM_CANONICAL = {
    "instagram_reels": "instagram_reels",
    "instagram": "instagram_reels",
    "facebook_reels": "facebook_reels",
    "facebook": "facebook_reels",
    "youtube_shorts": "youtube_shorts",
    "youtube": "youtube_shorts",
    "tiktok": "tiktok",
}


@dataclass(frozen=True)
class PreparedHandoff:
    job_path: Path
    job_id: str
    clip_id: str
    version: int
    platform: str
    render_path: Path
    sha256: str
    caption: str
    caption_sha256: str
    title: str
    receipt_path: Path


Runner = Callable[[Sequence[str]], str]


def _run(command: Sequence[str]) -> str:
    completed = subprocess.run(
        list(command),
        check=True,
        capture_output=True,
        text=True,
        env={**os.environ, "NO_COLOR": "1"},
    )
    return completed.stdout


def _extract_json(output: str) -> Any:
    decoder = json.JSONDecoder()
    parsed: list[Any] = []
    for index, char in enumerate(output):
        if char not in "[{":
            continue
        try:
            value, end = decoder.raw_decode(output[index:])
        except json.JSONDecodeError:
            continue
        if not output[index + end :].strip():
            return value
        parsed.append(value)
    if not parsed:
        raise ManifestError("Postiz returned no machine-readable JSON")
    return parsed[-1]


def _clip(job: dict[str, Any], clip_id: str) -> dict[str, Any]:
    if not clip_id or not all(character.isalnum() or character in "._-" for character in clip_id):
        raise ManifestError("clip id contains unsafe path characters")
    clips = job.get("clips")
    if not isinstance(clips, list):
        raise ManifestError("job clips must be a list")
    match = next((item for item in clips if item.get("id") == clip_id), None)
    if not isinstance(match, dict):
        raise ManifestError(f"clip not found in job: {clip_id}")
    return match


def _approved_hash(clip: dict[str, Any]) -> str | None:
    decision = clip.get("decision")
    candidates: list[Any] = [clip.get("approved_sha256")]
    if isinstance(decision, dict):
        candidates.extend(
            [decision.get("approved_sha256"), decision.get("sha256")]
        )
    for candidate in candidates:
        if isinstance(candidate, str) and len(candidate) == 64:
            return candidate.lower()
    return None


def _render_path(job_path: Path, clip: dict[str, Any], root: Path) -> Path:
    render = clip.get("render") if isinstance(clip.get("render"), dict) else {}
    raw = next(
        (
            candidate
            for candidate in (
                render.get("path"),
                render.get("output_path"),
                clip.get("output_path"),
                clip.get("captioned_path"),
            )
            if isinstance(candidate, str) and candidate
        ),
        None,
    )
    if raw is None:
        raise ManifestError("approved clip has no rendered media path")
    candidate = Path(raw).expanduser()
    if not candidate.is_absolute():
        candidate = job_path.parent / candidate
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(root.expanduser().resolve(strict=True))
    except (FileNotFoundError, ValueError) as exc:
        raise ManifestError("render path is missing or outside the factory root") from exc
    if not resolved.is_file() or resolved.suffix.lower() != ".mp4":
        raise ManifestError("Postiz handoff requires a rendered MP4")
    return resolved


def _qa_passed(clip: dict[str, Any]) -> bool:
    render = clip.get("render") if isinstance(clip.get("render"), dict) else {}
    qa = render.get("qa") if isinstance(render.get("qa"), dict) else {}
    return qa.get("passed") is True


def _platform_allowed(clip: dict[str, Any], platform: str) -> tuple[bool, str | None]:
    values = clip.get("platform_eligibility")
    if not isinstance(values, dict) or platform not in values:
        return False, "platform eligibility was not evaluated"
    value = values[platform]
    if isinstance(value, bool):
        return value, None
    if isinstance(value, dict):
        reasons = value.get("reasons")
        detail = value.get("reason")
        if not detail and isinstance(reasons, list):
            detail = " ".join(str(reason) for reason in reasons if reason)
        return value.get("eligible") is True, str(detail or "") or None
    return False, "platform eligibility has an invalid value"


def _approved_publication_copy(clip: dict[str, Any]) -> tuple[str, str]:
    decision = clip.get("decision")
    if not isinstance(decision, dict):
        raise ManifestError("approval decision is missing")
    caption = decision.get("approved_caption")
    title = decision.get("approved_title")
    recorded_hash = decision.get("approved_caption_sha256")
    if not isinstance(caption, str) or not caption.strip():
        raise ManifestError("approval has no checksum-locked publication caption")
    if not isinstance(title, str) or len(title.strip()) < 2:
        raise ManifestError("approval has no locked platform title")
    actual_hash = hashlib.sha256(caption.encode("utf-8")).hexdigest()
    if recorded_hash != actual_hash:
        raise ManifestError("approved publication caption checksum does not match")
    banned = find_banned_phrases(f"{caption}\n{title}")
    if banned:
        raise ManifestError(
            "approved publication copy contains governance-banned language: "
            + ", ".join(banned)
        )
    if unresolved_claims(clip) and not isinstance(decision.get("claim_waiver"), dict):
        raise ManifestError(
            "unverified verify/high-risk claims lack Taylor's approval waiver"
        )
    return caption, title[:100]


def prepare_handoff(
    *,
    root: Path,
    job_ref: str | Path,
    clip_id: str,
    platform: str,
    confirmed_sha256: str,
) -> PreparedHandoff:
    if platform not in PLATFORM_IDENTIFIERS:
        raise ManifestError(f"unsupported Postiz platform: {platform}")
    canonical_platform = PLATFORM_CANONICAL[platform]
    job_path = resolve_job_path(root, job_ref)
    try:
        job_path.relative_to(root.expanduser().resolve(strict=True) / "jobs")
    except (FileNotFoundError, ValueError) as exc:
        raise ManifestError("Postiz job must be inside the factory jobs root") from exc
    job = read_json(job_path)
    clip = _clip(job, clip_id)
    status = str(clip.get("status"))
    if status not in {APPROVED, READY_TO_PUBLISH}:
        raise ManifestError("clip must be approved before Postiz handoff")
    if not _qa_passed(clip):
        raise ManifestError("clip technical QA has not passed")
    allowed, reason = _platform_allowed(clip, canonical_platform)
    if not allowed:
        detail = f": {reason}" if reason else ""
        raise ManifestError(f"clip is ineligible for {canonical_platform}{detail}")

    approved = _approved_hash(clip)
    if not approved:
        raise ManifestError("approval has no locked SHA-256 checksum")
    supplied = confirmed_sha256.strip().lower()
    if supplied != approved:
        raise ManifestError("--approved-sha256 does not match the approval lock")
    render_path = _render_path(job_path, clip, root)
    actual = sha256_file(render_path).lower()
    if actual != approved:
        raise ManifestError("render changed after approval; Postiz handoff blocked")

    version = int(clip.get("version", 1))
    receipt_path = (
        job_path.parent
        / "receipts"
        / "postiz"
        / f"{clip_id}-v{version}-{canonical_platform}.json"
    )
    caption, publication_title = _approved_publication_copy(clip)
    return PreparedHandoff(
        job_path=job_path,
        job_id=str(job.get("job_id", job_path.parent.name)),
        clip_id=clip_id,
        version=version,
        platform=canonical_platform,
        render_path=render_path,
        sha256=actual,
        caption=caption,
        caption_sha256=hashlib.sha256(caption.encode("utf-8")).hexdigest(),
        title=publication_title,
        receipt_path=receipt_path,
    )


def list_integrations(*, runner: Runner = _run, cli: str = "postiz") -> list[dict[str, Any]]:
    payload = _extract_json(runner([cli, "integrations:list"]))
    if not isinstance(payload, list):
        raise ManifestError("Postiz integration response was not a list")
    return [item for item in payload if isinstance(item, dict)]


def select_integration(
    integrations: list[dict[str, Any]],
    *,
    platform: str,
    profile: str | None = None,
) -> dict[str, Any]:
    identifier = PLATFORM_IDENTIFIERS[platform]
    matches = [
        item
        for item in integrations
        if item.get("identifier") == identifier and item.get("disabled") is not True
    ]
    if profile:
        needle = profile.casefold()
        matches = [
            item
            for item in matches
            if needle in {
                str(item.get("profile", "")).casefold(),
                str(item.get("name", "")).casefold(),
            }
        ]
    if not matches:
        raise ManifestError(f"no enabled Postiz integration matches {platform}")
    if len(matches) > 1:
        raise ManifestError(
            f"multiple Postiz integrations match {platform}; pass --profile exactly"
        )
    if not isinstance(matches[0].get("id"), str):
        raise ManifestError("Postiz integration has no id")
    return matches[0]


def _media_url(payload: Any) -> str:
    values = payload if isinstance(payload, list) else [payload]
    for value in values:
        if not isinstance(value, dict):
            continue
        for key in ("path", "url", "publicUrl", "public_url"):
            candidate = value.get(key)
            if isinstance(candidate, str) and candidate.startswith(("https://", "http://")):
                return candidate
    raise ManifestError("Postiz upload response did not contain a media URL")


@contextmanager
def _receipt_lock(receipt_path: Path) -> Iterator[None]:
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    lock_path = receipt_path.with_suffix(receipt_path.suffix + ".lock")
    with lock_path.open("a+", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


@contextmanager
def _handoff_lock(job_path: Path) -> Iterator[None]:
    """Coordinate Postiz handoff with the Node review route and Python decisions."""
    lock_path = job_path.parent / ".postiz-handoff-lock"
    try:
        lock_path.mkdir()
    except FileExistsError as exc:
        raise ManifestError(
            "a Postiz handoff is already active or needs manual reconciliation"
        ) from exc
    try:
        if Path(f"{job_path}.decision-lock").exists():
            raise ManifestError("a review decision is currently being saved")
        yield
    finally:
        try:
            lock_path.rmdir()
        except FileNotFoundError:
            pass


def _assert_same_handoff(expected: PreparedHandoff, current: PreparedHandoff) -> None:
    fields = (
        "job_id",
        "clip_id",
        "version",
        "platform",
        "render_path",
        "sha256",
        "caption_sha256",
        "title",
    )
    if any(getattr(expected, field) != getattr(current, field) for field in fields):
        raise ManifestError("approved handoff changed after preflight")


def _freeze_approved_media(handoff: PreparedHandoff) -> Path:
    """Copy the approved bytes once, then upload only the verified frozen copy."""
    staging = handoff.receipt_path.parent / ".staging"
    staging.mkdir(parents=True, exist_ok=True)
    descriptor, name = tempfile.mkstemp(
        prefix=f"{handoff.clip_id}-v{handoff.version}-",
        suffix=".mp4",
        dir=staging,
    )
    frozen = Path(name)
    try:
        with handoff.render_path.open("rb") as source, os.fdopen(descriptor, "wb") as target:
            shutil.copyfileobj(source, target, length=8 * 1024 * 1024)
            target.flush()
            os.fsync(target.fileno())
        if sha256_file(frozen).lower() != handoff.sha256:
            raise ManifestError("render changed while freezing approved Postiz media")
        return frozen
    except Exception:
        frozen.unlink(missing_ok=True)
        raise


def _platform_settings(handoff: PreparedHandoff) -> dict[str, Any]:
    identifier = PLATFORM_IDENTIFIERS[handoff.platform]
    if identifier == "instagram":
        return {"post_type": "post"}
    if identifier == "facebook":
        return {"post_type": "post"}
    if identifier == "youtube":
        return {"title": handoff.title, "type": "private"}
    if identifier == "tiktok":
        return {
            "privacy_level": "SELF_ONLY",
            "duet": False,
            "stitch": False,
            "comment": True,
            "autoAddMusic": "no",
            "brand_content_toggle": False,
            "brand_organic_toggle": False,
            "content_posting_method": "UPLOAD",
        }
    raise ManifestError(f"no validated Postiz settings for {handoff.platform}")


def _record_draft_locked(
    handoff: PreparedHandoff,
    receipt: dict[str, Any],
) -> None:
    job = read_json(handoff.job_path)
    clip = _clip(job, handoff.clip_id)
    current = str(clip.get("status"))
    if current not in {APPROVED, READY_TO_PUBLISH}:
        raise ManifestError("approval was revoked before the draft receipt was recorded")
    if int(clip.get("version", 0)) != handoff.version:
        raise ManifestError("render version changed before the draft receipt was recorded")
    if _approved_hash(clip) != handoff.sha256:
        raise ManifestError("approval checksum changed before the draft receipt was recorded")
    changed = False
    if current == APPROVED:
        clip["status"] = transition(current, READY_TO_PUBLISH)
        changed = True
    receipts = clip.setdefault("postiz_receipts", [])
    summary = {
        "platform": handoff.platform,
        "version": handoff.version,
        "approved_sha256": handoff.sha256,
        "status": "draft_created",
        "receipt_path": str(handoff.receipt_path),
        "created_at": receipt["created_at"],
    }
    if isinstance(receipts, list) and not any(
        isinstance(item, dict)
        and item.get("platform") == handoff.platform
        and item.get("version") == handoff.version
        and item.get("approved_sha256") == handoff.sha256
        for item in receipts
    ):
        receipts.append(summary)
        changed = True
    job["status"] = aggregate_job_state(job.get("clips", []))
    history = job.setdefault("history", [])
    if isinstance(history, list) and not any(
        isinstance(item, dict)
        and item.get("event") == "postiz_draft_created"
        and item.get("receipt_path") == str(handoff.receipt_path)
        for item in history
    ):
        history.append(
            {
                "at": receipt["created_at"],
                "event": "postiz_draft_created",
                **summary,
            }
        )
        changed = True
    if not changed:
        return
    job["revision"] = int(job["revision"]) + 1
    job["updated_at"] = utc_now()
    atomic_write_json(handoff.job_path, job)


def create_postiz_draft(
    handoff: PreparedHandoff,
    *,
    profile: str | None = None,
    runner: Runner = _run,
    cli: str = "postiz",
) -> dict[str, Any]:
    """Create one idempotent Postiz draft for one platform."""
    with _receipt_lock(handoff.receipt_path):
        if handoff.receipt_path.exists():
            existing = read_json(handoff.receipt_path)
            if existing.get("status") in {
                "draft_created",
                "draft_created_reconciliation_required",
            }:
                with _handoff_lock(handoff.job_path), manifest_lock(handoff.job_path):
                    current = prepare_handoff(
                        root=handoff.job_path.parents[2],
                        job_ref=handoff.job_path,
                        clip_id=handoff.clip_id,
                        platform=handoff.platform,
                        confirmed_sha256=handoff.sha256,
                    )
                    _assert_same_handoff(handoff, current)
                    existing_integration = existing.get("integration")
                    stored_profile = (
                        str(existing.get("requested_profile"))
                        if existing.get("requested_profile") is not None
                        else None
                    )
                    integration_profile = (
                        str(existing_integration.get("profile", ""))
                        if isinstance(existing_integration, dict)
                        else ""
                    )
                    profile_matches = (
                        profile is None
                        or profile.casefold()
                        in {
                            (stored_profile or "").casefold(),
                            integration_profile.casefold(),
                        }
                    )
                    if (
                        not isinstance(existing_integration, dict)
                        or not profile_matches
                        or existing.get("approved_sha256") != handoff.sha256
                        or existing.get("approved_caption_sha256")
                        != handoff.caption_sha256
                        or existing.get("settings") != _platform_settings(handoff)
                    ):
                        raise ManifestError(
                            "existing Postiz receipt targets different approved copy/settings/profile"
                        )
                    repaired = {
                        **existing,
                        "status": "draft_created",
                        "remote_state": "confirmed",
                        "reconciled_at": utc_now(),
                    }
                    atomic_write_json(handoff.receipt_path, repaired)
                    _record_draft_locked(handoff, repaired)
                    return repaired
            raise ManifestError(
                f"a non-reusable Postiz receipt already exists: {handoff.receipt_path}"
            )
        with _handoff_lock(handoff.job_path), manifest_lock(handoff.job_path):
            current = prepare_handoff(
                root=handoff.job_path.parents[2],
                job_ref=handoff.job_path,
                clip_id=handoff.clip_id,
                platform=handoff.platform,
                confirmed_sha256=handoff.sha256,
            )
            _assert_same_handoff(handoff, current)
            integrations = list_integrations(runner=runner, cli=cli)
            integration = select_integration(
                integrations, platform=handoff.platform, profile=profile
            )
            settings = _platform_settings(handoff)
            frozen = _freeze_approved_media(handoff)
            intent = {
                "schema_version": "shorts-postiz-receipt/v1",
                "status": "creating",
                "remote_state": "unknown",
                "created_at": utc_now(),
                "job_id": handoff.job_id,
                "clip_id": handoff.clip_id,
                "version": handoff.version,
                "platform": handoff.platform,
                "approved_sha256": handoff.sha256,
                "approved_caption_sha256": handoff.caption_sha256,
                "settings": settings,
                "requested_profile": profile,
                "message": "Do not retry blindly if this process is interrupted.",
            }
            atomic_write_json(handoff.receipt_path, intent)
            confirmed_receipt: dict[str, Any] | None = None
            try:
                upload_payload = _extract_json(runner([cli, "upload", str(frozen)]))
                media_url = _media_url(upload_payload)
                # Revalidate state and source after upload, before the draft mutation.
                revalidated = prepare_handoff(
                    root=handoff.job_path.parents[2],
                    job_ref=handoff.job_path,
                    clip_id=handoff.clip_id,
                    platform=handoff.platform,
                    confirmed_sha256=handoff.sha256,
                )
                _assert_same_handoff(handoff, revalidated)
                date = datetime.now(timezone.utc).isoformat()
                post_output = runner(
                    [
                        cli,
                        "posts:create",
                        "--content",
                        handoff.caption,
                        "--media",
                        media_url,
                        "--integrations",
                        str(integration["id"]),
                        "--date",
                        date,
                        "--type",
                        "draft",
                        "--settings",
                        json.dumps(settings, separators=(",", ":")),
                    ]
                )
                post_payload = _extract_json(post_output)
                receipt = {
                    **intent,
                    "status": "draft_created",
                    "remote_state": "confirmed",
                    "created_at": utc_now(),
                    "integration": {
                        "id": integration["id"],
                        "identifier": integration.get("identifier"),
                        "profile": integration.get("profile"),
                    },
                    "media_url": media_url,
                    "postiz_response": post_payload,
                }
                confirmed_receipt = receipt
                atomic_write_json(handoff.receipt_path, receipt)
                _record_draft_locked(handoff, receipt)
                return receipt
            except Exception as exc:
                evidence = {
                    **(confirmed_receipt or intent),
                    "status": (
                        "draft_created_reconciliation_required"
                        if confirmed_receipt
                        else "ambiguous"
                    ),
                    "remote_state": (
                        "confirmed_manifest_reconciliation_required"
                        if confirmed_receipt
                        else "manual_reconciliation_required"
                    ),
                    "failed_at": utc_now(),
                    "error_type": type(exc).__name__,
                    "error": str(exc)[:1000],
                }
                atomic_write_json(handoff.receipt_path, evidence)
                raise
            finally:
                frozen.unlink(missing_ok=True)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Verify an approved short and optionally create an idempotent Postiz draft."
    )
    parser.add_argument("job", help="Job id, job directory, or job.json path")
    parser.add_argument("clip_id")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--platform", required=True, choices=sorted(PLATFORM_IDENTIFIERS))
    parser.add_argument("--approved-sha256", required=True)
    parser.add_argument("--profile", help="Exact Postiz profile or integration name")
    parser.add_argument(
        "--create-draft",
        action="store_true",
        help="Perform upload and create a Postiz draft. Never schedules or publishes.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    handoff = prepare_handoff(
        root=args.root,
        job_ref=args.job,
        clip_id=args.clip_id,
        platform=args.platform,
        confirmed_sha256=args.approved_sha256,
    )
    if not args.create_draft:
        print(
            json.dumps(
                {
                    "ok": True,
                    "mode": "preflight_only",
                    "job_id": handoff.job_id,
                    "clip_id": handoff.clip_id,
                    "version": handoff.version,
                    "platform": handoff.platform,
                    "approved_sha256": handoff.sha256,
                    "message": "No upload, Postiz draft, schedule, or publication occurred.",
                },
                indent=2,
            )
        )
        return 0
    receipt = create_postiz_draft(handoff, profile=args.profile)
    print(json.dumps(receipt, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
