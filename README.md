# claude-social-media-manager

> Content OS + operational CLI for Taylor Dasch (EG Realty, Temple TX). Governance-first architecture: skills generate, CLI approves, nothing auto-posts.

## What It Does

- **Capture** ideas from anywhere (clients, comments, videos, market data) into a typed intake queue.
- **Generate** platform-specific drafts via Claude Code skills (30 production skills — TikTok, YouTube, IG Reels, LinkedIn, GMB, Newsletter, Reddit/BP, and more).
- **Approve** drafts through a compliance-gated queue. HARD violations (banned phrases, broker rule, Fort Cavazos, TikTok-investor leaks, guaranteed returns) block approval.
- **Export** approved posts as CSV (default) or JSON. Optional live push via Postiz / Ayrshare / Buffer when credentials are set. Never auto-posts by default.
- **Track** calendar + gaps + weekly mix vs target + performance ledger.
- **Enforce** brand voice — codified from `governance/QUALITY-GATES.md` + `data/voice-rubric.json` into `smm/compliance.py`.

Full architecture in `PROJECT_AUDIT.md`. Voice rules in `BRAND_VOICE.md`. Daily + weekly rhythm in `WORKFLOW.md`. Agent contract in `AGENTS.md`. Governance overrides in `governance/`.

## Install

Python 3.12+ (tested on 3.14). Stdlib only — no `pip install` required for the core CLI.

```bash
cd ~/claude-social-media-manager
python3 cli.py version
```

First run creates `data/drafts.db` (SQLite) and `exports/` automatically.

## Optional: environment variables

Copy `.env.example` and set only what you use:

```bash
cp .env.example .env
# edit .env — set POSTIZ_API_URL / POSTIZ_API_KEY only when Postiz is deployed.
```

Without `.env`, the CLI runs fully on CSV export. Scheduler push returns a graceful no-op with a clear reason.

## Quickstart

```bash
# Capture an idea
python3 cli.py intake add --source-type youtube \
  --title "Temple vs Killeen investing" \
  --audience investor \
  --body "Audience wants a quick math comparison"

# Create a platform draft (or import from skill output)
python3 cli.py draft new --platform linkedin \
  --body "Temple median is \$247K. Bell County effective tax ~2.18% …" \
  --hook "The tax rate kills lazy Temple underwriting." \
  --cta "DM for the deal analyzer."

python3 cli.py draft import output/2026-W17/gmb/investor-cash-flow-math-2026-04-20.md \
  --platform gmb

# See what's waiting for review
python3 cli.py draft list --status needs_review

# Inspect + approve
python3 cli.py draft show drft_xxx
python3 cli.py draft approve drft_xxx --note "ships Tuesday"

# Export to CSV (Meta Business Suite / Postiz / Ayrshare / Buffer upload)
python3 cli.py export approved --target csv --platform linkedin

# Mark posted after you publish
python3 cli.py draft posted drft_xxx --note "live at https://..."
```

## Commands

```
cli.py intake   add | list | show | close
cli.py draft    new | import | list | show | edit
                approve | reject | revise | scheduled | posted | history | delete
cli.py export   approved --target csv|json|postiz|ayrshare|buffer
cli.py compliance check --path FILE [--platform tiktok]
cli.py calendar week | gaps | mix
cli.py analytics template --out some.csv
cli.py version
```

Full subcommand help: `python3 cli.py <cmd> --help`.

## How the pieces fit

```
  (ideas)                  (skill outputs)
     │                            │
     ▼                            ▼
  intake (DB) ───── drafts (DB) ─── compliance.py
                         │
                         ▼
                   approval queue
                         │
                         ▼
                 approved (DB)
                         │
                         ▼
                  exports/*.csv  ──► Meta / Postiz / Ayrshare / Buffer
                                      (manual upload by default)
                         │
                         ▼
                 posted (DB)  ──►  performance-ledger.csv
                                      (manual ratings for now)
```

