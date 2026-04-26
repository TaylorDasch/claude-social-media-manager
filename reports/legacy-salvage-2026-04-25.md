# Legacy Salvage — 2026-04-25

## Included

- New operational CLI and package:
  - `cli.py`
  - `smm/` excluding `__pycache__`
  - `tests/` excluding `__pycache__`
- New repo docs and config:
  - `README.md`
  - `PROJECT_AUDIT.md`
  - `WORKFLOW.md`
  - `BRAND_VOICE.md`
  - `.env.example`
  - `analytics_template.csv`
  - `market_data.json`
- New content planning artifacts:
  - `yt-videos/new-construction-pillar-honest-guide/`
  - `yt-videos/new-construction-vertical/`
  - `yt-videos/temple-map-tour/PRE-PRODUCTION-PACKAGE.md`
  - `yt-videos/temple-map-tour/RECORDING-SCRIPT.md`
  - `yt-videos/temple-map-tour/temple-map-tour-v2.html`
  - `yt-videos/temple-map-tour/temple-map-tour-v3.html`
  - `yt-videos/temple-map-tour/temple-map-tour-v3-resume.html`
- New/updated thumbnail assets:
  - `thumbnails/assets/expressions/smiling*.png`
  - `thumbnails/assets/expressions/arms-crossed*.png`
  - `thumbnails/assets/expressions/pointing-right*.png`
  - `thumbnails/assets/expressions/shocked*.png`
- Audit note:
  - `reports/skill-descriptions-audit-2026-04-24.md`

## Sanitized During Salvage

- Replaced embedded Mapbox token strings in:
  - `yt-videos/temple-map-tour/temple-map-tour-v2.html`
  - `yt-videos/temple-map-tour/temple-map-tour-v3.html`
  - `yt-videos/temple-map-tour/temple-map-tour-v3-resume.html`

All three now use `MAPBOX_PUBLIC_TOKEN`.

## Intentionally Skipped

- Runtime state and local-only artifacts:
  - `data/drafts.db`
  - `data/.claude-flow/`
  - `data/engagement-queue-state.json`
- Generated reports and daily outputs:
  - `reports/daily-health/2026-04-21.md` through `2026-04-25.md`
  - `output/film-today/2026-04-24.md`
  - `output/film-today/2026-04-25.md`
  - `output/2026-W17/scorecard.md`
- Raw media, transcripts, and backups:
  - `yt-videos/temple-map-tour/audio/`
  - `yt-videos/temple-map-tour/0424(2)/`
  - `yt-videos/temple-map-tour/temple-map-tour.html.bak-20260424-211933`
- Broad deletions of the legacy repo content were not carried forward.
  The salvage branch is additive and reviewable against clean `main`.

## Verification

- `python3 -m unittest discover -s tests -v`
  - Result: `Ran 32 tests ... OK`

## Follow-up

- If the new CLI/app is the intended repo direction, the next step is to review `salvage/legacy-delta` against `main` and decide whether to merge all or only selected parts.
