#!/usr/bin/env python3
"""
transcribe-batch.py — for /clip-grader skill

Walks shorts/inbox/, runs ffprobe + Whisper (tiny.en) on each clip,
and writes shorts/reports/batch-YYYY-MM-DD-HHMM.json with structured data
for Claude to score against the grader rubric.

Usage:
  ./transcribe-batch.py
  ./transcribe-batch.py --inbox /custom/path --whisper-model base.en
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

VIDEO_EXTS = {".mp4", ".mov", ".mkv", ".webm", ".m4v"}

def run(cmd, **kwargs):
    return subprocess.run(cmd, capture_output=True, text=True, **kwargs)

def ffprobe_meta(path: Path) -> dict:
    r = run([
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_format", "-show_streams", str(path)
    ])
    if r.returncode != 0:
        return {"error": r.stderr.strip()[:200]}
    try:
        data = json.loads(r.stdout)
    except json.JSONDecodeError as e:
        return {"error": f"ffprobe json parse: {e}"}
    vstream = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), {})
    fmt = data.get("format", {})
    dur = float(fmt.get("duration", 0)) if fmt.get("duration") else None
    size_b = int(fmt.get("size", 0)) if fmt.get("size") else None
    return {
        "duration_sec": round(dur, 2) if dur else None,
        "width": vstream.get("width"),
        "height": vstream.get("height"),
        "aspect_ratio": vstream.get("display_aspect_ratio"),
        "fps": eval(vstream.get("avg_frame_rate", "0/1") or "0/1") if vstream.get("avg_frame_rate") not in (None, "0/0") else None,
        "size_mb": round(size_b / 1_000_000, 2) if size_b else None,
        "codec": vstream.get("codec_name"),
    }

def transcribe(path: Path, model: str, tmpdir: Path) -> dict:
    out_json = tmpdir / (path.stem + ".json")
    r = run([
        "whisper", str(path),
        "--model", model,
        "--language", "en",
        "--output_format", "json",
        "--output_dir", str(tmpdir),
        "--verbose", "False",
        "--fp16", "False",
        "--task", "transcribe",
    ])
    if r.returncode != 0:
        return {"error": r.stderr.strip()[:300] or r.stdout.strip()[:300]}
    if not out_json.exists():
        return {"error": "whisper produced no json"}
    try:
        data = json.loads(out_json.read_text())
    except json.JSONDecodeError as e:
        return {"error": f"whisper json parse: {e}"}
    segments = data.get("segments", []) or []
    full_text = (data.get("text") or "").strip()
    first_5s_words = []
    for seg in segments:
        if seg.get("start", 0) <= 5.0:
            first_5s_words.append(seg.get("text", "").strip())
        else:
            break
    return {
        "full_text": full_text,
        "first_5s": " ".join(first_5s_words).strip(),
        "first_10s": " ".join(
            seg.get("text", "").strip() for seg in segments if seg.get("start", 0) <= 10.0
        ).strip(),
        "n_segments": len(segments),
        "lang_detected": data.get("language"),
    }

def main():
    ap = argparse.ArgumentParser()
    default_inbox = Path.home() / "claude-social-media-manager" / "shorts" / "inbox"
    default_reports = Path.home() / "claude-social-media-manager" / "shorts" / "reports"
    ap.add_argument("--inbox", default=str(default_inbox))
    ap.add_argument("--reports", default=str(default_reports))
    ap.add_argument("--whisper-model", default="tiny.en",
                    help="tiny.en (fastest) | base.en | small.en | medium.en")
    ap.add_argument("--limit", type=int, default=0, help="Cap clips processed (0 = no cap)")
    args = ap.parse_args()

    inbox = Path(args.inbox)
    reports = Path(args.reports)
    reports.mkdir(parents=True, exist_ok=True)

    if not inbox.exists():
        print(f"ERROR: inbox not found: {inbox}", file=sys.stderr)
        sys.exit(1)

    clips = sorted(
        [p for p in inbox.iterdir() if p.suffix.lower() in VIDEO_EXTS and not p.name.startswith(".")],
        key=lambda p: p.stat().st_mtime,
    )
    if args.limit:
        clips = clips[: args.limit]

    if not clips:
        print(f"No video files in {inbox}. Drop .mp4/.mov/.mkv files there and re-run.", file=sys.stderr)
        sys.exit(2)

    stamp = datetime.now().strftime("%Y-%m-%d-%H%M")
    out_path = reports / f"batch-{stamp}.json"

    print(f"Found {len(clips)} clips in {inbox}", file=sys.stderr)
    print(f"Whisper model: {args.whisper_model}", file=sys.stderr)

    items = []
    with tempfile.TemporaryDirectory(prefix="clipgrader-") as td:
        tmpdir = Path(td)
        for i, p in enumerate(clips, 1):
            print(f"  [{i}/{len(clips)}] {p.name} ... ", end="", file=sys.stderr, flush=True)
            meta = ffprobe_meta(p)
            tx = transcribe(p, args.whisper_model, tmpdir)
            items.append({
                "filename": p.name,
                "path": str(p),
                "mtime": datetime.fromtimestamp(p.stat().st_mtime).isoformat(),
                "meta": meta,
                "transcript": tx,
            })
            ok = "OK" if "error" not in tx and "error" not in meta else "ERR"
            extra = ""
            if "error" in tx:
                extra = f" (whisper: {tx['error'][:60]})"
            elif "error" in meta:
                extra = f" (ffprobe: {meta['error'][:60]})"
            print(f"{ok}{extra}", file=sys.stderr)

    payload = {
        "generated_at": datetime.now().isoformat(),
        "inbox": str(inbox),
        "whisper_model": args.whisper_model,
        "count": len(items),
        "clips": items,
    }
    out_path.write_text(json.dumps(payload, indent=2))
    print(f"\nWrote: {out_path}", file=sys.stderr)
    print(str(out_path))  # stdout = path, so callers can capture

if __name__ == "__main__":
    main()
