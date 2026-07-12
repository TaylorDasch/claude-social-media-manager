from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from shorts_factory.errors import ManifestError
from shorts_factory.pipeline import _clip_manifest, _verify_source_integrity


def ranked(candidate_id: str = "cand-w0000100-w0000200") -> dict:
    return {
        "candidate": {
            "id": candidate_id,
            "start": 10.0,
            "end": 40.0,
            "duration_s": 30.0,
            "start_word_id": "w0000100",
            "end_word_id": "w0000200",
            "strategy": "hook_to_payoff",
            "text": "Temple or Belton depends on your actual commute and budget.",
        },
        "evaluation": {
            "scores": {},
            "hook": "Temple or Belton?",
            "summary": "A complete comparison.",
            "lane": "relocator",
            "topic_axes": ["work commute"],
            "topic_purity": 96,
            "promise": "Which city fits the commute?",
            "payoff": "The clip gives the commute tradeoff.",
            "payoff_complete": True,
            "reasons": [],
        },
        "rerank": {
            "final_score": 91,
            "distinct_angle": "commute tradeoff",
            "selection_reason": "standalone",
        },
        "warnings": [],
        "claims": [],
        "platform_eligibility": {},
    }


def test_reanalysis_increments_render_version_and_preserves_prior_evidence() -> None:
    prior = {
        "id": "clip-w0000100-w0000200",
        "candidate_id": "cand-w0000100-w0000200",
        "version": 1,
        "status": "approved",
        "render": {"path": "renders/clip-v1.mp4", "sha256": "a" * 64},
        "decision": {"approved_sha256": "a" * 64},
        "postiz_receipts": [{"status": "draft_created"}],
    }
    revised = _clip_manifest(ranked(), rank=1, previous_clips=[prior])
    assert revised["id"] == prior["id"]
    assert revised["version"] == 2
    assert revised["versions"][0]["version"] == 1
    assert revised["versions"][0]["decision"]["approved_sha256"] == "a" * 64
    assert revised["versions"][0]["postiz_receipts"][0]["status"] == "draft_created"


def test_new_candidate_starts_at_version_one_with_stable_id() -> None:
    clip = _clip_manifest(ranked("cand-w0000300-w0000400"), rank=4)
    assert clip["id"] == "clip-w0000300-w0000400"
    assert clip["version"] == 1
    assert clip["versions"] == []


def test_source_integrity_blocks_replaced_master(tmp_path: Path) -> None:
    source = tmp_path / "master.mp4"
    source.write_bytes(b"ingested-source")
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    job = {"source": {"path": str(source), "sha256": digest}}
    assert _verify_source_integrity(job, phase="test") == source
    source.write_bytes(b"re-exported-source")
    with pytest.raises(ManifestError, match="changed after ingest"):
        _verify_source_integrity(job, phase="test")
