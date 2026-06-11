# Real Estate Social OS 3x

Status: DRAFT control plane. Taylor approval is required before posting, sending, scheduling, CRM writes, site edits, or paid promotion.

This project turns `claude-social-media-manager` from a content folder into a real estate social operating system for Taylor Dasch with EG Realty. The bar is not "more posts." The bar is a demand-led machine that converts one source asset into native social drafts, page authority, lead paths, and measurable follow-up.

## What Makes It 3x

Most advanced AI social projects stop at a calendar, prompt stack, and platform templates. This system adds five things they usually miss:

1. Search Console demand routing: social work amplifies pages and topics that already have impressions, position, or CTR problems.
2. MLS-backed proof: market claims come from `/Users/taylordasch_1/market-monitor/`, with dates and caveats.
3. Registry discipline: every asset has a state, parent, persona, lead magnet, CTA, and refresh path.
4. Lead attribution: every post maps to a DM keyword, UTM, FUB/source note, and next action.
5. Quality gates: TikTok buyer/relocator rule, no live posting without approval, no unsourced numbers, and no generic real estate copy.

## Core Files

- `00-evidence-map.md` — source-of-truth findings from repo inspection, GSC, MLS, and scripts.
- `01-operating-system.md` — the daily and weekly operating model.
- `02-double-usage-sprint.md` — May 21-31 sprint plan while usage is doubled.
- `03-content-portfolio.md` — source asset portfolio and channel routing.
- `04-asset-factory.md` — source-to-derivative factory and file manifest.
- `05-measurement-and-attribution.md` — UTM, FUB/source, and performance rules.
- `06-agent-command-system.md` — operator roles, prompts, and approval gates.
- `07-risk-and-rollback.md` — known risks and rollback notes.
- `command-center.md` — current command view and next actions.

## Tools Added

- `scripts/social-os-snapshot.py` generates a local command-center snapshot from the registry, output folders, and market-monitor freshness.

Run:

```bash
python3 scripts/social-os-snapshot.py --out projects/real-estate-social-os-3x/snapshots/latest.md
```

## Operating Rule

Every output is a draft until Taylor explicitly approves the real-world action. That includes social posting, scheduling, email sends, FUB/CRM updates, site edits, and ad spend.