- **Intake / drafts / approvals** live in `data/drafts.db` (SQLite, created on first run).
- **Published content** is tracked in the existing `data/content-registry.csv` (64 rows) — the CLI reads it for `calendar gaps`.
- **Skill output files** land in `output/YYYY-WXX/…` and can be imported as drafts.
- **Performance ledger** is `data/performance-ledger.csv` (manual CRUSH/SOLID/MEH/MISS ratings for now; auto-pull planned via `/weekly-analytics-pull`).
- **Compliance** reads `data/voice-rubric.json` + hardcoded HARD gates from `QUALITY-GATES.md`.

## Known Limits

- **No auto-posting.** Hard rule; export is always a file.
- **No LLM draft generation in the CLI itself.** Generation happens via Claude Code skills in `skills/`. The CLI imports their output.
- **Performance analytics are manual** until the per-platform MCP pulls are wired into `weekly-pull.py`.
- **Scheduler integrations (Postiz/Ayrshare/Buffer) are stubs.** CSV export is the default fallback and works without any credentials. Live pushes require deploying Postiz on Railway (per `SMM-IMPROVEMENT-PLAN.md`) and setting `POSTIZ_API_URL` + `POSTIZ_API_KEY`.
- **HARD compliance can be overridden** with `--force` — but every override is logged in the `approval_events` table.

## Next Build Priorities

1. Wire `cli.py calendar week` output into an auto-rendered section of `TODO.md` (replacing or complementing `~/.hermes/scripts/smm-todo-writer.py`).
2. Live Postiz push (when Railway-deployed). `smm/integrations/postiz.py` stub is in place.
3. Auto-populate `performance-ledger.csv` from YouTube / Beehiiv / GSC / FUB MCPs — extend `scripts/weekly-pull.py`.
4. Optional: reconcile `~/.hermes/scripts/voice-check.py` with `smm/compliance.py` (DRY).

## Project Structure

```
claude-social-media-manager/
  cli.py                       ← main CLI (this file is the entrypoint)
  smm/                         ← Python package (stdlib only)
    __init__.py, db.py, models.py
    intake.py, drafts.py, approval.py
    compliance.py, calendar.py, exporters.py
    integrations/{csv_export,postiz,ayrshare,buffer}.py
  tests/test_smm.py            ← smoke + unit tests
  data/                        ← state
    drafts.db                  ← intake + drafts + approval_events (NEW)
    content-registry.csv       ← published content (existing SoT)
    performance-ledger.csv     ← analytics (existing, schema matches analytics_template.csv)
    voice-rubric.json          ← compliance source-of-truth
    hook-bank.json             ← rotating hook pool
    community-memory.db        ← engagement (existing)
  exports/                     ← CSV/JSON exports (created on first export)
  governance/                  ← QUALITY-GATES, SESSION-LOOP, MULTI-PASS, etc.
  skills/                      ← 30 production Claude Code skills
  scripts/                     ← 9 production Python scripts (freshness, dedupe, etc.)
  output/YYYY-WXX/             ← weekly skill outputs
  reference/                   ← 16 reference playbooks
  research/                    ← strategy + research docs
  templates/                   ← newsletter templates + branding
  social-media-config.json     ← full business/brand/audience/platform config (42KB)
  BRAND_VOICE.md               ← canonical voice + banned-phrase doc
  WORKFLOW.md                  ← daily + weekly rhythm
  AGENTS.md                    ← Codex-agent contract
  CLAUDE.md                    ← Claude Code instructions
  PROJECT_AUDIT.md             ← full gap analysis + build order
  SMM-IMPROVEMENT-PLAN.md      ← MCP/automation roadmap
  TODO.md                      ← auto-populated pending work
  CODEX-BACKLOG.md             ← Codex-owned Wave jobs
  analytics_template.csv       ← per-post analytics schema
  market_data.json             ← verified Temple/Bell County facts
  .env.example                 ← scheduler + DB envs
```

## Tests

```bash
cd ~/claude-social-media-manager
python3 -m unittest discover -s tests -v
```

Smoke tests live in `tests/test_smm.py` and cover: DB init, intake add/list, draft add/compliance/approve/reject/force, CSV export, compliance edge cases.
