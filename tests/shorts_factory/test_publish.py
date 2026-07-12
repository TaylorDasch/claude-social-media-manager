from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from shorts_factory.errors import ManifestError
import shorts_factory.publish as publish_module
from shorts_factory.publish import create_postiz_draft, prepare_handoff


def make_job(tmp_path: Path) -> tuple[Path, str, str]:
    root = tmp_path / "factory"
    job_id = "temple-vs-belton-20260712"
    job_dir = root / "jobs" / job_id
    render_dir = job_dir / "renders"
    render_dir.mkdir(parents=True)
    render_path = render_dir / "clip-01-v1.mp4"
    render_path.write_bytes(b"deterministic-render")
    digest = hashlib.sha256(render_path.read_bytes()).hexdigest()
    approved_caption = "A standalone Central Texas city comparison."
    manifest = {
        "schema_version": "shorts-job/v1",
        "revision": 1,
        "job_id": job_id,
        "status": "approved",
        "clips": [
            {
                "id": "clip-01",
                "version": 1,
                "status": "approved",
                "hook": "Temple or Belton? Run the real numbers first.",
                "summary": "A standalone Central Texas city comparison.",
                "platform_eligibility": {
                    "instagram_reels": {"eligible": True},
                    "youtube_shorts": {"eligible": True},
                    "tiktok": {
                        "eligible": False,
                        "reason": "Long-form YouTube derivative",
                    },
                },
                "render": {
                    "path": "renders/clip-01-v1.mp4",
                    "sha256": digest,
                    "qa": {"passed": True},
                },
                "decision": {
                    "status": "approve",
                    "approved_sha256": digest,
                    "approved_version": 1,
                    "approved_caption": approved_caption,
                    "approved_caption_sha256": hashlib.sha256(
                        approved_caption.encode("utf-8")
                    ).hexdigest(),
                    "approved_title": "Temple or Belton? Run the real numbers first.",
                },
            }
        ],
    }
    (job_dir / "job.json").write_text(json.dumps(manifest), encoding="utf-8")
    return root, job_id, digest


def test_preflight_requires_exact_hash_and_platform_eligibility(tmp_path: Path) -> None:
    root, job_id, digest = make_job(tmp_path)
    handoff = prepare_handoff(
        root=root,
        job_ref=job_id,
        clip_id="clip-01",
        platform="instagram_reels",
        confirmed_sha256=digest,
    )
    assert handoff.sha256 == digest
    assert handoff.render_path.is_file()

    alias = prepare_handoff(
        root=root,
        job_ref=job_id,
        clip_id="clip-01",
        platform="instagram",
        confirmed_sha256=digest,
    )
    assert alias.platform == "instagram_reels"
    assert alias.receipt_path == handoff.receipt_path

    with pytest.raises(ManifestError, match="does not match"):
        prepare_handoff(
            root=root,
            job_ref=job_id,
            clip_id="clip-01",
            platform="instagram_reels",
            confirmed_sha256="0" * 64,
        )
    with pytest.raises(ManifestError, match="ineligible for tiktok"):
        prepare_handoff(
            root=root,
            job_ref=job_id,
            clip_id="clip-01",
            platform="tiktok",
            confirmed_sha256=digest,
        )


def test_postiz_draft_is_idempotent_and_never_schedules(tmp_path: Path) -> None:
    root, job_id, digest = make_job(tmp_path)
    handoff = prepare_handoff(
        root=root,
        job_ref=job_id,
        clip_id="clip-01",
        platform="instagram_reels",
        confirmed_sha256=digest,
    )
    commands: list[list[str]] = []

    def runner(command: list[str] | tuple[str, ...]) -> str:
        command = list(command)
        commands.append(command)
        if command[1] == "integrations:list":
            return "Connected integrations:\n" + json.dumps(
                [
                    {
                        "id": "integration-ig",
                        "identifier": "instagram",
                        "profile": "dealswithdasch",
                        "disabled": False,
                    }
                ]
            )
        if command[1] == "upload":
            return "Uploaded:\n" + json.dumps(
                {"path": "https://uploads.example.test/clip.mp4"}
            )
        if command[1] == "posts:create":
            return "Created:\n" + json.dumps({"id": "draft-1", "type": "draft"})
        raise AssertionError(command)

    first = create_postiz_draft(handoff, runner=runner)
    assert first["status"] == "draft_created"
    assert len(commands) == 3
    create_command = commands[-1]
    assert create_command[create_command.index("--type") + 1] == "draft"
    assert "schedule" not in create_command
    settings = json.loads(create_command[create_command.index("--settings") + 1])
    assert settings == {"post_type": "post"}
    upload_path = Path(commands[-2][-1])
    assert upload_path != handoff.render_path

    second = create_postiz_draft(handoff, runner=runner)
    assert second["postiz_response"] == first["postiz_response"]
    assert len(commands) == 3, "idempotent retry must remain fully local"
    assert sum(command[1] == "upload" for command in commands) == 1
    assert sum(command[1] == "posts:create" for command in commands) == 1

    job = json.loads((root / "jobs" / job_id / "job.json").read_text())
    assert job["revision"] == 2
    assert job["clips"][0]["status"] == "ready_to_publish"


def test_handoff_blocks_file_changed_after_approval(tmp_path: Path) -> None:
    root, job_id, digest = make_job(tmp_path)
    render = root / "jobs" / job_id / "renders" / "clip-01-v1.mp4"
    render.write_bytes(b"mutated-after-approval")
    with pytest.raises(ManifestError, match="changed after approval"):
        prepare_handoff(
            root=root,
            job_ref=job_id,
            clip_id="clip-01",
            platform="instagram_reels",
            confirmed_sha256=digest,
        )


