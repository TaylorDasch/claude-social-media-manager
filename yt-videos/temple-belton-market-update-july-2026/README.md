# Temple–Belton Market Update — August 2026 Desk Refresh

Evidence-led filming package for `Living in Temple TX`.

**Status:** `READY_TO_FILM` — August desk packet verified; Taylor approval and publication approval still required

**Built:** 2026-07-20; desk refresh completed 2026-08-06

**Data cutoff:** 2026-08-05; current Closed window through 2026-08-05

**Audience:** a buyer relocating to Temple or Belton within roughly six months
**Decision:** whether to buy or wait, and how aggressively to structure an offer

## Recommended click package

- **Title:** `Temple & Belton Housing Market: The 60-Day Listing Test`
- **Thumbnail:** `14% vs 80%` with mandatory `0–30 DAYS` / `91+ DAYS` labels and a small `PRICE CUTS` label
- **Target runtime:** 5:30–6:15
- **Primary CTA:** Temple vs. Belton Family Decision Guide
- **Companion page:** `https://templetxhomes.net/temple-tx-market-update/`

## Core thesis

This is not one uniformly slow market. In the August 5 Active Temple/Belton Residential snapshot, 13.7% of listing records at 0–30 DOM had recorded a prior price cut. That climbed to 66.0% at 61–90 DOM and 79.8% after day 90. The latest 168 qualifying Closed records finished at a median 99.48% of final list, so listing age is not automatic lowball permission. The useful buyer question is: **How old is this listing relative to the homes it actually competes with, and how much correction has already happened?**

## Start here

1. [Current desk-film packet](./DESK-FILM-PACKET-2026-08-06.md) — controlling document for this week
2. [Taylor ground-truth note](./GROUND-TRUTH-TAYLOR-TAKE-2026-08-06.md)
3. [Production bible](./PRODUCTION-BIBLE.md) — deeper July foundation; dated claims are superseded by the desk packet
4. [Full July script](./SCRIPT.md) — long version; do not film its dated numbers without refreshing them
5. [Hook lab](./HOOK-LAB.md)
6. [Packaging lab](./PACKAGING-LAB.md)
7. [Thumbnail brief](./THUMBNAIL-BRIEF.md)
8. [Market proof brief](./RESEARCH.md)
9. [Shot list](./SHOT-LIST.md)
10. [Film-day checklist](./FILM-DAY-CHECKLIST.md)
11. [Council prompt](./council-prompt.md)
12. [Quality review](./QUALITY-REVIEW.md)
13. [Companion-page refresh brief](./COMPANION-PAGE-REFRESH-BRIEF.md)

The August aggregate analysis is in [`analysis/analyze_august_desk.py`](./analysis/analyze_august_desk.py). It reuses the reviewed July calculation functions, reads the source exports without modifying them, and emits aggregates only. The original July analysis remains in [`analysis/analyze_market.py`](./analysis/analyze_market.py).

## Publishing guardrails

- Do not publish this as `Temple vs Belton`; that evergreen comparison is a separate video.
- FILMING GATE — CLEARED: the August 5 export includes exact Temple/Belton city values plus explicit `Status` and `PropertyType`; all 3,250 source rows are `Residential`.
- The current six-minute desk version omits the older May comparison, builder split, and YTD chart to reduce edit time and avoid unnecessary method exposition.
- Do not call the whole market a buyer’s market or predict a crash.
- Do not turn a median into a promise for an individual home.
- Do not display MLS addresses, private remarks, showing instructions, tenant information, or unlicensed listing photos.
- Taylor’s comments about photography, settling cracks, and roof age are labeled firsthand showing observations, not MLS-measured causes.
- Taylor’s spoken identity is `Taylor Dasch with EG Realty`.

## Source hierarchy

1. `/Users/taylordasch_1/market-monitor/temple-belton-0-365-2026-08-05.csv`
2. `/Users/taylordasch_1/market-monitor/temple-belton-historical-data/*.csv`
3. The reviewed July package in this folder, used for structure and packaging continuity

No external system has been changed and nothing has been published.
