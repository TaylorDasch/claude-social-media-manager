# Stylecraft CapCut Timeline Transcript

This folder is a read-only reconstruction of the active CapCut project timeline. The CapCut draft itself was not edited.

## Current 24 fps snapshot

- Frozen draft: `draft_info.snapshot.json`
- SHA-256: `e3c6b10dde3324d2c238ffe5f059a442ee0c2e9a780f9dbc039cf9dbf37a8a26`
- Duration: `00:27:18.208`
- Main-track edits: 68
- Overlay edits: 9

## Start here

- `EDIT-DECISION-LIST.md` — exact current-time cut, keep, cover, and pickup decisions
- `TIMELINE-CLIP-MAP.md` — edit order with timeline and source in/out points
- `timeline-clip-map.tsv` — spreadsheet-friendly version of the edit map
- `TIMESTAMPED-TRANSCRIPT.md` — readable machine transcript aligned to the current timeline
- `stylecraft-capcut-timeline-final-24fps-base-en.srt` — subtitle-format transcript
- `TRANSCRIPTION-MANIFEST.md` — source lock, reconstruction method, model details, and timing limits

## Reconstruction files

- `timeline-audio-48k-stereo.flac` — lossless 48 kHz timeline audio mix
- `timeline-whisper-16k-mono.wav` — exact-duration Whisper input
- `timeline-segments.json` — machine-readable edit map
- `stylecraft-capcut-timeline-final-24fps-base-en.json` — raw Whisper result
- `build-timeline-artifacts.mjs`, `render-timeline-audio.zsh`, and `build-transcript-markdown.mjs` — reproducibility scripts

## Media-link check

- The DJI outro source is online at CapCut's linked path:
  `/Volumes/Untitled 1/DCIM/DJI_001/DJI_20260726134740_0421_D.MP4`
- It was restored as a copy from the volume Trash; the Trash copy was left untouched.
- Source and restored copy match SHA-256:
  `c94af6409869249ed8a81beb8a52ec30364b2bc5899fdb42beb46755bc6fb572`

The following directories are historical and must not be used for current edit decisions:

- `superseded-24fps-pre-c6779-removal-4a672c48/`
- `superseded-30fps-snapshot/`
