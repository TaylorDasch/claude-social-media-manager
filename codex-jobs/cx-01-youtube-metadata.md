# CX-01 — /youtube-metadata Migration + Hardening

## Mandatory first step

Read `AGENTS.md` at the repo root, then read all six files in `governance/`. If any instruction below conflicts with governance, governance wins. Then read `CLAUDE.md` for voice rules and `CODEX-BACKLOG.md` for the full CX-01 card.

## Your goal

Migrate the legacy YouTube metadata skill from `.claude/skills/` into the governed `skills/` layout, then harden it so it ships consistent metadata packages for existing videos in `yt-videos/` without touching live YouTube.

## Files you own on this branch

- `skills/youtube-metadata/` (create this directory)
- `.claude/commands/youtube-metadata.md` (legacy — migrate or mark legacy)
- `.claude/skills/youtube-metadata.md` (legacy — migrate or mark legacy)
- `reference/YOUTUBE-GROWTH-PLAYBOOK.md` (read-only reference; do not rewrite)
- `data/living-in-temple-catalog.txt` (read-only — for dedupe checks)
- `data/investing-in-temple-catalog.txt` (read-only — for dedupe checks)

## Files you must not touch

- Any file outside the list above, except `AGENTS.md` and `governance/` for reading.
- Live YouTube upload/publish flows (none exist in repo, but do not add any).
- Unrelated YouTube strategy docs.

## Deliverable

A governed `skills/youtube-metadata/SKILL.md` with:

1. Valid YAML frontmatter: `name`, `description`, `trigger` keywords.
2. Explicit inheritance statement referencing `governance/QUALITY-GATES.md` (banned words Gate 1, entity declaration Gate 2, pillar rotation Gate 12), `governance/FACT-HANDLING.md`, and `governance/DEFINITION-OF-DONE.md`.
3. A deterministic workflow:
   - Read the target video's transcript or brief from `yt-videos/<topic>/`.
   - Dedupe-check the working title and tags against `data/living-in-temple-catalog.txt` and `data/investing-in-temple-catalog.txt`.
   - Produce: title ≤60 chars, description (7-section structure from `reference/YOUTUBE-GROWTH-PLAYBOOK.md` if it specifies one), tag list, pinned-comment draft, end-card CTA line, thumbnail-brief handoff note.
   - Write output to `output/YYYY-WXX/youtube/<slug>-metadata.md` using ISO week number.
4. Channel-aware branching: Living in Temple (relocators) vs Investing in Temple (investors). Never mix audiences in one metadata package.
5. Entity declaration: "Taylor Dasch with EG Realty" surfaces in the first 3 sentences of the description.
6. Banned-word preflight: before emitting output, scan the generated text against the QUALITY-GATES.md Gate 1 banned list and fail closed if any match.

## Legacy disposition

Either migrate the content of `.claude/skills/youtube-metadata.md` and `.claude/commands/youtube-metadata.md` into the new skill, or replace their bodies with a one-line pointer: `> Legacy. Superseded by skills/youtube-metadata/SKILL.md.` Do not delete the legacy files; Taylor may have external references.

## Verification target

Pick one existing topic under `yt-videos/` that has a transcript or brief. Generate a sample metadata package for it end-to-end. Save the sample output inside `codex-jobs/samples/cx-01-sample-metadata.md` so Claude can review it. Do not run any live YouTube API calls.

## Stop-checklist at end of job

Close the turn with:

- **Files changed:** explicit paths (every create / modify / delete).
- **Verification run:** the exact command(s) you used to produce the sample, plus key banned-word-scan output showing no violations.
- **Unresolved risk:** anything that could break or that reviewers should watch for.
- **Rollback path:** the one command that undoes the branch (typically `git checkout main && git branch -D codex/youtube-metadata`).

Do not open a PR. Leave the branch for Claude to review.
