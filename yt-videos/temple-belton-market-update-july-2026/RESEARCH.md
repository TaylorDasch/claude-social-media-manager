# Market Proof Brief — Temple and Belton, July 2026

## Executive read

The useful update is not another blanket `56% cut prices` headline. It is the relationship between listing age and visible price correction in an exact Active Residential snapshot.

After filtering the July 20 source to `City in {Temple, Belton}`, `Status = Active`, and `PropertyType = Residential`:

- **0–30 DOM:** 28 of 204 listings, or **13.7%**, had recorded a prior price cut.
- **31–60 DOM:** 84 of 185, or **45.4%**.
- **61–90 DOM:** 76 of 114, or **66.7%**.
- **91+ DOM:** 298 of 367, or **81.2%**.

This is a cross-sectional association, not proof that reaching a certain day causes a seller to cut. It does show why a relocating buyer should not use the same offer strategy on a fresh listing and a 90-day listing.

The second half of the story prevents overreach. The latest 200 qualifying Closed records had a median 50 DOM, finished at a median 99.76% of final list, and finished at a median 97.01% of original list. Of those, 103, or 51.5%, closed below final list. Much of the visible correction can happen before contract. A stale listing may support a different conversation; a red price-cut badge does not guarantee another large discount.

## Source audit and exact routing

### Primary point-in-time sources

- `/Users/taylordasch_1/market-monitor/whole-market-with-status-2026-07-20.csv` — controlling July source; 3,502 data rows / 3,503 total lines; explicit `Status` and `PropertyType`; all rows are `Residential`; 19 cities in the broad export.
- `/Users/taylordasch_1/market-monitor/05-14-2026-mls-templebelton.csv` — May continuity comparison. It lacks `Status` and `PropertyType`, so its first stable block is the best comparable inferred Active section, not an equally explicit month-to-month observation.
- Relevant July and June point-in-time exports in `/Users/taylordasch_1/market-monitor/` — continuity checks only.
- `/Users/taylordasch_1/market-monitor/temple-belton-historical-data/*.csv` — deduplicated long-run Closed history through July 17, retained as the crash/forecast guardrail.

### Source integrity

- SHA-256: `be9edd7d034c8ccd14961befe5229d60c5898fba22385a67d80086a74df478f5`.
- The downloaded source and Market Monitor copy matched.
- Broad-source status counts reconcile to 3,502 rows: Active 1,944; Closed 984; Pending 387; Active Under Contract 173; Coming Soon 14.
- No row-level field is reproduced in the public package; only aggregates are emitted.

### Exact July filters

- **Active slice:** exact `City = Temple or Belton`, `Status = Active`, `PropertyType = Residential`.
- **Closed slice:** exact `City = Temple or Belton`, `Status = Closed`, `PropertyType = Residential`, `CloseDate` from 2026-06-21 through 2026-07-20 inclusive, and `ClosePrice >= $25,000`.
- The broad source includes 19 cities. City filtering is performed after reading explicit source fields; no inferred status block is used for July.
- Every source row has `PropertyType = Residential`.

**FILMING GATE — CLEARED:** explicit `Status` and `PropertyType` fields resolve the prior status-reconstruction issue. Taylor approval and publication approval remain required.

### Files excluded from citywide owner-occupant claims

- purpose-specific rentals, multifamily/duplex, seller-financing, client-report, Salado-only, Georgetown/Round Rock, UMHB micro-radius, and similar files;
- generated `snapshots/2026-W29.json` and `outputs/public/market-pulse.json` counts and months-of-supply values;
- any row outside exact Temple/Belton city values or outside the stated Active/Closed criteria.

The generated snapshot/pulse is not used here. Its prior engine blended stale no-close-date rows from older files and could not support a reliable months-of-supply denominator. This package uses the explicit July 20 CSV fields and reproducible aggregate filters instead.

### Public-use and platform checks

