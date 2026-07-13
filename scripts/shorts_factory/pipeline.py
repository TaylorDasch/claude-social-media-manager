"""Production orchestration through the approval-manifest boundary."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .boundaries import build_sentence_units
from .candidates import generate_overlapping_candidates, preselect_diverse_candidates
from .errors import InvalidTransition, ManifestError, ModelOutputError, RevisionConflict
from .graphics import load_visual_replacements, replacements_for_clip
from .policy import deduplicate_ranked
from .qa import verify_render
from .ranking import (
    DEFAULT_CLAUDE_MODEL,
    DEFAULT_OPENAI_MODEL,
    AutoModelClient,
    is_single_subject_evaluation,
    ModelClient,
    StrictJsonCaller,
    rank_two_pass,
    ranking_input_context,
    validate_pass1,
    validate_pass2,
)
from .render import RenderValidationError, render_clip, render_input_fingerprint
from .state import (
    AWAITING_REVIEW,
    FAILED,
    NEEDS_CHANGES,
    PROCESSING,
    apply_clip_decision,
    transition,
)
from .storage import (
    JOB_SCHEMA_VERSION,
    atomic_write_json,
    read_json,
    resolve_job_path,
    sha256_file,
    update_job,
    utc_now,
    write_clip_manifests,
)
from .transcribe import transcribe_or_reuse
from .vision import validate_visual_analysis


def _validate_job(job: dict[str, Any], path: Path) -> None:
    if job.get("schema_version") != JOB_SCHEMA_VERSION:
        raise ManifestError(
            f"unsupported job schema at {path}: {job.get('schema_version')!r}"
        )
    if not isinstance(job.get("revision"), int):
        raise ManifestError(f"job revision is invalid at {path}")
    if not isinstance(job.get("source"), dict) or not isinstance(job.get("audio"), dict):
        raise ManifestError(f"job source/audio metadata is incomplete at {path}")


def _verify_source_integrity(job: dict[str, Any], *, phase: str) -> Path:
    source = job.get("source")
    if not isinstance(source, dict):
        raise ManifestError("job source metadata is missing")
    raw_path = source.get("reference_path") or source.get("path")
    expected = source.get("sha256")
    if not isinstance(raw_path, str) or not isinstance(expected, str):
        raise ManifestError("job source path/checksum is incomplete")
    path = Path(raw_path).expanduser().resolve()
    if not path.is_file():
        raise ManifestError(f"source master is missing during {phase}: {path}")
    actual = sha256_file(path)
    if actual != expected:
        raise ManifestError(
            f"source master changed after ingest during {phase}; "
            "create a new versioned job before continuing"
        )
    return path


def _mark_analysis_started(job: dict[str, Any]) -> None:
    current = str(job.get("status"))
    transition(current, PROCESSING)
    job["status"] = PROCESSING
    job["error"] = None
    job.setdefault("history", []).append(
        {"at": utc_now(), "event": "analysis_started", "from": current, "to": PROCESSING}
    )


def _mark_failed(job_path: Path, error: Exception) -> None:
    def mutate(job: dict[str, Any]) -> None:
        current = str(job.get("status"))
        if current != PROCESSING:
            raise RevisionConflict(
                f"refusing to overwrite concurrent state {current!r} with failed"
            )
        try:
            transition(current, FAILED)
        except InvalidTransition:
            # Preserve evidence even if a separate actor moved state while work ran.
            pass
        job["status"] = FAILED
        job["error"] = {"type": type(error).__name__, "message": str(error)[:2000]}
        job.setdefault("history", []).append(
            {
                "at": utc_now(),
                "event": "analysis_failed",
                "from": current,
                "to": FAILED,
                "error": str(error)[:1000],
            }
        )

    try:
        update_job(job_path, expected_revision=None, mutate=mutate)
    except Exception:
        # The original exception is more actionable than a secondary logging error.
        return


def _archived_version(clip: dict[str, Any]) -> dict[str, Any]:
    """Preserve immutable evidence before producing a replacement version."""
    return {
        key: value
        for key, value in clip.items()
        if key not in {"versions"}
    }


def _clip_manifest(
    item: dict[str, Any],
    *,
    rank: int,
    previous_clips: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    candidate = item["candidate"]
    evaluation = item["evaluation"]
    rerank = item["rerank"]
    prior = next(
        (
            clip
            for clip in (previous_clips or [])
            if clip.get("candidate_id") == candidate["id"]
        ),
        None,
    )
    clip_id = (
        str(prior["id"])
        if prior
        else f"clip-{str(candidate['id']).removeprefix('cand-')}"
    )
    prior_versions = list(prior.get("versions", [])) if prior else []
    if prior:
        snapshot = _archived_version(prior)
        identity = (snapshot.get("id"), snapshot.get("version"))
        if not any(
            (version.get("id"), version.get("version")) == identity
            for version in prior_versions
            if isinstance(version, dict)
        ):
            prior_versions.append(snapshot)
    version = max(
        [
            int(value.get("version", 0))
            for value in [*(prior_versions or []), *([prior] if prior else [])]
            if isinstance(value, dict)
        ]
        or [0]
    ) + 1
    return {
        "id": clip_id,
        "candidate_id": candidate["id"],
        "version": version,
        "versions": prior_versions,
        "rank": rank,
        "score": rerank["final_score"],
        "score_breakdown": evaluation["scores"],
        "status": PROCESSING,
        "start": candidate["start"],
        "end": candidate["end"],
        "duration_s": candidate["duration_s"],
        "start_word_id": candidate["start_word_id"],
        "end_word_id": candidate["end_word_id"],
        "strategy": candidate["strategy"],
        "hook": evaluation["hook"],
        "summary": evaluation["summary"],
        "transcript": candidate["text"],
        "lane": evaluation["lane"],
        "topic_axes": evaluation["topic_axes"],
        "topic_purity": evaluation["topic_purity"],
        "promise": evaluation["promise"],
        "payoff": evaluation["payoff"],
        "payoff_complete": evaluation["payoff_complete"],
        "distinct_angle": rerank["distinct_angle"],
        "reasons": evaluation["reasons"] + [rerank["selection_reason"]],
        "warnings": item["warnings"],
        "claims": item["claims"],
        "platform_eligibility": item["platform_eligibility"],
        "render": {
            "path": None,
            "sha256": None,
            "qa": {
                "status": "not_rendered",
                "checks": [],
                "verified_at": None,
            },
        },
        "decision": {
            "status": "pending",
            "decided_at": None,
            "decided_by": None,
            "reason": None,
            "requested_changes": None,
            "approved_sha256": None,
            "approved_version": None,
        },
    }


def _render_review_clip(
    clip: dict[str, Any],
    *,
    source_path: Path,
    source_sha256: str,
    transcript_words: list[dict[str, Any]],
    job_dir: Path,
    render_mode: str,
    visual_replacements: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Render one selected span; fail closed before review eligibility."""
    output_path = (
        job_dir
        / "renders"
        / f"{clip['id']}-v{int(clip['version'])}.mp4"
    )
    existing_manifest_path = output_path.with_suffix(".render.json")
    render_metadata: dict[str, Any] = {"source_sha256": source_sha256}
    if visual_replacements:
        render_metadata["visual_replacements"] = visual_replacements
    # A caption-only revision does not need to rescan the 6 GB source for the
    # same shot/crop plan. Reuse only a validated, contained prior sidecar for
    # the exact same source span; render bytes and captions are still rebuilt
    # and fully QA'd under a new fingerprint/version.
    for prior in reversed(clip.get("versions", [])):
        if not isinstance(prior, dict):
            continue
        try:
            same_span = (
                abs(float(prior.get("start", -1)) - float(clip["start"])) <= 0.001
                and abs(float(prior.get("end", -1)) - float(clip["end"])) <= 0.001
            )
        except (TypeError, ValueError):
            continue
        if not same_span:
            continue
        prior_render = prior.get("render")
        if not isinstance(prior_render, dict):
            continue
        sidecars = prior_render.get("sidecars")
        crop_raw = sidecars.get("crop_track") if isinstance(sidecars, dict) else None
        if not isinstance(crop_raw, str):
            continue
        try:
            crop_path = Path(crop_raw).expanduser().resolve(strict=True)
            crop_path.relative_to(job_dir.resolve(strict=True))
            prior_analysis = read_json(crop_path)
            if not validate_visual_analysis(prior_analysis):
                render_metadata["visual_analysis"] = prior_analysis
                break
        except (FileNotFoundError, ManifestError, TypeError, ValueError):
            continue
    expected_fingerprint = render_input_fingerprint(
        source_path,
        float(clip["start"]),
        float(clip["end"]),
        transcript_words,
        render_mode,
        render_metadata,
    )
    if existing_manifest_path.is_file():
        try:
            existing = read_json(existing_manifest_path)
            span = existing.get("source_span")
            sidecars = existing.get("sidecars")
            if (
                existing.get("output_path") == str(output_path)
                and existing.get("source_path") == str(source_path.resolve())
                and isinstance(span, dict)
                and abs(float(span.get("start_s")) - float(clip["start"])) <= 0.001
                and abs(float(span.get("end_s")) - float(clip["end"])) <= 0.001
                and isinstance(sidecars, dict)
                and existing.get("input_fingerprint") == expected_fingerprint
            ):
                qa = verify_render(
                    output_path,
                    float(clip["end"]) - float(clip["start"]),
                    str(existing.get("sha256")),
                    captions_path=sidecars.get("captions"),
                    crop_track_path=sidecars.get("crop_track"),
                    graphics_plan_path=sidecars.get("graphics"),
                    checksum_path=sidecars.get("checksum"),
                )
                if qa.get("passed") is True:
                    clip["render"] = {
                        "path": str(output_path),
                        "sha256": qa["sha256"],
                        "qa": qa,
                        "manifest_path": str(existing_manifest_path),
                        "sidecars": sidecars,
                        "dominant_mode": existing.get("dominant_mode"),
                        "visual_replacements": existing.get("visual_replacements"),
                        "reused_verified_render": True,
                    }
                    clip["status"] = AWAITING_REVIEW
                    clip["render_error"] = None
                    return clip
        except Exception:
            # Any mismatch falls through to a clean overwrite and fresh QA.
            pass
    try:
        rendered = render_clip(
            source_path,
            output_path,
            float(clip["start"]),
            float(clip["end"]),
            transcript_words,
            mode=render_mode,
            metadata=render_metadata,
        )
        qa = rendered.get("qa")
        if not isinstance(qa, dict) or qa.get("passed") is not True:
            raise RenderValidationError("render QA did not pass", qa or {})
        clip["render"] = {
            "path": rendered["output_path"],
            "sha256": rendered["sha256"],
            "qa": qa,
            "manifest_path": rendered.get("sidecars", {}).get("manifest"),
            "sidecars": rendered.get("sidecars", {}),
            "dominant_mode": rendered.get("dominant_mode"),
            "visual_replacements": rendered.get("visual_replacements"),
        }
        clip["status"] = AWAITING_REVIEW
        clip["render_error"] = None
    except RenderValidationError as exc:
        clip["status"] = FAILED
        clip["render"] = {
            "path": str(output_path) if output_path.exists() else None,
            "sha256": exc.qa.get("sha256"),
            "qa": dict(exc.qa),
            "manifest_path": str(output_path.with_suffix(".render.json")),
            "sidecars": {},
            "dominant_mode": None,
        }
        clip["render_error"] = str(exc)
        clip["warnings"] = sorted(set(clip["warnings"] + [str(exc)]))
    except Exception as exc:
        clip["status"] = FAILED
        clip["render"] = {
            "path": str(output_path) if output_path.exists() else None,
            "sha256": None,
            "qa": {
                "passed": False,
                "errors": [str(exc)],
                "warnings": [],
                "path": str(output_path),
            },
            "manifest_path": str(output_path.with_suffix(".render.json")),
            "sidecars": {},
            "dominant_mode": None,
        }
        clip["render_error"] = f"{type(exc).__name__}: {exc}"
        clip["warnings"] = sorted(set(clip["warnings"] + [clip["render_error"]]))
    return clip


