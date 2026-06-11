#!/usr/bin/env python3
"""
generate-cta-audio.py — Phase 1 of CTA pipeline for /clip-grader

For each keeper in a keepers manifest, extract the comment-keyword CTA line
from the TikTok caption, generate an MP3 in Taylor's ElevenLabs cloned voice
(Dasch YT Voice, voice_id 5uXjRsasfECt86L0kAzz), and save to:
  ~/claude-social-media-manager/shorts/keepers/cta/{clip_stem}.mp3

Usage:
  ./generate-cta-audio.py <keepers-manifest.json>
  ./generate-cta-audio.py <keepers-manifest.json> --voice-id <id> --model eleven_multilingual_v2

Env:
  ELEVENLABS_API_KEY  — required (from ~/shared-keys.env)
  ELEVENLABS_VOICE_ID — optional, defaults to Dasch YT Voice clone
"""
import argparse
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

DEFAULT_VOICE_ID = "5uXjRsasfECt86L0kAzz"  # Dasch YT Voice (professional clone)
DEFAULT_MODEL = "eleven_multilingual_v2"

def load_key():
    key = os.environ.get("ELEVENLABS_API_KEY")
    if key:
        return key
    env_file = Path.home() / "shared-keys.env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith("ELEVENLABS_API_KEY="):
                return line.split("=", 1)[1].strip()
    return None

def extract_cta_line(caption: str) -> str:
    """Pull the 'Comment X for Y' line from the caption.
    Falls back to the last sentence before the hashtags."""
    # Look for "Comment <KEYWORD> for ..." pattern
    m = re.search(r"(Comment\s+[A-Z]+\s+for[^\n.#]+\.?)", caption)
    if m:
        return m.group(1).strip()
    # Fall back: last non-empty non-hashtag line before the tags
    lines = [l.strip() for l in caption.split("\n") if l.strip() and not l.strip().startswith("#")]
    if lines:
        return lines[-1]
    return ""

def tts(text: str, voice_id: str, model: str, api_key: str, out_path: Path) -> bool:
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format=mp3_44100_128"
    payload = json.dumps({
        "text": text,
        "model_id": model,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.0,
            "use_speaker_boost": True,
        },
    }).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="ignore")[:300]
        print(f"  HTTP {e.code}: {body}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"  ERROR: {e}", file=sys.stderr)
        return False
    if len(data) < 1000:
        print(f"  WARN: response only {len(data)} bytes — likely error", file=sys.stderr)
        return False
    out_path.write_bytes(data)
    return True

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest", help="Path to keepers-*.json")
    ap.add_argument("--voice-id", default=os.environ.get("ELEVENLABS_VOICE_ID", DEFAULT_VOICE_ID))
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--out-dir", default=str(Path.home() / "claude-social-media-manager" / "shorts" / "keepers" / "cta"))
    args = ap.parse_args()

    api_key = load_key()
    if not api_key:
        print("ERROR: ELEVENLABS_API_KEY not found in env or ~/shared-keys.env", file=sys.stderr)
        sys.exit(1)

    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print(f"ERROR: manifest not found: {manifest_path}", file=sys.stderr)
        sys.exit(1)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    keepers = json.loads(manifest_path.read_text())
    print(f"Manifest: {manifest_path.name} — {len(keepers)} keeper(s)")
    print(f"Voice ID: {args.voice_id} | Model: {args.model}")
    print(f"Output dir: {out_dir}\n")

    results = []
    for i, k in enumerate(keepers, 1):
        clip_path = Path(k["path"])
        stem = clip_path.stem
        out_path = out_dir / f"{stem}.mp3"
        caption = k.get("caption_tiktok", "")
        cta = extract_cta_line(caption)
        if not cta:
            print(f"[{i}/{len(keepers)}] {stem}\n  SKIP: no CTA line found in caption")
            results.append({"clip": stem, "cta": None, "mp3": None, "status": "no_cta"})
            continue
        print(f"[{i}/{len(keepers)}] {stem}\n  CTA: \"{cta}\"")
        ok = tts(cta, args.voice_id, args.model, api_key, out_path)
        if ok:
            size_kb = out_path.stat().st_size / 1024
            print(f"  OK: {out_path.name} ({size_kb:.1f} KB)\n")
            results.append({"clip": stem, "cta": cta, "mp3": str(out_path), "status": "ok", "size_kb": round(size_kb, 1)})
        else:
            print(f"  FAILED\n")
            results.append({"clip": stem, "cta": cta, "mp3": None, "status": "failed"})

    # Write a small results manifest alongside
    results_path = out_dir / f"results-{manifest_path.stem.replace('keepers-', '')}.json"
    results_path.write_text(json.dumps(results, indent=2))
    print(f"Results: {results_path}")
    n_ok = sum(1 for r in results if r["status"] == "ok")
    print(f"\nGenerated {n_ok}/{len(results)} CTA tracks.")

if __name__ == "__main__":
    main()
