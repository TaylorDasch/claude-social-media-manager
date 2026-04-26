# PROJECT_AUDIT.md — Social Media Manager

> Audit date: 2026-04-24
> Auditor: Claude Opus 4.7 (Swarm Mode — lead architect)
> Repo: `~/claude-social-media-manager/` (standalone since 2026-04-23, commit `e1ede90`)
> Scope: Inspect current state, identify gaps vs. requested CLI-first SMM spec, propose build order, and ship the glue layer that makes the existing system operable from the terminal.

---

## 1. Current Architecture Summary

The repo is **not** a fresh social-media CLI project. It is a mature **Content OS** with a governance-first architecture. Main layers:

| Layer | What Lives Here | State |
|---|---|---|
| **Governance** | `governance/` — QUALITY-GATES.md, WORKFLOW-STATE-MACHINE.md, FACT-HANDLING.md, SESSION-LOOP.md, DEFINITION-OF-DONE.md, MULTI-PASS-SYSTEM.md, scoring-rules.json | Mature |
| **Skills** | `skills/` — 30 SKILL.md-driven generators (tiktok-script, yt-video, gmb-post, instagram-reel, reddit-bp, newsletter, repurpose, voice-guardian, etc.) | Mature, but inconsistent frontmatter |
| **Systems of record** | `data/content-registry.csv` (64 rows, 21 cols), `performance-ledger.csv` (header-only), `hook-bank.json`, `voice-rubric.json`, `community-memory.db` (SQLite: interactions + handles) | CSV registry live; performance ledger empty; DB has 5 interactions |
| **Scripts** | `scripts/` — freshness-scanner(.py/v2), output-integrity-check, dedupe-checker, next-best-action, pattern-miner, weekly-pull, bsw-relocation-guide, common | All 5 core scripts verified working per SMM-IMPROVEMENT-PLAN (2026-04-13) |
| **Config** | `social-media-config.json` (42KB) — business, brand, audiences, platforms, content pillars, hook bank, performance, schedule, techStack, gaps | Mature; schema `social-media-config-v1` |
| **Reference** | `reference/` — 16 MD playbooks (data vault, filming style, lead-magnet matrix, schema library, etc.) | Mature |
| **Output** | `output/YYYY-WXX/<category>/<slug>.md` | Actively populated (W13–W17) |
| **Auto-TODO** | `TODO.md` auto-populated by `~/.hermes/scripts/smm-todo-writer.py` as new files land in `output/` | Working |
| **Agent contract** | `AGENTS.md` — Codex-owned jobs + hard prohibitions | Shipped 2026-04-23 |

**Content lifecycle today** (observed, not documented as a single diagram):

```
Idea → Skill invocation (via Claude Code /skill-name) → output/YYYY-WXX/<slug>.md
       → Auto-added to TODO.md by hermes writer
       → Taylor reviews in TODO.md
       → Taylor manually posts / schedules / publishes
       → Registry row created/updated manually (content-registry.csv)
       → Performance logged manually (performance-ledger.csv) — rarely done
```

There is **no typed intake → draft → approval queue** between skill generation and the registry. TODO.md serves as the approval queue, but it is plain markdown, not a DB, and nothing enforces status transitions.

---

## 2. What Works Now

- Governance enforcement (16 quality gates, banned-word list, entity declaration) — documented; voice-check script uses `voice-rubric.json`.
- Content registry as source of truth — 64 content items tracked with pillar/persona/platform/lifecycle state.
- All five production scripts verified running (SMM-IMPROVEMENT-PLAN 2026-04-13).
- 30 skills covering TikTok, YouTube, Instagram Reels, GMB, LinkedIn, Reddit, BiggerPockets, Newsletter, Community posts, Reply drafting, Engagement queue, Weekly retros, Transcript-to-blog, Repurpose.
- MCP wiring live for YouTube / Beehiiv / Canva / GSC / Google Maps / RSS / FUB / Playwright (per SMM-IMPROVEMENT-PLAN checkboxes).
- Community engagement tracked in SQLite (`community-memory.db`) with interactions + handles.
- News-hijack pipeline live (`hijack-queue.json` — 301KB, active).
- Output/TODO auto-sync working via `~/.hermes/scripts/smm-todo-writer.py`.
- Voice rubric is rich and platform-specific (TikTok-buyers-only, ads-BSW+military-only, etc.).

## 3. What Is Broken or Incomplete

**Against the requested spec:**

