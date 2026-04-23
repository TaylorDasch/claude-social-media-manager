# Codex-Only Backlog

> Bounded implementation, QA, and browser-ops jobs for `claude-social-media-manager`.
> Claude stays in the strategy/governance lane. Codex owns scoped build tickets, verification, and evidence.

## Working Rules

- Use one job per worktree and one branch per job. The main workspace is already noisy, so parallel work should stay isolated.
- Respect governance first: `governance/QUALITY-GATES.md`, `governance/FACT-HANDLING.md`, `governance/SESSION-LOOP.md`, and the registry/ledger files remain the system of record.
- Codex can build, test, audit, and stage drafts. It does not publish anything live or bypass Taylor approval.
- Prefer the smallest correct diff. Each job owns a narrow write set and should avoid opportunistic refactors.
- When a job depends on missing external setup (Postiz deployment, Reddit MCP install, API keys), Codex should still build the repo-side scaffolding and leave the final auth/connect step explicit.

## Why These Jobs

- The repo already calls out the first four priorities in [SMM-IMPROVEMENT-PLAN.md](SMM-IMPROVEMENT-PLAN.md).
- Two of those "missing" skills already exist in legacy form under `.claude/`; the right move is migration plus hardening, not starting from zero.
- The existing scripts already cover scanner/audit/ledger basics, which makes Codex well-suited for incremental automation and QA closure.

## Recommended Parallel Launch

### Wave 1

1. `CX-01` `/youtube-metadata` migration + hardening
2. `CX-02` `/keyword-audit` migration + GSC upgrade
3. `CX-03` Postiz integration hardening
4. `CX-04` automated performance-ledger population

### Wave 2

5. `CX-07` scanner evidence pack
6. `CX-08` derivative reconciliation
7. `CX-05` content calendar automation

### Wave 3

8. `CX-09` pattern-miner feedback loop
9. `CX-10` embed + VideoObject queue builder
10. `CX-06` Reddit monitoring inbox

## Job Cards

### CX-01 — `/youtube-metadata` Migration + Hardening

- Status: Ready now
- Suggested branch: `codex/youtube-metadata`
- Suggested worktree: `../wt-smm-youtube-metadata`
- Why now: The improvement plan says this skill is deferred, but the repo already has a legacy `.claude/commands/youtube-metadata.md` and `.claude/skills/youtube-metadata.md`.
- Own these paths:
  - `skills/youtube-metadata/`
  - `.claude/commands/youtube-metadata.md`
  - `.claude/skills/youtube-metadata.md`
  - `reference/YOUTUBE-GROWTH-PLAYBOOK.md`
  - `data/living-in-temple-catalog.txt`
  - `data/investing-in-temple-catalog.txt`
- Deliverable: A governed `skills/youtube-metadata/SKILL.md` that matches current repo conventions and explicitly inherits governance rules.
- Acceptance:
  - Skill lives in `skills/`, not only `.claude/`
  - Dedupe check against the video catalogs is part of the workflow
  - Output path is stable: `output/YYYY-WXX/youtube/[slug]-metadata.md`
  - Entity declaration, banned-word checks, and CTA matching are explicit
  - Any legacy `.claude` command either points to the governed skill or is marked legacy
- Verification target: Generate one sample metadata package from an existing `yt-videos/` topic without touching live YouTube settings.
- Do not touch:
  - Live upload/publish flows
  - Unrelated YouTube strategy docs beyond what the skill references

### CX-02 — `/keyword-audit` Migration + GSC Upgrade

- Status: Ready now
- Suggested branch: `codex/keyword-audit`
- Suggested worktree: `../wt-smm-keyword-audit`
- Why now: The repo already has a transcript-only legacy `.claude/skills/keyword-audit.md`, while the improvement plan wants real Google Search Console data.
- Own these paths:
  - `skills/keyword-audit/`
  - `.claude/skills/keyword-audit.md`
  - `skills/content-calendar/SKILL.md`
  - `skills/audit/SKILL.md`
  - `reference/YOUTUBE-GROWTH-PLAYBOOK.md`
- Deliverable: A governed `/keyword-audit` skill that combines transcript diagnostics with live ranking opportunity checks when GSC is available.
- Acceptance:
  - Skill runs in two modes: transcript-only fallback and GSC-enriched audit
  - Output path is stable: `output/YYYY-WXX/keyword-audit/[slug].md`
  - Audit surfaces striking-distance keywords, missing spoken entities, and page/video opportunity notes
  - Quality gates are inherited explicitly
  - The new skill does not duplicate `/audit`; it stays focused on keyword opportunity diagnosis
- Verification target: Run against one existing transcript or SRT and document the fallback behavior if GSC is unavailable.
- Do not touch:
  - Broad `/content-calendar` rewrites
  - Generic SEO audits outside the keyword-audit scope

