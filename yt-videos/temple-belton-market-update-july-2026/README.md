# Temple–Belton Market Update — July 2026

Evidence-led filming package for `Living in Temple TX`.

**Status:** `READY_TO_FILM` — FILMING GATE — CLEARED; Taylor approval and publication approval still required  
**Built:** 2026-07-20  
**Data cutoff:** 2026-07-20; closed sales through 2026-07-20  
**Audience:** a buyer relocating to Temple or Belton within roughly six months  
**Decision:** whether to buy or wait, and how aggressively to structure an offer

## Recommended click package

- **Title:** `Temple & Belton Housing Market: The 60-Day Listing Test`
- **Thumbnail:** `14% vs 81%` with mandatory `0–30 DAYS` / `91+ DAYS` labels and a small `PRICE CUTS` label
- **Target runtime:** 9:00–10:00
- **Primary CTA:** Temple vs. Belton Family Decision Guide
- **Companion page:** `https://templetxhomes.net/temple-tx-market-update/`

## Core thesis

This is not one uniformly slow market. In the July 20 Active Temple/Belton Residential snapshot, 13.7% of listings at 0–30 DOM had recorded a prior price cut. That climbed to 66.7% at 61–90 DOM and 81.2% after day 90. The latest 200 Closed records had a median DOM of 50 and finished at a median 99.76% of final list, so listing age is not automatic lowball permission. The useful buyer question is: **How old is this listing relative to its true substitutes, and how much correction has already happened?**

## Start here

1. [Production bible](./PRODUCTION-BIBLE.md)
2. [Full script](./SCRIPT.md)
3. [Hook lab](./HOOK-LAB.md)
4. [Packaging lab](./PACKAGING-LAB.md)
5. [Thumbnail brief](./THUMBNAIL-BRIEF.md)
6. [Market proof brief](./RESEARCH.md)
7. [Shot list](./SHOT-LIST.md)
8. [Film-day checklist](./FILM-DAY-CHECKLIST.md)
9. [Council prompt](./council-prompt.md)
10. [Quality review](./QUALITY-REVIEW.md)
11. [Companion-page refresh brief](./COMPANION-PAGE-REFRESH-BRIEF.md)

The reproducible aggregate analysis is in [`analysis/analyze_market.py`](./analysis/analyze_market.py). It reads the source exports without modifying them and does not emit addresses, private remarks, or other row-level identifying data.

## Publishing guardrails

- Do not publish this as `Temple vs Belton`; that evergreen comparison is a separate video.
- FILMING GATE — CLEARED: the July 20 export includes explicit `Status` and `PropertyType` fields; every source row is `Residential`. The source covers 19 cities, and the package applies the exact public slice `City in {Temple, Belton}` plus `Status = Active` for Active claims.
- Treat the May comparison as continuity evidence, not a precise month-to-month series. The May file lacks `Status` and `PropertyType`, so its first stable block is the best comparable inferred Active section; the July side is exact.
- Do not call the whole market a buyer’s market or predict a crash.
- Do not turn a median into a promise for an individual home.
- Do not quote changing builder offers. Compare builder and resale inventory using stable public facts only.
- Do not display MLS addresses, private remarks, showing instructions, tenant information, or unlicensed listing photos.
- Taylor’s spoken identity is `Taylor Dasch with EG Realty`.

## Source hierarchy

1. `/Users/taylordasch_1/market-monitor/whole-market-with-status-2026-07-20.csv`
2. `/Users/taylordasch_1/market-monitor/05-14-2026-mls-templebelton.csv`
3. `/Users/taylordasch_1/market-monitor/temple-belton-historical-data/*.csv`
4. Local YouTube Studio export through 2026-07-02
5. Public YouTube page for the May update, used only for packaging continuity

No external system has been changed and nothing has been published.
