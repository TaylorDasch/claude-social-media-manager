from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from shorts_factory.boundaries import build_sentence_units
from shorts_factory.candidates import generate_overlapping_candidates
from shorts_factory.errors import InvalidTransition, ManifestError, ModelOutputError, RevisionConflict
from shorts_factory.policy import deduplicate_ranked
from shorts_factory.ranking import (
    StrictJsonCaller,
    rank_two_pass,
    ranking_input_context,
    validate_pass1,
)
from shorts_factory.state import (
    AWAITING_REVIEW,
    PUBLISHED,
    apply_clip_decision,
    transition,
)
from shorts_factory.storage import atomic_write_json, resolve_job_path, update_job


def transcript_words(spec: list[tuple[float, float, str]]) -> dict:
    return {
        "words": [
            {
                "id": f"w{index:07d}",
                "segment_id": "s00001",
                "start": start,
                "end": end,
                "text": text,
            }
            for index, (start, end, text) in enumerate(spec, start=1)
        ]
    }


class BoundaryTests(unittest.TestCase):
    def test_punctuation_pause_and_overlapping_windows(self) -> None:
        transcript = transcript_words(
            [
                (0.0, 1.0, "Temple"),
                (1.0, 2.0, "costs."),
                (2.2, 3.2, "Here"),
                (3.2, 4.2, "is"),
                (4.2, 5.2, "why."),
                (6.4, 7.4, "Belton"),
                (7.4, 8.4, "differs"),
                (8.4, 9.4, "today."),
                (9.6, 10.6, "Run"),
                (10.6, 11.6, "your"),
                (11.6, 12.6, "numbers."),
                (12.8, 13.8, "Then"),
                (13.8, 14.8, "choose"),
                (14.8, 15.8, "carefully."),
            ]
        )
        units = build_sentence_units(transcript, pause_seconds=0.7)
        self.assertEqual([unit["boundary_reason"] for unit in units], [
            "punctuation",
            "punctuation",
            "punctuation",
            "punctuation",
            "punctuation",
        ])
        self.assertGreaterEqual(units[2]["gap_before_s"], 1.0)

        candidates = generate_overlapping_candidates(
            units,
            min_seconds=5,
            max_seconds=15,
            targets=(("short", 7.0), ("long", 12.0)),
        )
        self.assertGreaterEqual(len(candidates), 4)
        starts = {candidate["start"] for candidate in candidates}
        self.assertGreater(len(starts), 1, "windows must start at overlapping sentence boundaries")
        self.assertTrue(
            any(
                left["start"] < right["start"] < left["end"]
                for left in candidates
                for right in candidates
            ),
            "candidate alternatives should overlap instead of fixed non-overlapping chunks",
        )


def ranked_item(candidate_id: str, start: float, end: float, text: str, score: int) -> dict:
    return {
        "candidate": {
            "id": candidate_id,
            "start": start,
            "end": end,
            "duration_s": end - start,
            "text": text,
        },
        "evaluation": {
            "hook": "Exact local comparison",
            "summary": "A complete comparison.",
            "lane": "relocator",
            "scores": {
                "hook_strength": 24,
                "angle_quality": 24,
                "audience_fit": 12,
                "arc_payoff": 12,
                "cta_strength": 8,
            },
            "total_score": 80,
            "standalone": True,
            "claim_flags": [],
            "warnings": [],
            "reasons": ["Complete thought."],
        },
        "rerank": {
            "candidate_id": candidate_id,
            "final_score": score,
            "keep": True,
            "selection_reason": "Strong and complete.",
            "distinct_angle": candidate_id,
        },
    }


class DedupeTests(unittest.TestCase):
    def test_higher_scoring_overlap_wins_and_distinct_moment_remains(self) -> None:
        ranked = [
            ranked_item("cand-a", 0, 30, "Temple buyers should compare the monthly payment first.", 92),
            ranked_item("cand-b", 2, 31, "Temple buyers should compare the monthly payment first.", 88),
            ranked_item("cand-c", 80, 110, "Belton has a different commute tradeoff for families.", 84),
        ]
        selected, rejected = deduplicate_ranked(
            ranked,
            source_kind="other",
            minimum_score=60,
            top_n=5,
        )
        self.assertEqual([item["candidate"]["id"] for item in selected], ["cand-a", "cand-c"])
        duplicate = next(item for item in rejected if item["candidate"]["id"] == "cand-b")
        self.assertEqual(duplicate["duplicate_of"], "cand-a")

    def test_standalone_flag_cannot_override_cutoff_warning(self) -> None:
        item = ranked_item(
            "cand-cutoff",
            0,
            45,
            "Temple has a tax difference, but here is the part that matters most.",
            95,
        )
        item["evaluation"]["warnings"] = [
            "The final line cuts off mid-thought, but enough context is present."
        ]
        selected, rejected = deduplicate_ranked(
            [item], source_kind="other", minimum_score=60, top_n=5
        )
        self.assertEqual(selected, [])
        self.assertIn("incomplete", rejected[0]["selection_reasons"][0].lower())

    def test_standalone_flag_cannot_override_partial_payoff_warning(self) -> None:
        item = ranked_item(
            "cand-tease",
            0,
            45,
            "The tax difference is real, but here is the part that matters most.",
            95,
        )
        item["evaluation"]["warnings"] = [
            "Ends on a tease rather than a complete answer, so payoff is partial."
        ]
        selected, rejected = deduplicate_ranked(
            [item], source_kind="other", minimum_score=60, top_n=5
        )
        self.assertEqual(selected, [])
        self.assertIn("incomplete", rejected[0]["selection_reasons"][0].lower())

    def test_equal_final_scores_prefer_the_more_complete_arc(self) -> None:
        setup = ranked_item(
            "cand-setup", 0, 45, "Temple and Belton look almost identical.", 70
        )
        payoff = ranked_item(
            "cand-payoff", 80, 125, "The ETJ changes the annual tax tradeoff.", 70
        )
        setup["evaluation"]["scores"]["arc_payoff"] = 10
        payoff["evaluation"]["scores"]["arc_payoff"] = 14
        selected, _ = deduplicate_ranked(
            [setup, payoff], source_kind="other", minimum_score=60, top_n=1
        )
        self.assertEqual(selected[0]["candidate"]["id"], "cand-payoff")