| Gap | Severity | Notes |
|---|---|---|
| No unified CLI (`cli.py`) | High | Every action goes through Claude Code skills; nothing is terminal-scriptable |
| No typed intake/drafts/approvals DB | High | TODO.md + content-registry.csv cover different lifecycle stages |
| No `BRAND_VOICE.md` | High | Voice lives in `voice-rubric.json` + CLAUDE.md + governance; spec asks for a consolidated MD |
| No `README.md` at repo root | Medium | First-touch discoverability is weak |
| No `WORKFLOW.md` | Medium | Daily/weekly rhythm is split across SESSION-LOOP.md + TODO.md auto-sections |
| No `market_data.json` (spec schema) | Medium | Data exists in `social-media-config.json` + `reference/TEMPLE-TX-DATA-VAULT.md`, but not in the single-file format the generators/compliance checkers want |
| No `analytics_template.csv` (spec schema) | Low | `performance-ledger.csv` has a similar schema but misses lead-attribution fields |
| No `.env.example` | Medium | Scheduler creds (Postiz/Ayrshare/Buffer) are documented in SMM-IMPROVEMENT-PLAN but not scaffolded |
| No scheduler integration layer | Medium | Spec requires abstraction with CSV-export fallback |
| No compliance filter as importable Python module | Medium | Rules live in QUALITY-GATES.md (human-readable only); voice-check.py exists but in `~/.hermes/scripts/`, not this repo |
| Limited automated tests | High | Only `scripts/test-all.sh`; no `tests/` directory; Python scripts have no unit tests |
| Inconsistent SKILL.md frontmatter | Low | Many skills have blank `description:` in YAML (grep showed 15+ blank lines) |
| `performance-ledger.csv` empty | Low | Header only; blocker on analytics feedback loop |

**Not broken, but worth flagging (meta-findings):**

