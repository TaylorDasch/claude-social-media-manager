# Evidence Map

This project was built from local repo inspection, Godmode routing, Search Console, MLS files, and existing SMM governance.

## Mission Routing

- Primary workstream: Social / Repurposing / Platform Content.
- Secondary workstream: Agentic AI / Dashboard / Automation.
- Required skills used: `godmode`, `taylor-social-distribution`, `social`, and the local `/claude-social-media-manager` skills.
- Godmode route score: social-content primary, agentic-systems secondary.
- Native Godmode MCP tools were not exposed as Codex tools, so the local Godmode server was called through JSON-RPC from the shell.

## Source Files Read

- `/Users/taylordasch_1/AGENTS.md`
- `/Users/taylordasch_1/CLAUDE.md`
- `/Users/taylordasch_1/plugins/godmode/commands/godmode.md`
- `/Users/taylordasch_1/claude-social-media-manager/CLAUDE.md`
- `/Users/taylordasch_1/claude-social-media-manager/AGENTS.md`
- `/Users/taylordasch_1/claude-social-media-manager/governance/QUALITY-GATES.md`
- `/Users/taylordasch_1/claude-social-media-manager/governance/FACT-HANDLING.md`
- `/Users/taylordasch_1/claude-social-media-manager/governance/SESSION-LOOP.md`
- `/Users/taylordasch_1/claude-social-media-manager/governance/DEFINITION-OF-DONE.md`
- `/Users/taylordasch_1/claude-social-media-manager/governance/MULTI-PASS-SYSTEM.md`
- `/Users/taylordasch_1/claude-social-media-manager/governance/WORKFLOW-STATE-MACHINE.md`
- `/Users/taylordasch_1/claude-social-media-manager/social-media-config.json`
- `/Users/taylordasch_1/claude-social-media-manager/data/content-registry.csv`
- `/Users/taylordasch_1/claude-social-media-manager/data/hook-bank.json`
- `/Users/taylordasch_1/claude-social-media-manager/scripts/next-best-action.py`
- `/Users/taylordasch_1/claude-social-media-manager/scripts/output-integrity-check.py`

## Repo Health Findings

- The repo already had a dirty worktree before this build.
- Existing modified files include `CLAUDE.md`, `governance/QUALITY-GATES.md`, multiple `reference/` files, and `data/weekly-brief.json`.
- Existing deleted or moved `yt-videos/` assets are present in git status.
- This build is additive. It does not modify existing governance, registry, reference files, or deleted video workspaces.

## Local Script Findings

`python3 scripts/next-best-action.py --json` surfaced:

- 8 high-priority stuck items at score `8.0`, including Buy and Hold Spreadsheet Walkthrough, Physician Loan Temple TX, Temple vs Waco Investing, Top 3 Luxury Neighborhoods Temple, and Deal of the Week 2 assets.
- 2 refresh needs: Market Shifting Fast February Update Temple TX and Whats Really Happening to Temple TX Home Prices Jan 2026, both 20 days overdue.
- Current week gaps included 3 TikTok drafts, 3 GMB posts, 2 community posts, 1 long-form YouTube video, 1 Short, 1 blog, 1 newsletter, 1 BiggerPockets engagement item, and 1 AEO audit.

`python3 scripts/output-integrity-check.py --week 2026-W21 --gates` found:

- Week 21 output itself had no issues.
- Registry and prep surfaces had 59 total issues, including invalid `QUEUED` states, published videos missing related page links, one orphaned Physician Loan Temple TX file reference, and many incomplete video prep folders.

## Search Console Evidence

Date range: February 20, 2026 through May 20, 2026. Site: `sc-domain:templetxhomes.net`.

Top page opportunities by impressions:

| Page | Clicks | Impressions | CTR | Avg position | Social job |
| --- | ---: | ---: | ---: | ---: | --- |
| `/data-center-impact/` | 71 | 7,654 | 0.93% | 7.5 | Turn into a social proof cluster and CTR rescue series. |
| `/investing/temple-tx-market-report/` | 8 | 3,151 | 0.25% | 6.7 | Investor channel only; not TikTok. |
| `/neighborhoods/` | 9 | 1,434 | 0.63% | 13.6 | Buyer/relocator clips and GBP posts. |
| `/temple-vs-waco/` | 11 | 1,427 | 0.77% | 7.9 | LinkedIn, YouTube Short, newsletter comparison. |
| `/temple-tx-market-update/` | 6 | 894 | 0.67% | 5.7 | Refresh and distribute fresh market-read snippets. |
| `/hoa-rental-restrictions-temple-belton-tx/` | 12 | 881 | 1.36% | 7.4 | Investor newsletter and LinkedIn carousel. |
| `/sellers/is-now-the-right-time-to-sell/` | 9 | 830 | 1.08% | 6.2 | Seller authority posts and GBP expertise draft. |
| `/communities/the-groves-at-lakewood-ranch/` | 9 | 815 | 1.10% | 10.1 | Neighborhood video/social bridge. |
| `/baylor-scott-white-relocation/` | 8 | 763 | 1.05% | 7.1 | BSW medical relocation series. |
| `/stylecraft/` | 5 | 698 | 0.72% | 9.0 | Builder comparison social pack. |
| `/arnold-design-build/` | 5 | 666 | 0.75% | 20.6 | Builder proof/social refresh candidate. |

## Market-Monitor Evidence

Source root: `/Users/taylordasch_1/market-monitor/`.

Fresh files detected:

- `new-construction-mls-data.csv`, modified May 19, 2026.
- `05-14-2026-mls-templebelton.csv`, modified May 14, 2026.
- `05-08-26-update.csv`, modified May 8, 2026.

Structured snapshot examples from the Godmode local server:

| Source file | Market slice | Active rows | Sold rows | Median active | Median sold | Median DOM | Caveat |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| `new-construction-mls-data.csv` | Temple | 216 | 28 | $304,550 | $309,400 | 104 | Rows filtered to CloseDate within 30 days when CloseDate is present. |
| `05-14-2026-mls-templebelton.csv` | Temple | 859 | 54 | $285,900 | $299,950 | 60 | Rows filtered to CloseDate within 30 days when CloseDate is present. |

Public-facing content must use aggregated stats, cite the file/date, and avoid raw private MLS fields.