class StateTests(unittest.TestCase):
    def test_approval_checksum_locks_render_without_changing_version(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            job_dir = Path(directory)
            render = job_dir / "renders" / "clip.mp4"
            render.parent.mkdir()
            render.write_bytes(b"exact-render")
            digest = hashlib.sha256(render.read_bytes()).hexdigest()
            job = {
                "status": AWAITING_REVIEW,
                "clips": [
                    {
                        "id": "clip-01",
                        "version": 3,
                        "status": AWAITING_REVIEW,
                        "hook": "Temple or Belton?",
                        "summary": "Compare the real monthly tradeoffs before you choose.",
                        "claims": [],
                        "render": {
                            "path": "renders/clip.mp4",
                            "sha256": digest,
                            "qa": {"passed": True},
                        },
                    }
                ],
                "history": [],
            }
            clip = apply_clip_decision(
                job,
                clip_id="clip-01",
                decision="approved",
                actor="taylor",
                job_dir=job_dir,
            )
            self.assertEqual(clip["version"], 3)
            self.assertEqual(clip["decision"]["approved_version"], 3)
            self.assertEqual(clip["decision"]["approved_sha256"], digest)
            self.assertEqual(
                clip["decision"]["approved_caption"],
                "Compare the real monthly tradeoffs before you choose.",
            )
            self.assertEqual(len(clip["decision"]["approved_caption_sha256"]), 64)

    def test_unverified_claim_requires_explicit_taylor_waiver(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            job_dir = Path(directory)
            render = job_dir / "clip.mp4"
            render.write_bytes(b"render")
            digest = hashlib.sha256(render.read_bytes()).hexdigest()
            clip = {
                "id": "clip-claim",
                "version": 1,
                "status": AWAITING_REVIEW,
                "hook": "The number buyers miss",
                "summary": "Temple homes cost $300,000 in this example.",
                "claims": [
                    {
                        "text": "Temple homes cost $300,000.",
                        "type": "market_stat",
                        "severity": "verify",
                        "source_status": "unverified",
                    }
                ],
                "render": {
                    "path": str(render),
                    "sha256": digest,
                    "qa": {"passed": True},
                },
            }
            job = {"status": AWAITING_REVIEW, "clips": [clip], "history": []}
            with self.assertRaisesRegex(ManifestError, "explicit claim waiver"):
                apply_clip_decision(
                    job,
                    clip_id="clip-claim",
                    decision="approve",
                    actor="taylor",
                    job_dir=job_dir,
                )
            approved = apply_clip_decision(
                job,
                clip_id="clip-claim",
                decision="approve",
                actor="taylor",
                job_dir=job_dir,
                waive_unverified_claims=True,
            )
            self.assertEqual(
                approved["decision"]["claim_waiver"]["waived_by"], "taylor"
            )

    def test_invalid_transition_is_rejected(self) -> None:
        with self.assertRaises(InvalidTransition):
            transition(PUBLISHED, AWAITING_REVIEW)

    def test_optimistic_revision_conflict(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "job.json"
            atomic_write_json(path, {"revision": 2, "job_id": "job", "updated_at": "now"})
            with self.assertRaises(RevisionConflict):
                update_job(path, expected_revision=1, mutate=lambda job: job.update(status="declined"))

    def test_safe_job_id_cannot_follow_symlink_outside_factory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "factory"
            outside = base / "outside-job"
            outside.mkdir()
            (outside / "job.json").write_text('{"job_id":"escaped"}', encoding="utf-8")
            (root / "jobs").mkdir(parents=True)
            (root / "jobs" / "escaped").symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(ManifestError, "escapes the factory jobs root"):
                resolve_job_path(root, "escaped")


class FakeClient:
    def __init__(self, responses: list[str]) -> None:
        self.responses = iter(responses)

    def complete(self, **_: object) -> str:
        return next(self.responses)


class ModelValidationTests(unittest.TestCase):
    def test_ranking_cache_fingerprint_binds_transcript_and_models(self) -> None:
        base = {
            "id": "cand-a",
            "start": 1.0,
            "end": 31.0,
            "duration_s": 30.0,
            "start_word_id": "w1",
            "end_word_id": "w20",
            "strategy": "standard",
            "text": "Temple has one tax tradeoff.",
        }
        first = ranking_input_context(
            [base],
            primary_model="claude-a",
            openai_model="gpt-a",
            batch_size=8,
            rerank_limit=1,
        )
        changed_text = ranking_input_context(
            [{**base, "text": "Belton has a different tax tradeoff."}],
            primary_model="claude-a",
            openai_model="gpt-a",
            batch_size=8,
            rerank_limit=1,
        )
        changed_model = ranking_input_context(
            [base],
            primary_model="claude-b",
            openai_model="gpt-a",
            batch_size=8,
            rerank_limit=1,
        )
        self.assertNotEqual(first["fingerprint"], changed_text["fingerprint"])
        self.assertNotEqual(first["fingerprint"], changed_model["fingerprint"])

    def test_corrupt_model_output_fails_after_one_retry(self) -> None:
        caller = StrictJsonCaller(
            client=FakeClient(["```json\n{}\n```", json.dumps({"evaluations": []})]),
            retries=1,
        )
        with self.assertRaises(ModelOutputError):
            caller.call(
                system="test",
                user="test",
                validator=lambda value: validate_pass1(value, ["cand-a"]),
            )

    def test_pass2_uses_short_aliases_then_restores_canonical_ids(self) -> None:
        candidates = [
            {
                "id": "cand-121004d5c58e",
                "start": 0.0,
                "end": 30.0,
                "duration_s": 30.0,
                "strategy": "standard",
                "text": "Temple and Belton have different monthly-payment tradeoffs.",
            },
            {
                "id": "cand-b678824b4208",
                "start": 40.0,
                "end": 70.0,
                "duration_s": 30.0,
                "strategy": "standard",
                "text": "The right choice depends on how you actually use the city.",
            },
        ]
        checkpoints: list[dict] = []

        class AliasAwareCaller:
            def __init__(self) -> None:
                self.pass1_batch_sizes: list[int] = []

            def call(self, *, user: str, **_: object) -> dict:
                payload = user.split("Candidates:\n", 1)
                if len(payload) == 2:
                    supplied = json.loads(payload[1])
                    self.pass1_batch_sizes.append(len(supplied))
                    return {
                        "evaluations": [
                            {
                                "candidate_id": item["candidate_id"],
                                "hook": item["transcript"],
                                "summary": "Complete local comparison.",
                                "lane": "relocator",
                                "scores": {
                                    "hook_strength": 20,
                                    "angle_quality": 20,
                                    "audience_fit": 10,
                                    "arc_payoff": 10,
                                    "cta_strength": 0,
                                },
                                "total_score": 60,
                                "standalone": True,
                                "claim_flags": [],
                                "warnings": [],
                                "reasons": ["Complete thought."],
                            }
                            for item in supplied
                        ]
                    }
                supplied = json.loads(user.split("Finalists:\n", 1)[1])
                aliases = [item["candidate_id"] for item in supplied]
                self_outer.assertEqual(aliases, ["C01", "C02"])
                return {
                    "ranking": [
                        {
                            "candidate_id": alias,
                            "final_score": 80 - index,
                            "keep": True,
                            "selection_reason": "Distinct complete thought.",
                            "distinct_angle": alias,
                        }
                        for index, alias in enumerate(aliases)
                    ]
                }

        self_outer = self
        scripted = AliasAwareCaller()
        ranked, pass1, pass2 = rank_two_pass(
            candidates,
            caller=scripted,  # type: ignore[arg-type]
            batch_size=2,
            rerank_limit=2,
            pass1_checkpoint=checkpoints.append,
        )
        expected = {candidate["id"] for candidate in candidates}
        self.assertEqual({item["candidate_id"] for item in pass2["ranking"]}, expected)
        self.assertEqual({item["candidate"]["id"] for item in ranked}, expected)
        self.assertEqual(checkpoints[-1], pass1)
        self.assertEqual(scripted.pass1_batch_sizes, [2])

        resumed = AliasAwareCaller()
        resumed_ranked, resumed_pass1, _ = rank_two_pass(
            candidates,
            caller=resumed,  # type: ignore[arg-type]
            batch_size=2,
            rerank_limit=2,
            existing_pass1={"evaluations": [pass1["evaluations"][0]]},
        )
        self.assertEqual(resumed.pass1_batch_sizes, [1])
        self.assertEqual(
            {item["candidate"]["id"] for item in resumed_ranked}, expected
        )
        self.assertEqual(len(resumed_pass1["evaluations"]), 2)


if __name__ == "__main__":
    unittest.main()