- The existing system is **content-production optimized**, not **operations-optimized**. Skills produce output files beautifully; the operational glue between "file exists" and "posted to platforms" is manual TODO.md.
- Community-memory.db is the only SQLite usage; the system otherwise leans on CSV + JSON. That's fine, but adding a `drafts.db` is consistent with existing patterns.
- Scripts in `~/.hermes/scripts/` vs. `scripts/` are split (Taylor's security policy: Hermes scripts live in ~/.hermes). This repo's CLI must NOT migrate those — just call them where useful.

## 4. Highest-Leverage Next Improvements

Ordered by ROI (business impact per hour of build):

1. **Unified CLI (`cli.py`)** — single terminal entrypoint that makes intake/draft/approve/export/gaps/calendar/compliance scriptable. Unblocks everything else. Ships this session.
2. **Typed drafts DB (`data/drafts.db`)** — SQLite with intake + drafts + approvals tables. Replaces TODO.md as the approval queue's source of truth (TODO.md stays as human-readable view).
3. **Compliance module (`smm/compliance.py`)** — codified QUALITY-GATES.md rules. Every draft passes through this before `status='approved'` is allowed. Run before any export.
4. **CSV export as scheduler fallback** — approved drafts become one `exports/YYYY-MM-DD-approved-posts.csv` that can be uploaded to Meta Business Suite, Postiz, Ayrshare, or Buffer manually. No API creds needed.
5. **`market_data.json`** — consolidated, verified facts with `needs_verification` flags. Generators prefer this over inventing numbers.
6. **Docs consolidation** — BRAND_VOICE.md + WORKFLOW.md + README.md — discoverability + onboarding.
7. **Smoke tests** — `tests/test_smm.py`. Prove CLI works before marking anything done.

Deferred (existing system already covers, or needs external creds):
- Postiz/Ayrshare live API integrations (keys not set; CSV export is MVP).
- Performance ledger auto-population (depends on analytics_template + per-platform MCP pulls; stub the schema, defer the pull).
- Auto-publishing (never default per AGENTS.md hard prohibition).

## 5. Risk Areas

| Risk | Mitigation |
|---|---|
| Duplicate state between `drafts.db`, `TODO.md`, `content-registry.csv` | Keep drafts.db as the authority for pre-publish state; content-registry.csv is post-publish authority; TODO.md becomes a human view rendered from drafts.db |
| Schema drift on `content-registry.csv` | AGENTS.md already prohibits schema changes without a job card — honor this. CLI reads, appends; never alters columns |
| Voice rules split across `voice-rubric.json` + `QUALITY-GATES.md` + `CLAUDE.md` | `BRAND_VOICE.md` consolidates the human-readable view; `compliance.py` reads `voice-rubric.json` + hardcoded gates from QUALITY-GATES.md. Rubric stays canonical |
| Banned-word false positives (e.g., "luxury" in luxury-homes pages is allowed; "dream" in "daydream"?) | Scan is substring+wordboundary; voice-rubric.json banned_phrases kept explicit; compliance returns per-rule violations with line context |
| TikTok-investor content leak | `compliance.check(platform="tiktok", text=...)` hard-fails if text contains investor keywords (DSCR, cap rate, cash-on-cash, rental comp) — mirrors Gate 14 |
| Fort Cavazos slip | Hard-fail on any occurrence (Gate 1 — banned) |
| Email/send drift | CLI never ships a send command. Export = write CSV/file. Posting is Taylor's explicit action |
| Secrets leak | `.env.example` only; `.env` is gitignored; compliance.py never logs raw env values |
| Hook: reading files while repo has uncommitted changes | CLI writes only to `data/drafts.db` + `exports/` + new doc files. It does NOT modify `content-registry.csv`, `social-media-config.json`, skills/, or governance/ |

## 6. Recommended Build Order

Phase 1 (this session):
1. Write `PROJECT_AUDIT.md` (this file). ✅
2. Scaffold `smm/` Python package + `cli.py`.
3. Build `smm/db.py` (sqlite schema for intake + drafts + approvals).
4. Build `smm/intake.py`, `smm/drafts.py`, `smm/approval.py`.
5. Build `smm/compliance.py` from QUALITY-GATES + voice-rubric.
6. Build `smm/exporters.py` + `smm/integrations/csv_export.py` + stubs for Postiz/Ayrshare/Buffer.
7. Write `BRAND_VOICE.md`, `WORKFLOW.md`, `README.md`, `.env.example`, `market_data.json`, `analytics_template.csv`.
8. Write smoke tests in `tests/`.
9. Run tests + smoke-test CLI end-to-end.

Phase 2 (next session, not in scope today):
- Wire `drafts.db` view into an auto-regenerated section of TODO.md (replacing the manual `hermes/smm-todo-writer.py` section, or complementing it).
- Live Postiz MCP test (requires deploy + key).
- Auto-populate `performance-ledger.csv` from YouTube/Beehiiv/GSC/FUB MCPs.
- Optional: migrate voice-check.py from `~/.hermes/scripts/` into `smm/compliance.py` or vice versa.

Phase 3 (later):
- Performance-driven content weighting (the "learned exemplars" loop).
- Lead-attribution dashboard.
- Cross-project triggers (TC deal-close → social package auto-queue).

## 7. Required Environment Variables

`.env.example` scaffolded at repo root. Required only when you wire actual integrations:

```env
# Scheduler integrations (all optional — CSV export is default)
POSTIZ_API_URL=
POSTIZ_API_KEY=
AYRSHARE_API_KEY=
BUFFER_ACCESS_TOKEN=

# Timezone + approval policy
DEFAULT_TIMEZONE=America/Chicago
APPROVAL_REQUIRED=true

# DB location (defaults to data/drafts.db)
SMM_DB_PATH=

# External systems (already set via ~/shared-keys.env; listed for awareness only)
# FUB_API_KEY, BEEHIIV_API_KEY, YOUTUBE_API_KEY etc. — do NOT duplicate here
```

## 8. Manual Setup Taylor Needs

**Nothing blocking.** The MVP ships on stdlib + local SQLite. After it's verified:

- (Optional) Install `python-dotenv` if you want `.env` auto-loading: `pip install python-dotenv`. Without it, export variables manually in the shell.
- (Optional) When Postiz deploys on Railway, drop `POSTIZ_API_URL` + `POSTIZ_API_KEY` into `~/shared-keys.env` and the integration fires.
- (Optional) When Ayrshare/Buffer tokens are available, same pattern.

## 9. What This Session Will Build

Concrete output:

- `smm/` Python package (db, models, intake, drafts, approval, compliance, calendar, exporters, integrations/{csv,postiz,ayrshare,buffer})
- `cli.py` (argparse-based single entrypoint)
- `data/drafts.db` (SQLite, created on first run)
- `exports/` (directory, created on first export)
- `tests/test_smm.py` (smoke + unit tests)
- `PROJECT_AUDIT.md` (this file)
- `BRAND_VOICE.md` (consolidated)
- `WORKFLOW.md` (daily + weekly rhythm)
- `README.md` (discoverability + command reference)
- `.env.example`
- `market_data.json` (verified facts + needs-verification flags)
- `analytics_template.csv` (schema matching spec)

What this session will **not** build:

- Auto-posting (hard prohibition per AGENTS.md).
- LLM-driven draft generation (skills already handle this; CLI calls skills or accepts imported skill output).
- MCP wiring for scheduler APIs (deferred until Postiz deploys).
- New skill files (spec requires building the operational layer; generators already exist).
- Migration of `~/.hermes/scripts/` tooling (Taylor's security policy: those live in Hermes).

## 10. Honest Limits

- I cannot test scheduler API pushes (no creds set).
- I cannot backfill `performance-ledger.csv` with real numbers (requires per-platform MCP pulls the user hasn't asked for this session).
- I will not modify `content-registry.csv`, `social-media-config.json`, governance files, or existing skills. Per AGENTS.md this requires a job card.
- Compliance rules I codify are a subset of QUALITY-GATES.md. Anything ambiguous (entity declaration in first 3 sentences, data density 3+ points per piece) will surface as SOFT warnings rather than HARD blocks unless I can unambiguously detect them.
- The CLI is a local-first operations layer. Content *generation* still happens via Claude Code skills — the CLI imports their output or accepts manual body text.

---

## Stop checklist (this audit — read-only)

- **Files changed:** `PROJECT_AUDIT.md` (new).
- **Verification run:** N/A (this is a diagnostic doc).
- **Unresolved risk:** None from this step.
- **Rollback path:** `rm PROJECT_AUDIT.md`.

Next turn: scaffold `smm/` package + `cli.py` and wire the DB.