- The publicly indexed August 2019 Central Texas MLS rules say MLS-based public representations should identify Central Texas MLS and the period covered: `https://www.fourriversrealtors.com/docman-documents/forms-public/524-ctxmls-rules-regulations-aug-2019/file`. Preserve the source-and-period notices below and verify any newer subscriber rule before publication if available.
- TREC treats social and electronic marketing as advertising and requires the license-holder/team name plus broker identification, with a profile/direct-link exception under stated conditions: `https://www.trec.texas.gov/article/what-you-need-know-comply-our-social-media-rules`.
- YouTube’s official title/thumbnail guidance prioritizes accuracy, clarity, brevity, and mobile legibility: `https://support.google.com/youtube/answer/12340300`.
- YouTube’s native title/thumbnail A/B test selects by watch time, not CTR alone: `https://support.google.com/youtube/answer/16391400`.

## Reproducible method

- **Cities:** exact `Temple` and `Belton` values only.
- **Current Active snapshot:** 2026-07-20.
- **Latest Closed window:** 2026-06-21 through 2026-07-20 inclusive.
- **May close window:** 2026-04-15 through 2026-05-14.
- **Price cut:** `OriginalListPrice > CurrentPrice` where both exist.
- **Final-list ratio:** `ClosePrice / ListPrice`; `CurrentPrice` on Closed rows is not used as the final-list denominator.
- **Original-list ratio:** `ClosePrice / OriginalListPrice`.
- **DOM:** median nonnegative `DOM`; the export does not contain CDOM.
- **Builder:** `SpecialListingConditions` contains `Builder`. `BuilderName` and `YearBuilt` are deliberately ignored because they can persist on resales.
- **Sale floor:** $25,000 to remove lease/non-sale records.
- **Privacy:** aggregates only. No address, agent remark, showing instruction, tenant detail, or row-level identifying field is emitted.

## Current Active scoreboard

### Temple + Belton combined

| Measure | July 20 exact Active |
|---|---:|
| Rows | 870 |
| Unique normalized addresses | 869 |
| Median ask | $299,440 |
| Median DOM | 69.5 |
| Prior price cut | 486 / 870, or 55.9% |
| Builder-identified | 222 / 870, or 25.5% |

### Current city context

| Measure | Temple | Belton |
|---|---:|---:|
| Active rows | 618 | 252 |
| Unique normalized addresses | 617 | 252 |
| Median ask | $285,000 | $349,900 |
| Median DOM | 69 | 73.5 |
| Price-cut share | 56.8% | 53.6% |

The city medians reflect different inventory mixes. Do not use the median-ask gap as a like-for-like value judgment or a city winner.

## May continuity comparison — directional, not a precise series

The July column below uses explicit source fields. The May file does not contain `Status` or `PropertyType`; its first 889-row block is the best comparable inferred Active section and is supported by prior block-continuity checks. Use the comparison as continuity evidence only, not as a precise month-to-month series.

| Measure | July exact Active | May best-comparable inferred block | Directional change |
|---|---:|---:|---:|
| Rows | 870 | 889 | -2.1% |
| Median ask | $299,440 | $309,900 | -3.4% |
| Median DOM | 69.5 | 71 | -2.1% |
| Share with a prior price cut | 55.9% | 54.1% | +1.8 percentage points |

**Meaning:** the best available continuity read shows a slightly smaller current Active count, a lower asking-price mix, slightly lower median DOM, and a modestly higher share with a prior reduction. It does not prove a same-home price change or establish a clean monthly trend.

## The hook: listing-age price-cut staircase

| Current DOM | Active rows | Previously reduced | Share reduced |
|---|---:|---:|---:|
| 0–30 days | 204 | 28 | 13.7% |
| 31–60 days | 185 | 84 | 45.4% |
| 61–90 days | 114 | 76 | 66.7% |
| 91–120 days | 99 | 80 | 80.8% |
| 121+ days | 268 | 218 | 81.3% |
| 91+ combined | 367 | 298 | 81.2% |

City-level checks preserve the same broad shape, although smaller Belton buckets vary more:

- Temple: 14.9% / 44.9% / 68.9% / 83.1% / 82.3% across the five buckets.
- Belton: 11.1% / 46.9% / 58.3% / 76.5% / 79.3%.

### Correct interpretation

- Fresh listings are far less likely to show a prior reduction.
- By days 61–90, prior reductions are common.
- After day 90, roughly four in five current listings have already reduced.
- Listing age is useful triage evidence, but no day count proves motivation, condition, value, or the next seller decision.
- This is not a longitudinal survival model; listings that sold, withdrew, or changed status are no longer in the Active snapshot.

### Buyer action