def test_create_revalidates_approval_before_any_remote_call(tmp_path: Path) -> None:
    root, job_id, digest = make_job(tmp_path)
    handoff = prepare_handoff(
        root=root,
        job_ref=job_id,
        clip_id="clip-01",
        platform="instagram_reels",
        confirmed_sha256=digest,
    )
    manifest = root / "jobs" / job_id / "job.json"
    job = json.loads(manifest.read_text())
    job["clips"][0]["status"] = "needs_changes"
    manifest.write_text(json.dumps(job), encoding="utf-8")
    calls: list[list[str]] = []

    with pytest.raises(ManifestError, match="must be approved"):
        create_postiz_draft(
            handoff,
            runner=lambda command: calls.append(list(command)) or "{}",
        )
    assert calls == []


def test_ambiguous_post_response_blocks_blind_retry(tmp_path: Path) -> None:
    root, job_id, digest = make_job(tmp_path)
    handoff = prepare_handoff(
        root=root,
        job_ref=job_id,
        clip_id="clip-01",
        platform="instagram_reels",
        confirmed_sha256=digest,
    )
    draft_calls = 0

    def runner(command: list[str] | tuple[str, ...]) -> str:
        nonlocal draft_calls
        command = list(command)
        if command[1] == "integrations:list":
            return json.dumps(
                [{"id": "ig", "identifier": "instagram", "disabled": False}]
            )
        if command[1] == "upload":
            return json.dumps({"path": "https://uploads.example.test/clip.mp4"})
        if command[1] == "posts:create":
            draft_calls += 1
            return "remote success but truncated response"
        raise AssertionError(command)

    with pytest.raises(ManifestError, match="machine-readable"):
        create_postiz_draft(handoff, runner=runner)
    ambiguous = json.loads(handoff.receipt_path.read_text())
    assert ambiguous["status"] == "ambiguous"
    assert ambiguous["remote_state"] == "manual_reconciliation_required"
    with pytest.raises(ManifestError, match="non-reusable"):
        create_postiz_draft(handoff, runner=runner)
    assert draft_calls == 1


def test_unsafe_clip_id_never_becomes_a_receipt_path(tmp_path: Path) -> None:
    root, job_id, digest = make_job(tmp_path)
    with pytest.raises(ManifestError, match="unsafe path"):
        prepare_handoff(
            root=root,
            job_ref=job_id,
            clip_id="../../outside",
            platform="instagram_reels",
            confirmed_sha256=digest,
        )


def test_confirmed_remote_evidence_survives_manifest_reconciliation_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root, job_id, digest = make_job(tmp_path)
    handoff = prepare_handoff(
        root=root,
        job_ref=job_id,
        clip_id="clip-01",
        platform="instagram_reels",
        confirmed_sha256=digest,
    )

    def runner(command: list[str] | tuple[str, ...]) -> str:
        command = list(command)
        if command[1] == "integrations:list":
            return json.dumps(
                [
                    {
                        "id": "integration-ig",
                        "identifier": "instagram",
                        "profile": "dealswithdasch",
                        "disabled": False,
                    }
                ]
            )
        if command[1] == "upload":
            return json.dumps({"path": "https://uploads.example.test/clip.mp4"})
        if command[1] == "posts:create":
            return json.dumps({"id": "confirmed-draft", "type": "draft"})
        raise AssertionError(command)

    original = publish_module._record_draft_locked
    monkeypatch.setattr(
        publish_module,
        "_record_draft_locked",
        lambda *_: (_ for _ in ()).throw(ManifestError("simulated manifest failure")),
    )
    with pytest.raises(ManifestError, match="simulated manifest failure"):
        create_postiz_draft(handoff, runner=runner)
    receipt = json.loads(handoff.receipt_path.read_text())
    assert receipt["status"] == "draft_created_reconciliation_required"
    assert receipt["postiz_response"]["id"] == "confirmed-draft"
    assert receipt["media_url"].startswith("https://")

    monkeypatch.setattr(publish_module, "_record_draft_locked", original)
    repaired = create_postiz_draft(handoff, runner=runner)
    assert repaired["status"] == "draft_created"
    job = json.loads(handoff.job_path.read_text())
    assert job["clips"][0]["status"] == "ready_to_publish"


def test_existing_receipt_cannot_be_reused_for_a_different_profile(tmp_path: Path) -> None:
    root, job_id, digest = make_job(tmp_path)
    handoff = prepare_handoff(
        root=root,
        job_ref=job_id,
        clip_id="clip-01",
        platform="instagram_reels",
        confirmed_sha256=digest,
    )

    def runner(command: list[str] | tuple[str, ...]) -> str:
        command = list(command)
        if command[1] == "integrations:list":
            return json.dumps(
                [
                    {
                        "id": "ig-a",
                        "identifier": "instagram",
                        "profile": "profile-a",
                        "disabled": False,
                    },
                    {
                        "id": "ig-b",
                        "identifier": "instagram",
                        "profile": "profile-b",
                        "disabled": False,
                    },
                ]
            )
        if command[1] == "upload":
            return json.dumps({"path": "https://uploads.example.test/clip.mp4"})
        if command[1] == "posts:create":
            return json.dumps({"id": "draft-a"})
        raise AssertionError(command)

    create_postiz_draft(handoff, profile="profile-a", runner=runner)
    with pytest.raises(ManifestError, match="different approved copy/settings/profile"):
        create_postiz_draft(handoff, profile="profile-b", runner=runner)