def _load_validated_ranking(
    candidates: list[dict[str, Any]],
    *,
    pass1_path: Path,
    pass2_path: Path,
    rerank_limit: int,
) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    """Reuse completed model artifacts after a downstream render interruption."""
    candidate_by_id = {str(candidate["id"]): candidate for candidate in candidates}
    pass1_raw = read_json(pass1_path)
    pass1 = validate_pass1(pass1_raw, list(candidate_by_id))
    evaluation_by_id = {
        item["candidate_id"]: item for item in pass1["evaluations"]
    }
    pass2_raw = read_json(pass2_path)
    expected_finalist_ids = [
        item["candidate_id"]
        for item in sorted(
            [
                item
                for item in pass1["evaluations"]
                if is_single_subject_evaluation(item)
            ],
            key=lambda value: value["total_score"],
            reverse=True,
        )[: min(rerank_limit, len(pass1["evaluations"]))]
    ]
    pass2 = validate_pass2(pass2_raw, expected_finalist_ids)
    ranked = [
        {
            "candidate": candidate_by_id[item["candidate_id"]],
            "evaluation": evaluation_by_id[item["candidate_id"]],
            "rerank": item,
        }
        for item in pass2["ranking"]
    ]
    ranked.sort(key=lambda item: item["rerank"]["final_score"], reverse=True)
    return ranked, pass1, pass2