- **Fresh and well-comped:** prepare to decide; a blanket lowball based on the citywide cut share can fail.
- **61–90 DOM:** study the full price history and substitutes; visible correction is much more common in this group.
- **91+ DOM:** ask why it remains—price, condition, location, insurance, title, layout, taxes, seller constraints, or a thin buyer pool—before assuming the answer is another price cut.

## Closed market: the guardrail against a lowball story

### Latest exact Closed window

| Measure | June 21–July 20 exact Closed | May comparison sample | Read |
|---|---:|---:|---|
| Qualifying records | 200 | 187 | Different windows and mixes |
| Median closed DOM | 50 | 83 | Current sample is 33 days lower; do not say homes sold 33 days faster |
| Median close price | $278,670 | $290,000 | Mix-sensitive |
| Median close / final list | 99.76% | 100.00% | Final list remained sticky |
| Median close / original list | 97.01% | 96.17% | Correction often occurred before contract |
| Closed below final list | 103 / 200, or 51.5% | 87 / 187, or 46.5% | Frequency does not measure discount size |

Do not call close-to-list net of concessions; this export has no seller-credit field. Do not describe the median-price difference as same-home appreciation or depreciation. The correct public wording is that the latest sample’s median DOM was 33 days lower than the May sample’s 83—not that homes sold 33 days faster.

### Current city closes

| Measure | Temple | Belton |
|---|---:|---:|
| Qualifying Closed records | 143 | 57 |
| Median close | $273,000 | $304,335 |
| Median DOM | 52 | 40 |
| Median close / final list | 100.00% | 99.59% |
| Median close / original list | 96.99% | 97.01% |

The clean audience lesson is:

> Much of the visible correction can be baked into the asking-price reset before contract; the latest median closed home still finished essentially at the final MLS list-price basis.

## Long-run context through July 17

| YTD year | Sales | Median close | Median DOM | Median close / original |
|---:|---:|---:|---:|---:|
| 2016 | 1,001 | $152,500 | 84 | 98.61% |
| 2017 | 1,111 | $162,000 | 80 | 99.00% |
| 2018 | 1,129 | $175,000 | 73 | 99.99% |
| 2019 | 1,216 | $181,200 | 41 | 99.33% |
| 2020 | 1,285 | $199,900 | 44 | 99.91% |
| 2021 | 1,191 | $240,000 | 20 | 100.75% |
| 2022 | 1,218 | $310,000 | 16 | 101.78% |
| 2023 | 1,194 | $295,000 | 45.5 | 98.18% |
| 2024 | 1,058 | $283,950 | 51.5 | 97.70% |
| 2025 | 1,162 | $289,000 | 66 | 97.14% |
| 2026 | 1,152 | $285,000 | 69 | 96.30% |

Compared with the same Jan. 1–July 17 period of 2025, 2026 sales are down 0.9%, the combined median is down 1.4%, and median DOM is three days longer. The market is much slower than the 2021–2022 period, but the 2026 volume and price medians do not support a broad crash claim.

## Price bands

| Current Active band | Rows | Median DOM | Price-cut share |
|---|---:|---:|---:|
| Under $200K | 96 | 79 | 62.5% |
| $200K–$299,999 | 348 | 53.5 | 55.2% |
| $300K–$399,999 | 204 | 91.5 | 56.9% |
| $400K–$499,999 | 87 | 84 | 48.3% |
| $500K+ | 135 | 88 | 56.3% |

The strongest supporting example is Temple’s $300,000s:

- current exact Active: 133 rows, median 86 DOM, 60.9% reduced;
- latest exact Closed: 31 records, median 37 DOM, median 99.73% of original list.

That coexistence is the deeper story: stale survivors and correctly positioned winners can occupy the same price band. These are different groups, not the same homes followed from Active to Closed.

## New construction versus non-builder inventory

| Current Active measure | Builder-identified | Non-builder |
|---|---:|---:|
| Rows | 222 | 648 |
| Share of Active | 25.5% | 74.5% |
| Median ask | $319,000 | $289,900 |
| Median DOM | 110 | 64 |
| Price-cut share | 44.1% | 59.9% |

Builder stock is roughly one-quarter of the exact Active snapshot. Longer builder DOM does not prove like-for-like builder homes are cheaper or that a builder will negotiate in a specific way.

