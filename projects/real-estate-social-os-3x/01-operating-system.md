# Operating System

## North Star

Build a social distribution machine that turns Taylor Dasch with EG Realty into the most useful Temple, TX real estate signal across buyer, BSW, military, seller, and investor lanes.

The work is not measured by post count first. It is measured by:

- Qualified conversations created.
- Existing page authority strengthened.
- Search Console CTR and position opportunities amplified.
- Reusable assets created from one research pull.
- Follow-up paths captured with DM keywords, UTMs, and FUB/source notes.

## Lane Discipline

| Lane | Primary channels | Never do |
| --- | --- | --- |
| Buyer / relocator | TikTok property tours, Instagram Reels, GBP, Temple Insider, YouTube Shorts | Do not turn this into investor math. |
| BSW medical | SEO pages, GBP, YouTube, LinkedIn, Temple Insider | Do not use gatekeeper outreach assumptions. |
| Military / Fort Hood | TikTok property tours, YouTube, GBP, buyer guides | Do not use the old base name. |
| Seller | GBP, LinkedIn, Facebook, seller pages, email drafts | Do not use pressure language. |
| Investor | YouTube, BiggerPockets, LinkedIn, Investor Brief, pages | Do not put investor content on TikTok. |

## Daily Loop

1. Pull snapshot:

```bash
python3 scripts/social-os-snapshot.py --out projects/real-estate-social-os-3x/snapshots/latest.md
```

2. Pick one source asset from the command center.
3. Check dedupe in `data/content-registry.csv` and `data/hook-bank.json`.
4. Pull source proof: GSC page/query data, `market-monitor/`, source page, video, transcript, or listing facts.
5. Produce one distribution packet using `templates/source-to-social-packet.md`.
6. Run gates: no unsourced numbers, no banned Gate 1 language, CTA fit, TikTok rule, draft-only approval.
7. Log the output path and expected next action in the command center.

## Weekly Rhythm

| Day | Primary job | Output |
| --- | --- | --- |
| Monday | Demand-led calendar | One weekly plan tied to GSC pages and stale registry items. |
| Tuesday | Film buyer/relocator assets | Native TikTok tour preps, YouTube long-form capture, Short concepts. |
| Wednesday | Repurpose non-TikTok assets | LinkedIn, GBP, newsletter, community, BP, Short. |
| Thursday | Authority and lead path day | BSW, seller, and page amplification packets. |
| Friday | Scorecard and cleanup | Performance ledger, registry state, stuck pipeline decisions. |
| Saturday | Freshness and page bridge | Refresh stale market/page assets and video-to-page mapping. |
| Sunday | Planning buffer | Backlog prune, prompt refresh, next week queue. |

## Source Selection Rules

Choose the source with the strongest blend of:

- Search demand: impressions, low CTR, striking-distance position.
- Business value: likely buyer, seller, medical, military, or investor lead path.
- Production readiness: existing page, video, MLS proof, listing asset, or transcript.
- Compounding ability: can become at least 4 native assets without forcing it.
- Risk: fewer unsupported claims, cleaner compliance path, and clear approval gate.

## Minimum Packet

A real packet is not done unless it has:

- Source asset and business outcome.
- Audience lane and platform fit.
- Proof notes with dates.
- Draft package for at least one platform.
- CTA, DM keyword or link, UTM, and FUB/source note.
- SEO/GEO/AEO amplification path.
- Registry/dedupe status.
- Approval gate.

## Hard Stops

- No live social posting, scheduling, email sends, CRM writes, site edits, or paid promotion without Taylor approval.
- No investor TikTok.
- No unsourced numbers.
- No raw private MLS fields in public copy.
- No audience mixing between Living in Temple and Investing in Temple.
- No claims about rankings, rates, incentives, or performance without current proof.
