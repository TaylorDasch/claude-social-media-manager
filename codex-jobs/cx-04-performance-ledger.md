# CX-04 — Automated Performance-Ledger Population

## Mandatory first step

Read `AGENTS.md` at the repo root, then all six files in `governance/`. Governance overrides anything below on conflict. Then read `CODEX-BACKLOG.md` for the full CX-04 card.

## Your goal

Harden `scripts/weekly-pull.py` and reconcile it with `skills/weekly-analytics-pull/SKILL.md` so the weekly ledger population is safe, idempotent, and produces both a human-readable snapshot and a machine-readable raw artifact.

## Files you own on this branch

- `scripts/weekly-pull.py` (harden and reconcile with skill spec)
- `scripts/common.py` (extend only if genuinely needed — prefer existing helpers)
- `scripts/test-all.sh` (add a smoke check for the dry-run path)
- `skills/weekly-analytics-pull/SKILL.md` (reconcile scope and outputs with script behavior)
- `data/performance-ledger.csv` (the target — preserve its existing schema)

## Files you must not touch

- `weekly-retro` coaching logic.
- Manual Taylor-notes columns in the ledger beyond preserving their schema.
- Any platform API keys. If a required env var is missing, the script must warn and skip that platform — never crash, never synthesize data.

## Deliverable

1. `python3 scripts/weekly-pull.py --dry-run` succeeds with graceful warnings for any missing env vars (YouTube, Beehiiv, GSC, FUB, Google Maps). Non-zero exit only for genuine errors, not missing keys.
2. Write mode is idempotent for the same ISO week: re-running the same week appends no duplicates. Document the dedupe strategy inline.
3. Each run saves:
   - `output/YYYY-WXX/analytics-snapshot.md` — human-readable weekly summary.
   - `output/YYYY-WXX/analytics-raw.json` — machine-readable raw data for downstream scripts.
4. `skills/weekly-analytics-pull/SKILL.md` matches the script's real scope and outputs — no aspirational behavior left in the skill.
5. Rollback path is documented at the top of the script: a one-command reversion for Taylor if a bad run writes malformed rows.

## Hard rules

- The ledger is a system of record. A corrupt write is worse than a skipped write. When in doubt, abort and log.
- Do not rewrite the ledger's column schema. If you need to add columns, stage that as a separate commit with a schema-change note.
- Do not call live APIs without the caller's explicit opt-in. Default is `--dry-run`.

## Verification target

Run `python3 scripts/weekly-pull.py --dry-run` and then a second run to prove idempotency. Save both runs' console output and any generated `output/YYYY-WXX/` artifacts. Reference them in the stop-checklist.

Fixture-backed runs are fine when live keys are unavailable. If a platform has real credentials available in the environment, use them for at least one platform and note which.

## Stop-checklist at end of job

- **Files changed:** explicit paths.
- **Verification run:** two dry-run invocations; any live-platform run noted.
- **Unresolved risk:** missing-platform fallbacks, ledger schema assumptions, or anything that could cause silent data loss.
- **Rollback path:** a named one-command reversion if a live run ever produces a bad row.

Do not open a PR. Leave the branch for Claude to review.
