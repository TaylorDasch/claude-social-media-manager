# Local Shorts Factory Core

The core CLI turns a local subtitle-free master into ranked review manifests. It
does not copy the master and never imports or invokes the separately gated
publishing bridge. The canonical record is:

```text
~/claude-video/shorts-factory/jobs/<job-id>/job.json
```

`job.json` uses `shorts-job/v1`, an integer `revision`, and embedded `clips`.
Each clip is also mirrored to `clips/<clip-id>/clip.json`; `job.json` wins if a
process is interrupted between those writes.

## Runtime

`ffmpeg` and `ffprobe` are available in Taylor's normal environment. Faster
Whisper is already installed in Vega's virtualenv, so no dependency install is
needed:

```bash
cd /Users/taylordasch_1/claude-social-media-manager
/Users/taylordasch_1/dasch-command/agents/vega/clipper/.venv/bin/python \
  scripts/shorts-factory.py run /absolute/path/to/master.mp4
```

Ranking is provider-resilient: Anthropic is tried first when configured. A
missing Anthropic key or an explicit low-credit/billing response switches that
run to the stdlib OpenAI client (`OPENAI_API_KEY`, default `gpt-5.4-mini`).
Authentication and transient provider errors still fail closed.

An existing transcript avoids model transcription and is normalized into stable
word IDs:

```bash
python3 scripts/shorts-factory.py run /absolute/path/to/master.mp4 \
  --transcript-json /absolute/path/to/transcript.json
```

Useful commands:

```bash
python3 scripts/shorts-factory.py ingest /absolute/path/to/master.mp4
python3 scripts/shorts-factory.py analyze <job-id>
python3 scripts/shorts-factory.py analyze <job-id> --reuse-ranking
python3 scripts/shorts-factory.py status
python3 scripts/shorts-factory.py status <job-id> --full
python3 scripts/shorts-factory.py decide <job-id> <clip-id> decline \
  --expected-revision 3 --reason "Repeated point"
```

Approval is checksum-locked. `approve` fails until `render.path` exists; it
computes the media SHA-256, verifies any recorded checksum, and stores
`approved_sha256` plus the unchanged render `version`. Approval never publishes.

## Native vertical graphic replacements

An exact source edit may contain baked 16:9 cards that should be replaced in a
vertical delivery. Place an optional manifest at:

```text
<job-dir>/analysis/visual-replacements.json
```

The timeline is bound to the ingested master checksum, not to selected clip IDs,
so it remains valid when ranking chooses a different overlapping span:

```json
{
  "schema_version": "shorts-visual-replacements/v1",
  "source_sha256": "<master-sha256>",
  "replacements": [
    {
      "id": "annual-tax",
      "source_start_s": 223.36,
      "source_end_s": 232.46,
      "asset_path": "../../vertical-assets/annual-tax.mp4",
      "asset_sha256": "<asset-sha256>",
      "timing_mode": "hold_last"
    }
  ]
}
```

Assets must be 1080x1920, 30fps H.264 MP4 files in `yuv420p`. Ranges may touch
but may not overlap. `hold_last` extends the final asset frame when the source
range is longer than the animation. Rendering preserves source audio, applies
the graphic before burned captions, fingerprints asset checksums and timing,
and writes a `.graphics.json` QA sidecar.

## Review reminders

The dedicated macOS reminder checks every four hours and suppresses an unchanged
queue for 24 hours. It also reports failed jobs instead of silently waiting:

```bash
PYTHONPATH=scripts python3 -m shorts_factory.reminder install \
  --root /Users/taylordasch_1/claude-video/shorts-factory \
  --interval-seconds 14400
```

Rollback is explicit:

```bash
PYTHONPATH=scripts python3 -m shorts_factory.reminder uninstall
```

## Postiz draft handoff

Publishing is a separate module and never schedules or publishes. The default
command is a read-only preflight; creating a Postiz draft requires the exact
approved checksum again and an explicit switch:

```bash
PYTHONPATH=scripts python3 -m shorts_factory.publish \
  <job-id> <clip-id> \
  --platform instagram_reels \
  --approved-sha256 <64-character-approved-digest>

# Only after Taylor explicitly says go:
PYTHONPATH=scripts python3 -m shorts_factory.publish \
  <job-id> <clip-id> \
  --platform instagram_reels \
  --approved-sha256 <64-character-approved-digest> \
  --create-draft
```

The bridge uploads a frozen verified copy, writes a durable intent before any
remote mutation, uses platform-required settings, and blocks ambiguous retries.