def analyze_job(
    job_path: Path,
    *,
    transcript_json: Path | None = None,
    transcriber: str = "faster-whisper",
    whisper_model: str = "large-v3-turbo",
    language: str | None = "en",
    claude_model: str = DEFAULT_CLAUDE_MODEL,
    openai_model: str = DEFAULT_OPENAI_MODEL,
    model_client: ModelClient | None = None,
    force_transcribe: bool = False,
    maximum_candidates: int = 64,
    minimum_score: int = 60,
    top_n: int = 5,
    render_mode: str = "auto",
    reuse_ranking: bool = False,
) -> dict[str, Any]:
    """Analyze a local job and stop in awaiting_review/needs_changes."""
    job_path = job_path.expanduser().resolve()
    initial = read_json(job_path)
    _validate_job(initial, job_path)
    started, _ = update_job(
        job_path,
        expected_revision=int(initial["revision"]),
        mutate=_mark_analysis_started,
    )
    analysis_dir = job_path.parent / "analysis"
    artifacts_dir = job_path.parent / "artifacts"
    analysis_dir.mkdir(parents=True, exist_ok=True)
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    try:
        source_path = _verify_source_integrity(started, phase="analysis start")
        transcript_path = artifacts_dir / "transcript.json"
        transcript, transcript_reused = transcribe_or_reuse(
            audio_path=Path(str(started["audio"]["path"])),
            audio_sha256=str(started["audio"]["sha256"]),
            destination=transcript_path,
            backend_name=transcriber,
            model_name=whisper_model,
            language=language,
            transcript_json=transcript_json,
            force=force_transcribe,
        )
        boundaries = build_sentence_units(transcript)
        all_candidates = generate_overlapping_candidates(boundaries)
        candidates = preselect_diverse_candidates(
            all_candidates, limit=maximum_candidates
        )
        if not candidates:
            raise ManifestError(
                "no complete 10-60 second candidate windows could be built from transcript"
            )
        boundaries_path = analysis_dir / "boundaries.json"
        candidates_path = analysis_dir / "candidates.json"
        atomic_write_json(boundaries_path, {"units": boundaries})
        atomic_write_json(
            candidates_path,
            {
                "generated_count": len(all_candidates),
                "preselected_count": len(candidates),
                "candidates": candidates,
            },
        )

        pass1_path = analysis_dir / "pass1.json"
        pass2_path = analysis_dir / "pass2.json"
        rerank_limit = min(len(candidates), max(12, top_n * 3))
        batch_size = 8
        ranking_context_path = analysis_dir / "ranking-input.json"
        expected_ranking_context = ranking_input_context(
            candidates,
            primary_model=claude_model,
            openai_model=openai_model,
            batch_size=batch_size,
            rerank_limit=rerank_limit,
        )
        if reuse_ranking:
            recorded_ranking_context = read_json(ranking_context_path)
            if recorded_ranking_context != expected_ranking_context:
                raise ManifestError(
                    "cached ranking input fingerprint does not match the current "
                    "transcript, candidates, prompts, or models"
                )
            try:
                ranked, pass1, pass2 = _load_validated_ranking(
                    candidates,
                    pass1_path=pass1_path,
                    pass2_path=pass2_path,
                    rerank_limit=rerank_limit,
                )
                ranking_client: ModelClient = AutoModelClient(
                    anthropic_model=claude_model,
                    openai_model=openai_model,
                )
                ranking_provider = "cached_validated"
                ranking_model = "previous-pass-artifacts"
                ranking_fallback_triggered = False
            except (ManifestError, ModelOutputError):
                existing_pass1 = read_json(pass1_path)
                ranking_client = model_client or AutoModelClient(
                    anthropic_model=claude_model,
                    openai_model=openai_model,
                )
                caller = StrictJsonCaller(
                    client=ranking_client,
                    model=claude_model,
                    retries=2,
                )
                ranked, pass1, pass2 = rank_two_pass(
                    candidates,
                    caller=caller,
                    batch_size=batch_size,
                    rerank_limit=rerank_limit,
                    pass1_checkpoint=lambda value: atomic_write_json(pass1_path, value),
                    existing_pass1=existing_pass1,
                )
                atomic_write_json(pass1_path, pass1)
                atomic_write_json(pass2_path, pass2)
                ranking_provider = str(
                    getattr(ranking_client, "provider_used", "custom")
                )
                ranking_model = str(
                    getattr(ranking_client, "model_used", claude_model)
                )
                ranking_fallback_triggered = bool(
                    getattr(ranking_client, "fallback_triggered", False)
                )
        else:
            atomic_write_json(ranking_context_path, expected_ranking_context)
            ranking_client = model_client or AutoModelClient(
                anthropic_model=claude_model,
                openai_model=openai_model,
            )
            caller = StrictJsonCaller(
                client=ranking_client,
                model=claude_model,
                retries=2,
            )
            ranked, pass1, pass2 = rank_two_pass(
                candidates,
                caller=caller,
                batch_size=batch_size,
                rerank_limit=rerank_limit,
                pass1_checkpoint=lambda value: atomic_write_json(pass1_path, value),
            )
            atomic_write_json(pass1_path, pass1)
            atomic_write_json(pass2_path, pass2)
            ranking_provider = str(
                getattr(ranking_client, "provider_used", "custom")
            )
            ranking_model = str(
                getattr(ranking_client, "model_used", claude_model)
            )
            ranking_fallback_triggered = bool(
                getattr(ranking_client, "fallback_triggered", False)
            )
        ranking_run_path = analysis_dir / "ranking-run.json"
        atomic_write_json(
            ranking_run_path,
            {
                "completed_at": utc_now(),
                "provider": ranking_provider,
                "model": ranking_model,
                "fallback_triggered": ranking_fallback_triggered,
                "reused": reuse_ranking,
                "input_fingerprint": expected_ranking_context["fingerprint"],
                "candidate_ids": [candidate["id"] for candidate in candidates],
            },
        )

        selected, rejected = deduplicate_ranked(
            ranked,
            source_kind=str(started.get("source_kind", "youtube_long")),
            minimum_score=minimum_score,
            top_n=top_n,
        )
        previous_clips = [
            clip
            for clip in started.get("clips", [])
            if isinstance(clip, dict)
        ]
        clips = []
        source_path = _verify_source_integrity(started, phase="pre-render")
        replacement_manifest_path = analysis_dir / "visual-replacements.json"
        replacement_manifest: dict[str, Any] | None = None
        if replacement_manifest_path.is_file():
            source_probe = started.get("source", {}).get("probe", {})
            source_duration = (
                float(source_probe.get("duration_s"))
                if isinstance(source_probe, dict)
                and source_probe.get("duration_s") is not None
                else None
            )
            replacement_manifest = load_visual_replacements(
                replacement_manifest_path,
                expected_source_sha256=str(started["source"]["sha256"]),
                source_duration_s=source_duration,
            )
        transcript_words = transcript.get("words")
        if not isinstance(transcript_words, list) or not transcript_words:
            raise ManifestError("word-level transcript is required for rendering")
        for index, item in enumerate(selected, start=1):
            clip = _clip_manifest(
                item,
                rank=index,
                previous_clips=previous_clips,
            )
            clips.append(
                _render_review_clip(
                    clip,
                    source_path=source_path,
                    source_sha256=str(started["source"]["sha256"]),
                    transcript_words=transcript_words,
                    job_dir=job_path.parent,
                    render_mode=render_mode,
                    visual_replacements=(
                        replacements_for_clip(
                            replacement_manifest,
                            float(clip["start"]),
                            float(clip["end"]),
                        )
                        if replacement_manifest
                        else []
                    ),
                )
            )
        _verify_source_integrity(started, phase="post-render")
        review_clips = [clip for clip in clips if clip["status"] == AWAITING_REVIEW]
        failed_clips = [clip for clip in clips if clip["status"] == FAILED]
        selection_audit_path = analysis_dir / "selection-audit.json"
        atomic_write_json(
            selection_audit_path,
            {
                "minimum_score": minimum_score,
                "top_n": top_n,
                "selected_candidate_ids": [item["candidate"]["id"] for item in selected],
                "qa_passed_clip_ids": [clip["id"] for clip in review_clips],
                "render_failed_clip_ids": [clip["id"] for clip in failed_clips],
                "rejected": [
                    {
                        "candidate_id": item["candidate"]["id"],
                        "final_score": item["rerank"]["final_score"],
                        "selection_reasons": item["selection_reasons"],
                        "duplicate_of": item["duplicate_of"],
                    }
                    for item in rejected
                ],
            },
        )

        def finalize(job: dict[str, Any]) -> None:
            if str(job.get("status")) != PROCESSING:
                raise InvalidTransition(
                    f"job changed during analysis: expected processing, got {job.get('status')}"
                )
            now = utc_now()
            selected_candidate_ids = {clip.get("candidate_id") for clip in clips}
            archive = [
                item
                for item in job.get("clip_archive", [])
                if isinstance(item, dict)
            ]
            archived_ids = {
                (item.get("id"), item.get("version")) for item in archive
            }
            for prior in previous_clips:
                if prior.get("candidate_id") in selected_candidate_ids:
                    continue
                identity = (prior.get("id"), prior.get("version"))
                if identity not in archived_ids:
                    archive.append(_archived_version(prior))
                    archived_ids.add(identity)
            job["clip_archive"] = archive
            job["clips"] = clips
            if review_clips:
                job["status"] = AWAITING_REVIEW
                job["error"] = None
            elif clips:
                job["status"] = FAILED
                job["error"] = {
                    "type": "RenderFailure",
                    "message": "No selected clip passed fail-closed render QA.",
                }
            else:
                job["status"] = NEEDS_CHANGES
                job["error"] = None
            job["warnings"] = []
            if not clips:
                job["warnings"].append(
                    f"No candidates met the {minimum_score}-point selection threshold."
                )
            if failed_clips:
                job["warnings"].append(
                    f"{len(failed_clips)} selected clip(s) failed render QA and cannot be reviewed."
                )
            job["analysis"] = {
                "schema_version": "shorts-analysis/v1",
                "completed_at": now,
                "transcriber": transcript["provider"],
                "whisper_model": transcript["model"],
                "transcript_reused": transcript_reused,
                "ranking_provider": ranking_provider,
                "ranking_model": ranking_model,
                "ranking_fallback_triggered": ranking_fallback_triggered,
                "ranking_reused": reuse_ranking,
                "ranking_run_path": str(ranking_run_path),
                "claude_model": (
                    claude_model
                    if ranking_provider == "anthropic"
                    else None
                ),
                "transcript_path": str(transcript_path),
                "boundaries_path": str(boundaries_path),
                "candidates_path": str(candidates_path),
                "pass1_path": str(pass1_path),
                "pass2_path": str(pass2_path),
                "selection_audit_path": str(selection_audit_path),
                "generated_candidate_count": len(all_candidates),
                "scored_candidate_count": len(candidates),
                "selected_clip_count": len(clips),
                "review_clip_count": len(review_clips),
                "render_failed_clip_count": len(failed_clips),
                "render_mode": render_mode,
                "visual_replacements_path": (
                    str(replacement_manifest_path) if replacement_manifest else None
                ),
                "visual_replacement_count": (
                    len(replacement_manifest["replacements"])
                    if replacement_manifest
                    else 0
                ),
                "minimum_score": minimum_score,
                "top_n": top_n,
                "dedupe": {
                    "time_iou_threshold": 0.20,
                    "text_similarity_threshold": 0.75,
                },
            }
            job.setdefault("history", []).append(
                {
                    "at": now,
                    "event": "analysis_completed",
                    "from": PROCESSING,
                    "to": job["status"],
                    "review_clip_count": len(review_clips),
                    "render_failed_clip_count": len(failed_clips),
                }
            )

        final, _ = update_job(
            job_path,
            expected_revision=int(started["revision"]),
            mutate=finalize,
        )
        write_clip_manifests(job_path, final)
        return final
    except BaseException as exc:
        recorded = (
            exc
            if isinstance(exc, Exception)
            else RuntimeError(f"analysis interrupted by {type(exc).__name__}")
        )
        _mark_failed(job_path, recorded)
        raise


