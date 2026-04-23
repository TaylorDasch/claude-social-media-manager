# CX-02 — /keyword-audit Migration + GSC Upgrade

## Mandatory first step

Read `AGENTS.md` at the repo root, then all six files in `governance/`. Governance overrides anything below on conflict. Then read `CLAUDE.md` for voice and `CODEX-BACKLOG.md` for the full CX-02 card.

## Your goal

Replace the legacy transcript-only keyword audit in `.claude/skills/keyword-audit.md` with a governed `/keyword-audit` skill that runs in two modes: transcript-only fallback when Google Search Console (GSC) data is unavailable, and GSC-enriched mode when it is.

## Files you own on this branch

- `skills/keyword-audit/` (create this directory)
- `.claude/skills/keyword-audit.md` (legacy — migrate or mark legacy)
- `skills/content-calendar/SKILL.md` (read-only — understand how audits feed calendar; do not rewrite)
- `skills/audit/SKILL.md` (read-only — ensure you do not duplicate it)
- `reference/YOUTUBE-GROWTH-PLAYBOOK.md` (read-only)

## Files you must not touch

- Generic SEO audit scopes belong to `/audit`; stay out of them.
- Broad `/content-calendar` rewrites.
- Any file outside the list above, except governance and `AGENTS.md` for reading.

## Deliverable

A governed `skills/keyword-audit/SKILL.md` with:

1. Valid YAML frontmatter.
2. Two documented modes:
   - **transcript-only**: input is a transcript or SRT; output surfaces spoken-entity coverage, keyword density, and missing-entity flags.
   - **gsc-enriched**: when GSC access is confirmed, add striking-distance keyword analysis (positions 4–15, impressions above a configurable threshold), top-losing queries week-over-week, and page-level opportunity notes.
3. A graceful fallback path: if GSC is unavailable, the skill degrades to transcript-only mode and reports the reason clearly. Do not hallucinate GSC numbers.
4. Output written to `output/YYYY-WXX/keyword-audit/<slug>.md` using ISO week number.
5. Audit surfaces at minimum: striking-distance keywords, missing spoken entities (for video audits), page/video opportunity notes, and a 3-item next-action list.
6. Explicit statement that this skill is for keyword opportunity diagnosis and does not duplicate `/audit`'s broader page-level scoring.

## Do not duplicate /audit

Scan `skills/audit/SKILL.md` before writing. If any workflow step overlaps, defer to `/audit` and cross-reference instead of re-implementing.

## Verification target

Pick one existing transcript or SRT from `yt-videos/` (or any .srt in the repo) and generate a transcript-only-mode audit. Save the sample at `codex-jobs/samples/cx-02-sample-audit.md`. Document in the sample what the gsc-enriched mode would have added if GSC were available. Do not attempt live GSC calls.

## Stop-checklist at end of job

- **Files changed:** explicit paths.
- **Verification run:** the exact command(s) you ran, plus a short summary of the sample output.
- **Unresolved risk:** anything unclear about GSC integration that Claude should resolve before gsc-enriched mode ships.
- **Rollback path:** `git checkout main && git branch -D codex/keyword-audit`.

Do not open a PR. Leave the branch for Claude to review.