### CX-03 — Postiz Integration Hardening

- Status: Ready now for repo-side prep, blocked later on deployed Postiz URL and API key
- Suggested branch: `codex/postiz-hardening`
- Suggested worktree: `../wt-smm-postiz-hardening`
- Why now: The improvement plan names Postiz as the biggest workflow improvement, but governance still requires draft-only behavior and safe scheduling.
- Own these paths:
  - `reference/INTEGRATION-MAP.md`
  - `skills/linkedin-carousel/SKILL.md`
  - `skills/repurpose/SKILL.md`
  - `skills/community-post/SKILL.md`
  - `templates/`
  - `scripts/`
- Deliverable: A safe Postiz preflight layer that prepares schedule-ready draft payloads and validates env/config without sending anything live.
- Acceptance:
  - Repo includes a clear Postiz handoff contract: required env vars, payload shape, approval gate
  - A preflight script or template validates platform, copy length, media requirements, and schedule metadata
  - Draft/export mode is the default; publish mode is out of scope
  - LinkedIn scheduling path is documented as "ready when Postiz exists"
  - Failure states are explicit when URL or API key is missing
- Verification target: `--dry-run` or equivalent produces a Postiz-ready payload for one existing content artifact.
- Do not touch:
  - Railway deployment itself
  - Live social publishing
  - Approval rules in governance

### CX-04 — Automated Performance-Ledger Population

- Status: Ready now
- Suggested branch: `codex/performance-ledger-auto`
- Suggested worktree: `../wt-smm-performance-ledger`
- Why now: `scripts/weekly-pull.py` already exists, but the skill spec is more ambitious than the script and the repo still describes ledger updates as partly manual.
- Own these paths:
  - `scripts/weekly-pull.py`
  - `scripts/common.py`
  - `scripts/test-all.sh`
  - `skills/weekly-analytics-pull/SKILL.md`
  - `data/performance-ledger.csv`
- Deliverable: A hardened weekly pull flow that safely appends platform data, emits a weekly snapshot, and avoids duplicate ledger rows.
- Acceptance:
  - `python3 scripts/weekly-pull.py --dry-run` succeeds with missing-key graceful warnings
  - Write mode is idempotent for the same week or has a documented dedupe strategy
  - The job saves `output/YYYY-WXX/analytics-snapshot.md` and `output/YYYY-WXX/analytics-raw.json`
  - Script and skill agree on scope and outputs
  - Rollback path is documented
- Verification target: Dry-run plus a fixture-backed or partial live run that shows at least one platform path working cleanly.
- Do not touch:
  - `weekly-retro` coaching logic
  - Manual Taylor notes columns beyond preserving schema

### CX-05 — Content Calendar Automation from System State

- Status: Ready after CX-02 and CX-04 are mostly stable
- Suggested branch: `codex/content-calendar-automation`
- Suggested worktree: `../wt-smm-content-calendar`
- Why now: `social-media-config.json` says content calendar automation is only partially closed, and the current skill still relies too heavily on generation from scratch.
- Own these paths:
  - `skills/content-calendar/SKILL.md`
  - `reference/INTEGRATION-MAP.md`
  - `social-media-config.json`
  - `data/content-registry.csv`
  - `data/performance-ledger.csv`
- Deliverable: A calendar workflow that prioritizes registry gaps, filming queue, performance winners, and router market data before inventing new topics.
- Acceptance:
  - Skill explicitly checks registry gaps and recent pillar rotation
  - Skill can consume output from the weekly analytics pull and keyword audit
  - Monday-calendar behavior in `reference/INTEGRATION-MAP.md` is no longer aspirational only
  - Output still lands in `output/YYYY-WXX/content-calendar.md`
- Verification target: Generate a calendar for the next week and show which items came from registry gaps versus live opportunities.
- Do not touch:
  - Publishing automations
  - Non-calendar skills except where a dependency call needs to be referenced

### CX-06 — Reddit Monitoring Inbox

- Status: Partially blocked on Reddit MCP install, but repo-side design can start now
- Suggested branch: `codex/reddit-monitoring`
- Suggested worktree: `../wt-smm-reddit-monitoring`
- Why now: The improvement plan says `/reddit-bp` needs monitoring and thread discovery, not just post drafting.
- Own these paths:
  - `skills/reddit-bp/SKILL.md`
  - `reports/`
  - `data/`
  - `social-media-config.json`
- Deliverable: A lightweight monitoring/report flow that turns Reddit signal discovery into a reviewable inbox instead of ad hoc browsing.
- Acceptance:
  - Monitoring and drafting are distinct modes
  - Output is saved to a stable local report path
  - Fallback behavior is documented when Reddit MCP is not installed
  - Governance rules for soft-sell / no self-promo remain explicit
