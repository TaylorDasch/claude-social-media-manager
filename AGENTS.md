# AGENTS.md — claude-social-media-manager

> This file instructs any coding agent (Codex, Copilot, other LLM CLIs) working in this repo.
> Claude Code reads `CLAUDE.md`; everything below applies to agents that read `AGENTS.md`.
> If a rule in this file conflicts with a job card in `CODEX-BACKLOG.md`, this file wins.

## Mission (Codex Owner Split)

- **Claude** owns: strategy, governance changes, approval rules, voice doctrine, final go/no-go.
- **Codex** owns: skill migration, script hardening, test coverage, browser verification, evidence packs, queue generation.

Codex does not publish anything live, does not bypass Taylor approval, does not write investor content to TikTok outputs, and does not commit secrets.

---

## MUST READ BEFORE WRITING CODE

Load these six governance files before any edit. They override your instinct.

1. `governance/QUALITY-GATES.md` — Banned words (HARD gate), entity declaration, data rules, CTA fit, schema
2. `governance/FACT-HANDLING.md` — Source provenance, confidence levels, conflict resolution
3. `governance/SESSION-LOOP.md` — Default operating procedure for every session
4. `governance/DEFINITION-OF-DONE.md` — When each content type is "done"
5. `governance/MULTI-PASS-SYSTEM.md` — 5-pass architecture (Strategist → Producer → Validator → Integrator → Optimizer)
6. `governance/WORKFLOW-STATE-MACHINE.md` — Content lifecycle states and transitions

If a skill's `SKILL.md` contradicts any file above, governance wins.

Also load `CLAUDE.md` (repo root) for voice, platform rules, and automation triggers.

---

## Systems of Record — never rewrite schemas

- `data/content-registry.csv`
- `data/performance-ledger.csv`
- `data/hook-bank.json`
- `data/living-in-temple-catalog.txt`
- `data/investing-in-temple-catalog.txt`

You may append rows, update state fields, or add columns only if the job card explicitly allows it.

---

## Hard prohibitions (no exceptions)

- No investor content on TikTok outputs. TikTok = buyers/relocators only.
- No `send_email` or `send_message`. Always `create_draft`. Taylor sends manually.
- No live API calls without a `--live` flag. Default mode is dry-run or draft.
- No banned words (see QUALITY-GATES.md Gate 1). HARD gate — output is blocked if violated.
- No "Fort Cavazos." Always "Fort Hood."
- No commits of `.env`, API keys, or `~/shared-keys.env`.
- No broad refactors. Stay inside the job card's "Own these paths" scope.
- No IDX widgets or `[afx_search_page]` shortcodes in generated HTML.
- No duplicate auto-posts across subreddits (Reddit Responsible Builder Policy).

---

## File and output conventions

| Kind | Location |
|------|----------|
| New skills | `skills/<slug>/SKILL.md` (the `.claude/skills/` folder is legacy — don't add there) |
| Python scripts | `scripts/` — inherit helpers from `scripts/common.py` |
| Weekly outputs | `output/YYYY-WXX/<category>/<slug>.md` (ISO week number) |
| Scanner/audit reports | `reports/<scanner-name>-YYYY-MM-DD.{json,md}` |
| Research notes | `research/` |

New `SKILL.md` files must have valid YAML frontmatter (`name`, `description`, optional `trigger`) and must explicitly reference which governance gates they inherit.

---

## Required stop-checklist on every ship turn

Every turn that changes state (writes files, creates branches, installs packages) ends with:

- **Files changed:** explicit paths, no hand-waving
- **Verification run:** commands executed + key output
- **Unresolved risk:** what could still break
- **Rollback path:** one command

Diagnostic / read-only turns skip this block.

---

## Quality hierarchy — trade-off order when you can't have all five

1. Data accuracy (never compromise — wrong numbers erode everything)
2. Voice authenticity (analyst, not salesperson — see `CLAUDE.md` and `reference/`)
3. Completeness (incomplete pipelines leak value at every gap)
4. Timeliness (fresh beats perfect — ship and iterate)
5. Volume (last priority — one CRUSH asset beats five MEH assets)

---

## Voice rules (summary — full list in `CLAUDE.md`)

- Taylor Dasch with EG Realty — analyst voice, data-first, honest about negatives.
- Entity declaration: "Taylor Dasch with EG Realty" in first 3 sentences of any public-facing asset.
- Pillar rotation: never 2 of the same pillar in a row.
- Hook formula: `[Specific number or contradiction] + [Who this is for] + [Delayed payoff]`.
- 7-second rule for video: visual or audio change every 7 seconds.
- Key stats to cite where relevant: $27M+ volume, 100+ transactions, 3-year BP Featured Agent, 76502 Power Zip.

---

## When you are unsure

Ask Taylor (through the job's review channel) before:

- Modifying governance files
- Renaming or deleting an existing skill
- Changing `social-media-config.json` schema
- Adding or removing columns in systems-of-record CSVs
- Touching files outside your job card's "Own these paths" list

Default to reading more and writing less.