What a relocating buyer should compare:

- total ownership cost, not just posted price;
- completion and closing timing;
- taxes, HOA, and any PID/MUD or similar district exposure;
- included features and lot position;
- independent inspection rights and warranty process;
- nearby resale alternatives and future resale competition.

The May source cannot reliably identify builders, so no May-to-July builder trend is claimed.

## Three-number offer test

### 1. Relative DOM

Compare the home’s DOM with the same city, price band, property type, condition, and closest reasonable substitute set. The 60/90-day staircase is a triage signal, not a valuation.

### 2. Current versus original price

Measure how much correction has already occurred and when. A listing already reduced near supported value may have less room than its price-cut badge implies.

### 3. Substitute pace and closing behavior

Check whether close substitutes are fresh, reducing, pending, withdrawn, or closing near the final ask. Determine whether the buyer has real alternatives.

All three should point in the same direction before Taylor recommends a more aggressive price or term conversation. This is an evidence framework, not a promise about acceptance.

## Public source notices

Active graphics/copy:

`Based on information from Central Texas MLS as of July 20, 2026. Temple + Belton Residential listings with Status = Active; source export covers multiple cities and was post-filtered to Temple/Belton; DOM groups are cross-sectional.`

Closing graphics/copy:

`Based on information from Central Texas MLS for June 21, 2026 through July 20, 2026. Temple + Belton Residential listings with Status = Closed; 200 records at or above $25,000; medians; seller credits unavailable.`

May–July Active continuity graphics/copy:

`Based on information from Central Texas MLS as of May 14 and July 20, 2026. Temple + Belton; July uses Residential listings with Status = Active, while the May file lacks Status and PropertyType and uses its best-comparable first status block. Directional continuity only; changing mix.`

Closed-sample comparison graphics/copy:

`Based on information from Central Texas MLS for April 15–May 14 and June 21–July 20, 2026. Temple + Belton; n=187 and n=200; medians; different samples and mixes; seller credits unavailable. July uses Residential listings with Status = Closed.`

YTD comparison graphics/copy:

`Based on information from Central Texas MLS for Jan. 1–July 17, 2025 and Jan. 1–July 17, 2026. Temple + Belton Closed records at or above $25,000; deduplicated; medians; seller credits unavailable.`

## Claim ledger

| Claim | Evidence | Confidence | Public use |
|---|---|---|---|
| 13.7% at 0–30 DOM vs 81.2% after day 90 had reduced | Exact Active, 28/204 and 298/367 | Confirmed | Hook; use source footer |
| 55.9% of Active listings had reduced | 486 / 870 | Confirmed | Supporting scoreboard |
| 870 Active rows / 869 unique addresses | Exact July filters | Confirmed | Research/method context |
| Best-comparable count is 2.1% lower than May | 870 exact vs 889 inferred | Directional only | Label May inference every time |
| Median Active ask is 3.4% lower than May comparison | $299,440 exact vs $309,900 inferred | Directional; mix-sensitive | Supporting context only |
| Latest Closed median DOM is 33 days lower than May sample | 50 vs 83; n=200 vs n=187 | Confirmed samples; not a speed claim | Secondary tension |
| Latest median close/final was 99.76% | `ClosePrice / ListPrice`, n=200 | Confirmed | Core buyer lesson |
| Latest median close/original was 97.01% | `ClosePrice / OriginalListPrice`, n=200 | Confirmed | Core buyer lesson |
| 51.5% closed below final list | 103 / 200 | Confirmed | Guardrail; no credit data |
| Builder Active median DOM 110 vs 64 non-builder | 222 vs 648 | Confirmed | New-construction section |
| Temple $300s: 86 Active DOM vs 37 Closed DOM | Active n=133; Closed n=31 | Confirmed; different groups | Price-band example |
| Months of supply | Source cannot support a clean denominator | Unsupported | Do not calculate |
| Future city price direction | Not established | Unsupported | Do not say |
| Seller credits/net price | Field absent | Unsupported | Do not say |

## Reproduction

```bash
python3 /Users/taylordasch_1/claude-social-media-manager/yt-videos/temple-belton-market-update-july-2026/analysis/analyze_market.py
```

The analysis is read-only and should print aggregate results from the documented sources. Treat source exports as immutable.