- Verification target: Produce one sample "opportunities inbox" report from either MCP results or a fixture/stubbed example.
- Do not touch:
  - Live Reddit posting
  - BP/Reddit voice rules except to inherit them

### CX-07 — Scanner Evidence Pack

- Status: Ready now
- Suggested branch: `codex/scanner-evidence-pack`
- Suggested worktree: `../wt-smm-scanner-evidence`
- Why now: The repo already has scanner scripts, but Codex is strongest when it can hand back evidence, not just console output.
- Own these paths:
  - `scripts/freshness-scanner-v2.py`
  - `scripts/output-integrity-check.py`
  - `scripts/dedupe-checker.py`
  - `reports/`
- Deliverable: Machine-readable and human-readable outputs for the existing audit scripts so weekly checks can feed review queues and automations.
- Acceptance:
  - Each scanner can emit a stable JSON or markdown report artifact
  - Severity and category are explicit enough for triage
  - Existing CLI behavior does not regress
  - Reports are easy to diff week-over-week
- Verification target: Run all three scanners and confirm both terminal output and saved artifacts are useful.
- Do not touch:
  - Core scanning logic unless needed for output stability
  - Content generation skills

### CX-08 — Registry Derivative Reconciliation

- Status: Ready now
- Suggested branch: `codex/derivative-reconciliation`
- Suggested worktree: `../wt-smm-derivative-reconciliation`
- Why now: The session loop and TODO both call out missing blog/short/reel/embed follow-through after video publication.
- Own these paths:
  - `scripts/next-best-action.py`
  - `VIDEO-TO-PAGE-MAP.md`
  - `data/content-registry.csv`
  - `reports/`
- Deliverable: A reconciliation pass that identifies published videos missing expected downstream derivatives and turns that into a prioritized queue.
- Acceptance:
  - Published videos missing blog or short-form derivatives are surfaced explicitly
  - Queue output references `content_id` and expected next action
  - Existing state-machine language is preserved
  - Read-only mode is available
- Verification target: Produce a queue against current registry data without mutating registry rows by default.
- Do not touch:
  - The actual derivative content
  - External page repos

### CX-09 — Pattern-Miner Feedback Loop into Planning

- Status: Ready after CX-04 has reliable weekly data
- Suggested branch: `codex/pattern-miner-feedback`
- Suggested worktree: `../wt-smm-pattern-feedback`
- Why now: `scripts/pattern-miner.py` exists, but its output is not yet clearly wired into planning decisions.
- Own these paths:
  - `scripts/pattern-miner.py`
  - `skills/weekly-scorecard/SKILL.md`
  - `skills/content-calendar/SKILL.md`
  - `data/performance-ledger.csv`
- Deliverable: A lightweight feedback artifact that turns ledger patterns into concrete "double down / stop doing / test next" recommendations.
- Acceptance:
  - Pattern miner outputs actionable grouped findings, not just raw aggregates
  - `/weekly-scorecard` and/or `/content-calendar` can reference that artifact
  - Missing Taylor ratings degrade gracefully instead of breaking the flow
- Verification target: Run pattern mining on current ledger data and produce a markdown brief with next-week implications.
- Do not touch:
  - Coaching tone in `weekly-retro`
  - Registry write paths unless strictly necessary

### CX-10 — Video Embed + VideoObject Queue Builder

- Status: Ready now
- Suggested branch: `codex/embed-queue-builder`
- Suggested worktree: `../wt-smm-embed-queue`
- Why now: Missing embeds and missing VideoObject/schema checks are explicitly called out in TODO and match Codex's page-audit lane.
- Own these paths:
  - `VIDEO-TO-PAGE-MAP.md`
  - `scripts/`
  - `reports/`
  - `output/audits/`
- Deliverable: A queue/report generator that compares the map, registry state, and audit outputs to show which pages need embeds or schema work next.
- Acceptance:
  - Report separates "page missing", "embed missing", and "schema likely missing"
  - Tier priority from the map is preserved
  - External page repos are referenced, not edited, from this project
  - Output is easy to hand off to a page-build worktree later
- Verification target: Generate a ranked report for current Tier 1 and Tier 3 items.
- Do not touch:
  - The page HTML in other repos during this ticket
  - Publishing workflows

## Suggested Owner Split

- Claude:
  - Strategy, governance changes, approval rules, voice doctrine, final go/no-go
- Codex:
  - Skill migration, script hardening, test coverage, browser verification, evidence packs, queue generation

## Immediate Next Move

If launching workers today, open four worktrees for `CX-01` through `CX-04` only. They are the cleanest mix of already-scoped repo work, existing partial assets, and visible leverage in the current docs.
