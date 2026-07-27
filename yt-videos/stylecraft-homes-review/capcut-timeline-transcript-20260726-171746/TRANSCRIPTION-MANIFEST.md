# Transcription Manifest

## Source lock

- CapCut project: `/Users/taylordasch_1/Movies/CapCut/User Data/Projects/com.lveditor.draft/0726 (1)`
- Frozen timeline snapshot: `draft_info.snapshot.json`
- Snapshot SHA-256: `e3c6b10dde3324d2c238ffe5f059a442ee0c2e9a780f9dbc039cf9dbf37a8a26`
- Timeline ID: `FAF19BF6-9603-498B-85F1-8864EC2426FC`
- Timeline duration: 1638.208333 seconds
- Timeline fps setting: 24
- Main segments: 68
- Overlay segments: 9

## Audio reconstruction

- Lossless timeline mix: `timeline-audio-48k-stereo.flac`
- Whisper input: `timeline-whisper-16k-mono.wav`
- Source trims use CapCut's microsecond source ranges.
- Timeline placement uses CapCut's microsecond target ranges.
- Segment volume values are applied before the tracks are mixed.
- Video segments without an audio stream are represented by silence of the exact target duration.
- Each segment is padded only when source packet/sample rounding would otherwise make it shorter than CapCut's target duration.

## Whisper run

- Binary: `/opt/homebrew/bin/whisper-cli`
- Model: `/Users/taylordasch_1/.cache/whisper/ggml-base.en.bin`
- Model SHA-256: `a03779c86df3323075f5e796cb2ce5029f00ec8869eee3fdfb897afe36c6d002`
- Language: English
- Decode: beam size 5, best-of 5, word-aware splitting
- Prompt supplied with Taylor/Stylecraft/Central Texas proper nouns.
- Machine segments: 224
- Mean token probability: 0.8922
- Segments with mean token probability below 0.50: 1

## Timing uncertainty

- Clip map: exact CapCut values, displayed to the nearest millisecond (rounding uncertainty ±0.5 ms).
- 48 kHz audio render: sample-aligned; boundary uncertainty is at most one 48 kHz sample after conversion.
- 16 kHz Whisper input: sample-aligned; boundary uncertainty is at most one 16 kHz sample after conversion.
- Whisper text segment boundaries are model estimates, not edit points. Treat them as approximately ±0.5–1.5 seconds, with larger uncertainty around silence, wind, music, overlapping audio, or cut-off words.
- Proper nouns, numbers, and builder/product terms require human review before publication.
