#!/usr/bin/env python3
"""
stitch-cta-tail.py — Phase 2 of CTA pipeline for /clip-grader

For each keeper in a manifest, build an augmented .mp4 that:
  1. Plays the original clip in full
  2. Appends a CTA tail (last frame frozen + on-screen text + ElevenLabs voiceover)

Expects matching CTA audio at:
  ~/claude-social-media-manager/shorts/keepers/cta/{clip_stem}.mp3

Writes augmented videos to:
  ~/claude-social-media-manager/shorts/keepers/with-cta/{clip_stem}.mp4

Usage:
  ./stitch-cta-tail.py <keepers-manifest.json>
  ./stitch-cta-tail.py <keepers-manifest.json> --tail-pad 0.5
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
DEFAULT_TAIL_PAD = 0.6  # extra seconds beyond audio for text-read buffer

def run(cmd, **kwargs):
    return subprocess.run(cmd, capture_output=True, text=True, **kwargs)

def ffprobe_duration(path: Path) -> float:
    r = run(["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)])
    try:
        return float(r.stdout.strip())
    except (ValueError, AttributeError):
        return 0.0

def ffprobe_dims(path: Path):
    r = run([
        "ffprobe", "-v", "quiet", "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate",
        "-of", "csv=p=0:s=x", str(path)
    ])
    parts = r.stdout.strip().split("x")
    if len(parts) < 2:
        return None, None, 30
    try:
        w = int(parts[0]); h = int(parts[1])
        fps_str = parts[2] if len(parts) > 2 else "30/1"
        num, den = fps_str.split("/")
        fps = int(round(float(num) / float(den))) if float(den) > 0 else 30
        return w, h, fps
    except Exception:
        return None, None, 30

def extract_keyword(cta_text: str) -> str:
    """From 'Comment MARKET for the breakdown...' → 'MARKET'"""
    m = re.search(r"Comment\s+([A-Z][A-Z0-9_]+)", cta_text)
    return m.group(1) if m else "DM"

def extract_last_frame(video: Path, out_png: Path) -> bool:
    """Grab a frame near the end of the video as PNG."""
    dur = ffprobe_duration(video)
    seek = max(0.0, dur - 0.15)
    r = run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-ss", f"{seek:.3f}", "-i", str(video),
        "-vframes", "1", "-q:v", "2", str(out_png),
    ])
    return r.returncode == 0 and out_png.exists()

def render_text_png(keyword: str, width: int, height: int, out_png: Path) -> bool:
    """Render 'Comment {KEYWORD}' as a transparent PNG sized to the video.
    PIL approach because ffmpeg here lacks the drawtext filter (no libfreetype)."""
    overlay_text = f"Comment {keyword}"
    fontsize = max(80, int(height * 0.055))
    pad = max(30, int(fontsize * 0.5))
    try:
        font = ImageFont.truetype(FONT, fontsize)
    except OSError:
        font = ImageFont.load_default()
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    bbox = draw.textbbox((0, 0), overlay_text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    box_w = text_w + pad * 2
    box_h = text_h + pad * 2
    x_box = (width - box_w) // 2
    y_box = int(height * 0.72)
    draw.rectangle([x_box, y_box, x_box + box_w, y_box + box_h], fill=(0, 0, 0, 220))
    x_text = x_box + pad - bbox[0]
    y_text = y_box + pad - bbox[1]
    draw.text((x_text, y_text), overlay_text, font=font, fill=(255, 255, 255, 255))
    img.save(out_png, "PNG")
    return out_png.exists()

def build_cta_tail(frame_png: Path, cta_audio: Path, keyword: str,
                   width: int, height: int, fps: int, tail_pad: float,
                   out_mp4: Path) -> bool:
    """Build a tail video: frozen frame + PNG text overlay composite + voiceover."""
    audio_dur = ffprobe_duration(cta_audio)
    tail_dur = audio_dur + tail_pad
    with tempfile.TemporaryDirectory(prefix="tail-") as td:
        td = Path(td)
        text_png = td / "text.png"
        if not render_text_png(keyword, width, height, text_png):
            print(f"  text PNG render failed", file=sys.stderr)
            return False
        r = run([
            "ffmpeg", "-y", "-loglevel", "error",
            "-loop", "1", "-framerate", str(fps), "-i", str(frame_png),
            "-loop", "1", "-framerate", str(fps), "-i", str(text_png),
            "-i", str(cta_audio),
            "-filter_complex", "[0:v][1:v]overlay=0:0:format=auto[v]",
            "-map", "[v]", "-map", "2:a",
            "-c:v", "libx264", "-preset", "fast", "-tune", "stillimage",
            "-c:a", "aac", "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            "-t", f"{tail_dur:.2f}",
            "-r", str(fps),
            "-s", f"{width}x{height}",
            str(out_mp4),
        ])
        if r.returncode != 0:
            print(f"  ffmpeg tail build failed: {r.stderr[:300]}", file=sys.stderr)
            return False
        return out_mp4.exists()

def concat_clips(original: Path, tail: Path, fps: int, out_mp4: Path) -> bool:
    """Re-encode concat via filter graph for codec consistency."""
    r = run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", str(original), "-i", str(tail),
        "-filter_complex",
        "[0:v]setsar=1[v0];[1:v]setsar=1[v1];[v0][0:a][v1][1:a]concat=n=2:v=1:a=1[v][a]",
        "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-r", str(fps),
        "-movflags", "+faststart",
        str(out_mp4),
    ])
    if r.returncode != 0:
        print(f"  ffmpeg concat failed: {r.stderr[:400]}", file=sys.stderr)
        return False
    return out_mp4.exists()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest")
    ap.add_argument("--cta-dir", default=str(Path.home() / "claude-social-media-manager" / "shorts" / "keepers" / "cta"))
    ap.add_argument("--out-dir", default=str(Path.home() / "claude-social-media-manager" / "shorts" / "keepers" / "with-cta"))
    ap.add_argument("--tail-pad", type=float, default=DEFAULT_TAIL_PAD)
    args = ap.parse_args()

    manifest_path = Path(args.manifest)
    cta_dir = Path(args.cta_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if not Path(FONT).exists():
        print(f"ERROR: font missing: {FONT}", file=sys.stderr)
        sys.exit(1)

    keepers = json.loads(manifest_path.read_text())
    print(f"Stitching {len(keepers)} keeper(s)...\n")

    results = []
    for i, k in enumerate(keepers, 1):
        clip = Path(k["path"])
        stem = clip.stem
        cta_mp3 = cta_dir / f"{stem}.mp3"
        out_mp4 = out_dir / f"{stem}.mp4"

        print(f"[{i}/{len(keepers)}] {stem}")
        if not clip.exists():
            print(f"  SKIP: clip missing"); results.append({"clip": stem, "status": "no_clip"}); continue
        if not cta_mp3.exists():
            print(f"  SKIP: CTA mp3 missing at {cta_mp3}"); results.append({"clip": stem, "status": "no_cta"}); continue

        w, h, fps = ffprobe_dims(clip)
        if not w:
            print(f"  SKIP: could not read video dims"); results.append({"clip": stem, "status": "bad_dims"}); continue
        keyword = extract_keyword(k.get("caption_tiktok", ""))
        print(f"  Dims: {w}x{h}@{fps}fps | Keyword: {keyword}")

        with tempfile.TemporaryDirectory(prefix="stitch-") as td:
            td = Path(td)
            frame = td / "lastframe.png"
            tail = td / "tail.mp4"
            if not extract_last_frame(clip, frame):
                print(f"  FAIL: extract last frame"); results.append({"clip": stem, "status": "frame_fail"}); continue
            if not build_cta_tail(frame, cta_mp3, keyword, w, h, fps, args.tail_pad, tail):
                results.append({"clip": stem, "status": "tail_fail"}); continue
            tail_dur = ffprobe_duration(tail)
            if not concat_clips(clip, tail, fps, out_mp4):
                results.append({"clip": stem, "status": "concat_fail"}); continue
            final_dur = ffprobe_duration(out_mp4)
            final_mb = out_mp4.stat().st_size / 1_000_000
            print(f"  OK: {out_mp4.name} | final={final_dur:.1f}s ({final_mb:.1f} MB) | tail={tail_dur:.1f}s\n")
            results.append({
                "clip": stem,
                "status": "ok",
                "out": str(out_mp4),
                "final_duration": round(final_dur, 2),
                "tail_duration": round(tail_dur, 2),
                "final_size_mb": round(final_mb, 2),
                "keyword": keyword,
            })

    n_ok = sum(1 for r in results if r["status"] == "ok")
    print(f"Stitched {n_ok}/{len(results)}.")
    results_path = out_dir / f"results-{manifest_path.stem.replace('keepers-', '')}.json"
    results_path.write_text(json.dumps(results, indent=2))
    print(f"Results: {results_path}")

if __name__ == "__main__":
    main()
