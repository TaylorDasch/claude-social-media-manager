"""Command-line interface for the local shorts factory."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

from .errors import ShortsFactoryError
from .ingest import ingest_local
from .pipeline import analyze_job, decide_job, list_jobs, load_job
from .ranking import DEFAULT_CLAUDE_MODEL, DEFAULT_OPENAI_MODEL
from .storage import DEFAULT_ROOT


def _default_root() -> Path:
    return Path(os.environ.get("SHORTS_FACTORY_ROOT", str(DEFAULT_ROOT))).expanduser()


def _add_root(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--root",
        type=Path,
        default=_default_root(),
        help="Factory data root (default: SHORTS_FACTORY_ROOT or ~/claude-video/shorts-factory)",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="shorts-factory",
        description="Local long-form to approval-gated short clip manifests.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    ingest = subparsers.add_parser("ingest", help="Reference a local master and extract audio")
    ingest.add_argument("source", type=Path)
    ingest.add_argument("--title")
    ingest.add_argument(
        "--source-kind",
        choices=["youtube_long", "original_vertical", "other"],
        default="youtube_long",
    )
    ingest.add_argument("--force-audio", action="store_true")
    _add_root(ingest)

    analyze = subparsers.add_parser("analyze", help="Transcribe, score, rerank, and queue review")
    analyze.add_argument("job", help="Job id, job directory, or job.json path")
    analyze.add_argument("--transcript-json", type=Path)
    analyze.add_argument("--transcriber", default="faster-whisper")
    analyze.add_argument("--whisper-model", default="large-v3-turbo")
    analyze.add_argument("--language", default="en")
    analyze.add_argument("--model", default=DEFAULT_CLAUDE_MODEL)
    analyze.add_argument("--openai-model", default=DEFAULT_OPENAI_MODEL)
    analyze.add_argument("--force-transcribe", action="store_true")
    analyze.add_argument(
        "--reuse-ranking",
        action="store_true",
        help="Reuse and strictly revalidate existing pass1/pass2 artifacts after a downstream failure.",
    )
    analyze.add_argument("--max-candidates", type=int, default=64)
    analyze.add_argument("--minimum-score", type=int, default=60)
    analyze.add_argument("--top-n", type=int, default=5)
    analyze.add_argument(
        "--render-mode",
        choices=["auto", "talking_head", "b_roll", "graphic_safe", "face_crop", "saliency_crop", "contain"],
        default="auto",
    )
    _add_root(analyze)

    run = subparsers.add_parser("run", help="Ingest and analyze one local master")
    run.add_argument("source", type=Path)
    run.add_argument("--title")
    run.add_argument(
        "--source-kind",
        choices=["youtube_long", "original_vertical", "other"],
        default="youtube_long",
    )
    run.add_argument("--transcript-json", type=Path)
    run.add_argument("--transcriber", default="faster-whisper")
    run.add_argument("--whisper-model", default="large-v3-turbo")
    run.add_argument("--language", default="en")
    run.add_argument("--model", default=DEFAULT_CLAUDE_MODEL)
    run.add_argument("--openai-model", default=DEFAULT_OPENAI_MODEL)
    run.add_argument("--force-audio", action="store_true")
    run.add_argument("--force-transcribe", action="store_true")
    run.add_argument("--reuse-ranking", action="store_true")
    run.add_argument("--max-candidates", type=int, default=64)
    run.add_argument("--minimum-score", type=int, default=60)
    run.add_argument("--top-n", type=int, default=5)
    run.add_argument(
        "--render-mode",
        choices=["auto", "talking_head", "b_roll", "graphic_safe", "face_crop", "saliency_crop", "contain"],
        default="auto",
    )
    _add_root(run)

    status = subparsers.add_parser("status", help="Show one job or the local queue")
    status.add_argument("job", nargs="?")
    status.add_argument("--full", action="store_true", help="Print the complete job manifest")
    _add_root(status)

    decide = subparsers.add_parser("decide", help="Record an approval/revision/decline decision")
    decide.add_argument("job")
    decide.add_argument("clip_id")
    decide.add_argument(
        "decision",
        choices=["approve", "approved", "needs_changes", "needs-changes", "decline", "declined"],
    )
    decide.add_argument("--expected-revision", type=int, required=True)
    decide.add_argument("--actor", default="taylor")
    decide.add_argument("--reason")
    decide.add_argument("--requested-changes")
    decide.add_argument(
        "--waive-unverified-claims",
        action="store_true",
        help="Taylor explicitly confirms unresolved verify/high-risk spoken claims.",
    )
    _add_root(decide)
    return parser


def _summary(job: dict[str, Any], path: Path) -> dict[str, Any]:
    return {
        "status": "ok",
        "job_id": job["job_id"],
        "job_status": job["status"],
        "revision": job["revision"],
        "clip_count": len(job.get("clips", [])),
        "job_path": str(path),
    }


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = args.root.expanduser().resolve()
    try:
        if args.command == "ingest":
            path, job = ingest_local(
                args.source,
                root,
                title=args.title,
                source_kind=args.source_kind,
                force_audio=args.force_audio,
            )
            result = _summary(job, path)
        elif args.command == "analyze":
            path, _ = load_job(root, args.job)
            job = analyze_job(
                path,
                transcript_json=args.transcript_json,
                transcriber=args.transcriber,
                whisper_model=args.whisper_model,
                language=args.language or None,
                claude_model=args.model,
                openai_model=args.openai_model,
                force_transcribe=args.force_transcribe,
                maximum_candidates=args.max_candidates,
                minimum_score=args.minimum_score,
                top_n=args.top_n,
                render_mode=args.render_mode,
                reuse_ranking=args.reuse_ranking,
            )
            result = _summary(job, path)
        elif args.command == "run":
            path, _ = ingest_local(
                args.source,
                root,
                title=args.title,
                source_kind=args.source_kind,
                force_audio=args.force_audio,
            )
            job = analyze_job(
                path,
                transcript_json=args.transcript_json,
                transcriber=args.transcriber,
                whisper_model=args.whisper_model,
                language=args.language or None,
                claude_model=args.model,
                openai_model=args.openai_model,
                force_transcribe=args.force_transcribe,
                maximum_candidates=args.max_candidates,
                minimum_score=args.minimum_score,
                top_n=args.top_n,
                render_mode=args.render_mode,
                reuse_ranking=args.reuse_ranking,
            )
            result = _summary(job, path)
        elif args.command == "status":
            if args.job:
                path, job = load_job(root, args.job)
                result = job if args.full else _summary(job, path)
            else:
                result = {"status": "ok", "root": str(root), "jobs": list_jobs(root)}
        elif args.command == "decide":
            path, _ = load_job(root, args.job)
            job = decide_job(
                path,
                clip_id=args.clip_id,
                decision=args.decision,
                expected_revision=args.expected_revision,
                actor=args.actor,
                reason=args.reason,
                requested_changes=args.requested_changes,
                waive_unverified_claims=args.waive_unverified_claims,
            )
            result = _summary(job, path)
        else:  # pragma: no cover - argparse guarantees a command
            raise AssertionError(args.command)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (ShortsFactoryError, FileNotFoundError, ValueError) as exc:
        print(
            json.dumps(
                {"status": "error", "error": type(exc).__name__, "message": str(exc)},
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