def decide_job(
    job_path: Path,
    *,
    clip_id: str,
    decision: str,
    expected_revision: int,
    actor: str,
    reason: str | None = None,
    requested_changes: str | None = None,
    waive_unverified_claims: bool = False,
) -> dict[str, Any]:
    job_path = job_path.expanduser().resolve()
    updated, _ = update_job(
        job_path,
        expected_revision=expected_revision,
        mutate=lambda job: apply_clip_decision(
            job,
            clip_id=clip_id,
            decision=decision,
            actor=actor,
            job_dir=job_path.parent,
            reason=reason,
            requested_changes=requested_changes,
            waive_unverified_claims=waive_unverified_claims,
        ),
    )
    write_clip_manifests(job_path, updated)
    return updated


def load_job(output_root: Path, job: str | Path) -> tuple[Path, dict[str, Any]]:
    path = resolve_job_path(output_root, job)
    payload = read_json(path)
    _validate_job(payload, path)
    return path, payload


def list_jobs(output_root: Path) -> list[dict[str, Any]]:
    jobs_root = output_root.expanduser().resolve() / "jobs"
    if not jobs_root.exists():
        return []
    jobs: list[dict[str, Any]] = []
    for path in jobs_root.glob("*/job.json"):
        try:
            value = read_json(path)
            jobs.append(
                {
                    "job_id": value.get("job_id"),
                    "title": value.get("title"),
                    "status": value.get("status"),
                    "revision": value.get("revision"),
                    "clip_count": len(value.get("clips", [])),
                    "updated_at": value.get("updated_at"),
                    "path": str(path),
                }
            )
        except ManifestError:
            continue
    return sorted(jobs, key=lambda value: str(value.get("updated_at", "")), reverse=True)
