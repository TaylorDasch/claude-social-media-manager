"""Approval workflow states and guarded transitions."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from .errors import InvalidTransition, ManifestError
from .policy import find_banned_phrases, publication_copy, unresolved_claims
from .storage import sha256_file, utc_now


PROCESSING = "processing"
AWAITING_REVIEW = "awaiting_review"
NEEDS_CHANGES = "needs_changes"
APPROVED = "approved"
DECLINED = "declined"
READY_TO_PUBLISH = "ready_to_publish"
SCHEDULED = "scheduled"
PUBLISHED = "published"
FAILED = "failed"

ALL_STATES = frozenset(
    {
        PROCESSING,
        AWAITING_REVIEW,
        NEEDS_CHANGES,
        APPROVED,
        DECLINED,
        READY_TO_PUBLISH,
        SCHEDULED,
        PUBLISHED,
        FAILED,
    }
)

ALLOWED_TRANSITIONS: dict[str, frozenset[str]] = {
    PROCESSING: frozenset({AWAITING_REVIEW, NEEDS_CHANGES, FAILED}),
    AWAITING_REVIEW: frozenset({NEEDS_CHANGES, APPROVED, DECLINED, FAILED}),
    NEEDS_CHANGES: frozenset(
        {PROCESSING, AWAITING_REVIEW, APPROVED, DECLINED, FAILED}
    ),
    APPROVED: frozenset({NEEDS_CHANGES, DECLINED, READY_TO_PUBLISH, FAILED}),
    DECLINED: frozenset({AWAITING_REVIEW}),
    READY_TO_PUBLISH: frozenset({NEEDS_CHANGES, SCHEDULED, FAILED}),
    SCHEDULED: frozenset({PUBLISHED, FAILED}),
    PUBLISHED: frozenset(),
    FAILED: frozenset({PROCESSING, NEEDS_CHANGES}),
}

DECISION_STATES = {
    "approve": APPROVED,
    "approved": APPROVED,
    "needs_changes": NEEDS_CHANGES,
    "needs-changes": NEEDS_CHANGES,
    "decline": DECLINED,
    "declined": DECLINED,
}

_CANONICAL_DECISIONS = {
    APPROVED: "approve",
    NEEDS_CHANGES: "needs_changes",
    DECLINED: "decline",
}


def ensure_state(state: str) -> str:
    if state not in ALL_STATES:
        raise ManifestError(f"unknown shorts workflow state: {state!r}")
    return state


def transition(current: str, target: str) -> str:
    ensure_state(current)
    ensure_state(target)
    if target == current:
        return current
    if target not in ALLOWED_TRANSITIONS[current]:
        raise InvalidTransition(f"invalid transition: {current} -> {target}")
    return target


def aggregate_job_state(clips: list[dict[str, Any]]) -> str:
    """Derive review state without silently promoting a job to publish-ready."""
    if not clips:
        return NEEDS_CHANGES
    states = {ensure_state(str(clip.get("status"))) for clip in clips}
    if PROCESSING in states:
        return PROCESSING
    if AWAITING_REVIEW in states:
        return AWAITING_REVIEW
    if NEEDS_CHANGES in states:
        return NEEDS_CHANGES
    if APPROVED in states:
        return APPROVED
    if states == {DECLINED}:
        return DECLINED
    if FAILED in states:
        return FAILED
    if PUBLISHED in states:
        return PUBLISHED
    if SCHEDULED in states:
        return SCHEDULED
    if READY_TO_PUBLISH in states:
        return READY_TO_PUBLISH
    raise ManifestError(f"cannot aggregate clip states: {sorted(states)}")


def apply_clip_decision(
    job: dict[str, Any],
    *,
    clip_id: str,
    decision: str,
    actor: str,
    job_dir: Path | None = None,
    reason: str | None = None,
    requested_changes: str | None = None,
    waive_unverified_claims: bool = False,
) -> dict[str, Any]:
    if decision not in DECISION_STATES:
        raise ManifestError(f"unsupported decision: {decision!r}")
    target = DECISION_STATES.get(decision)
    if target is None:
        raise ManifestError(f"unsupported decision: {decision!r}")
    canonical_decision = _CANONICAL_DECISIONS[target]
    if canonical_decision == "needs_changes" and not (requested_changes or reason):
        raise ManifestError("needs_changes requires --requested-changes or --reason")

    clips = job.get("clips")
    if not isinstance(clips, list):
        raise ManifestError("job clips must be a list")
    match = next((clip for clip in clips if clip.get("id") == clip_id), None)
    if match is None:
        raise ManifestError(f"clip not found in job: {clip_id}")

    current = ensure_state(str(match.get("status")))
    transition(current, target)
    approved_sha256: str | None = None
    approved_version: int | None = None
    approved_caption: str | None = None
    approved_caption_sha256: str | None = None
    approved_title: str | None = None
    claim_waiver: dict[str, Any] | None = None
    if target == APPROVED:
        render = match.get("render")
        if not isinstance(render, dict) or not render.get("path"):
            raise ManifestError(
                "cannot approve an unrendered clip; render.path is required"
            )
        qa = render.get("qa")
        if not isinstance(qa, dict) or qa.get("passed") is not True:
            raise ManifestError("cannot approve a clip until render QA has passed")
        render_path = Path(str(render["path"])).expanduser()
        if not render_path.is_absolute():
            if job_dir is None:
                raise ManifestError(
                    "relative render.path requires the canonical job directory"
                )
            render_path = job_dir / render_path
        render_path = render_path.resolve()
        if job_dir is not None:
            try:
                render_path.relative_to(job_dir.resolve())
            except ValueError as exc:
                raise ManifestError(
                    f"rendered clip is outside the canonical job directory: {render_path}"
                ) from exc
        if not render_path.is_file():
            raise ManifestError(f"rendered clip does not exist: {render_path}")
        actual_sha256 = sha256_file(render_path)
        recorded_sha256 = render.get("sha256")
        if recorded_sha256 and recorded_sha256 != actual_sha256:
            raise ManifestError(
                f"render checksum mismatch for {clip_id}: manifest has "
                f"{recorded_sha256}, file is {actual_sha256}"
            )
        render["sha256"] = actual_sha256
        approved_sha256 = actual_sha256
        approved_version = int(match.get("version", 1))
        unresolved = unresolved_claims(match)
        if unresolved and not waive_unverified_claims:
            raise ManifestError(
                f"cannot approve {len(unresolved)} unverified verify/high-risk claim(s) "
                "without Taylor's explicit claim waiver"
            )
        try:
            approved_caption, approved_title = publication_copy(match)
        except ValueError as exc:
            raise ManifestError(str(exc)) from exc
        banned = find_banned_phrases(f"{approved_caption}\n{approved_title}")
        if banned:
            raise ManifestError(
                "publication copy contains governance-banned language: "
                + ", ".join(banned)
            )
        approved_caption_sha256 = hashlib.sha256(
            approved_caption.encode("utf-8")
        ).hexdigest()
        if unresolved:
            claim_waiver = {
                "waived_by": actor,
                "waived_at": utc_now(),
                "reason": "Taylor explicitly confirmed the spoken claims for publication.",
                "claims": [
                    {
                        "text": claim.get("text"),
                        "type": claim.get("type"),
                        "severity": claim.get("severity"),
                    }
                    for claim in unresolved
                ],
            }
    timestamp = utc_now()
    match["status"] = target
    match["decision"] = {
        "status": canonical_decision,
        "decided_at": timestamp,
        "decided_by": actor,
        "reason": reason,
        "requested_changes": requested_changes,
        "approved_sha256": approved_sha256,
        "approved_version": approved_version,
        "approved_caption": approved_caption,
        "approved_caption_sha256": approved_caption_sha256,
        "approved_title": approved_title,
        "claim_waiver": claim_waiver,
    }
    job["status"] = aggregate_job_state(clips)
    history = job.setdefault("history", [])
    history.append(
        {
            "at": timestamp,
            "event": "clip_decision",
            "clip_id": clip_id,
            "from": current,
            "to": target,
            "actor": actor,
            "reason": reason,
            "requested_changes": requested_changes,
            "approved_sha256": approved_sha256,
            "approved_version": approved_version,
            "approved_caption_sha256": approved_caption_sha256,
            "claim_waiver": claim_waiver,
        }
    )
    return match
