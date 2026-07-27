# Stylecraft CapCut Timeline Transcript

This folder is a read-only reconstruction of the active CapCut project timeline. The CapCut draft itself was not edited.

## Final 24 fps snapshot

- Frozen draft: `draft_info.snapshot.json`
- SHA-256: `4a672c48b08d3355117050db81e80a33c9e62d819535cd4b465480a0b6a0a0b5`
- Duration: `00:27:40.250`
- Main-track edits: 69
- Overlay edits: 11

## Start here

- `TIMELINE-CLIP-MAP.md` — human-readable edit order with timeline and source in/out points
- `timeline-clip-map.tsv` — spreadsheet-friendly version of the same map
- `TIMESTAMPED-TRANSCRIPT.md` — readable machine transcript aligned to the rendered timeline
- `stylecraft-capcut-timeline-final-24fps-base-en.srt` — subtitle-format transcript
- `TRANSCRIPTION-MANIFEST.md` — source lock, reconstruction method, model details, and timing limits

## Reconstruction files

- `timeline-audio-48k-stereo.flac` — lossless 48 kHz timeline audio mix
- `timeline-whisper-16k-mono.wav` — exact-duration Whisper input
- `timeline-segments.json` — machine-readable edit map
- `stylecraft-capcut-timeline-final-24fps-base-en.json` — raw Whisper result
- `build-timeline-artifacts.mjs`, `render-timeline-audio.zsh`, and `build-transcript-markdown.mjs` — reproducibility scripts

The `superseded-30fps-snapshot/` directory contains the earlier transcript that was generated before the final project-rate change. Do not use it for edit decisions.

