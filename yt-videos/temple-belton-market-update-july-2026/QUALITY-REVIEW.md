# Quality Review

## Verdict

**PASS — 97/100 projected.** The exact July source, buyer thesis, opening, script, production plan, and derivative strategy are internally coherent. Package status is `READY_TO_FILM`.

**FILMING GATE — CLEARED:** the controlling July 20 CSV includes explicit `Status` and `PropertyType`; all 3,502 source rows are Residential, and public Active claims use an exact Temple/Belton + Active post-filter. Taylor approval and separate publication approval are still required.

## Evidence gate resolution

The controlling source is:

`/Users/taylordasch_1/market-monitor/whole-market-with-status-2026-07-20.csv`

- 3,502 data rows / 3,503 total lines.
- SHA-256: `be9edd7d034c8ccd14961befe5229d60c5898fba22385a67d80086a74df478f5`.
- Download copy and Market Monitor copy matched.
- All `PropertyType` values are `Residential`.
- Broad-source status counts: Active 1,944; Closed 984; Pending 387; Active Under Contract 173; Coming Soon 14.
- Broad source covers 19 cities.
- Active public slice: exact Temple/Belton + `Status = Active` + Residential.
- Closed public slice: exact Temple/Belton + `Status = Closed` + Residential + June 21–July 20, 2026 + `ClosePrice >= $25,000`.

The May comparison remains intentionally weaker. Its CSV lacks `Status` and `PropertyType`, so the first stable 889-row block is the best comparable inferred Active section and continuity evidence only—not a precise month-to-month series.

## Final click and opening system

- **Title:** `Temple & Belton Housing Market: The 60-Day Listing Test`
- **Thumbnail:** `14% vs 81%`, mandatory `0–30 DAYS` and `91+ DAYS` endpoint labels, small `PRICE CUTS`
- **Click contract:** explain what listing age changes about the buyer’s investigation, not promise an automatic offer or discount.
- **Exact opening:**

> Only about one in seven active Temple and Belton listings in the 0-to-30-day group showed a prior price cut in my July snapshot. In the 61-to-90-day group, it was two in three; after day 90, four in five. I’m Taylor Dasch with EG Realty. If you’re relocating here, listing age tells me when to investigate harder—not when to automatically offer less. I’ll show you the three numbers I check before an offer.

The thumbnail result is spoken by about 0:17, identity is sentence three, and the buyer consequence resolves before the answer-first section.

## Hard failures found and fixed

1. **Inferred July status:** the older source omitted `Status` and `PropertyType`. The July 20 controlling source now carries both fields, all rows are Residential, and filtering is exact.
2. **Stale Active denominator:** the exact slice is 870 rows / 869 unique normalized addresses, replacing the older inferred count.
3. **Stale staircase:** the exact buckets are 28/204 (13.7%), 84/185 (45.4%), 76/114 (66.7%), and 298/367 (81.2%) for 91+ DOM.
4. **Ambiguous endpoint label:** `91+ DAYS` now matches the exact DOM >= 91 bucket while spoken copy remains `after day 90`.
5. **Longitudinal implication:** the thumbnail remains `vs`, and every chart labels the staircase as cross-sectional.
6. **May overprecision:** all Active comparisons now label May as the best comparable inferred first block and continuity evidence, not a precise monthly series.
7. **Unsupported speed language:** the approved wording is `the latest sample’s median DOM was 33 days lower than the May sample’s 83`; no universal market-speed conclusion is drawn.
8. **Final-list denominator:** `ClosePrice / ListPrice` now produces the exact 99.76% median; 103 of 200 records, or 51.5%, closed below final list.
9. **Builder denominator:** exact Active builder counts are 222/870 (25.5%), with median DOM 110 versus 64 for non-builder inventory.
10. **Public attribution:** Active, current Closed, and YTD graphics each carry Central Texas MLS plus the applicable snapshot/window notice.
11. **Comparison-period attribution:** May–July Active and April/May-versus-June/July Closed graphics now identify both periods, sample differences, and the May status limitation.
12. **Sample-trend wording:** the public chapter now says `The 83 vs 50 closing-sample guardrail`, avoiding a claim that the whole market sped up.

## Claim ledger

| Public claim | Formula/source | Public caveat | Confidence |
|---|---|---|---|
| 870 Active rows / 869 unique addresses | Exact July Temple/Belton + Active + Residential filter | Point-in-time snapshot | Confirmed |
| 0–30 DOM: 13.7% reduced | 28 / 204 | Cross-sectional Active group | Confirmed |
| 31–60 DOM: 45.4% reduced | 84 / 185 | Cross-sectional Active group | Confirmed |
| 61–90 DOM: 66.7% reduced | 76 / 114 | Cross-sectional Active group | Confirmed |
| 91+ DOM: 81.2% reduced | 298 / 367 | Cross-sectional; no causal countdown | Confirmed |
| Active share reduced: 55.9% | 486 / 870 | Prior reduction, not promised future concession | Confirmed |
| Best-comparable count 2.1% lower than May | 870 exact vs 889 inferred | May lacks Status/PropertyType; continuity evidence only | Directional |
| Active median ask 3.4% lower than May comparison | $299,440 exact vs $309,900 inferred | Mix-sensitive; not same-home depreciation | Directional |
| Active median DOM 2.1% lower than May comparison | 69.5 exact vs 71 inferred | Mix-sensitive; not a precise monthly series | Directional |
| Reduction share +1.8 points vs May comparison | 55.9% exact vs 54.1% inferred | May limitation as above | Directional |
| Latest Closed median DOM 50 vs May sample 83 | June 21–July 20, n=200; April 15–May 14, n=187 | Different mixes; current sample median is 33 days lower | Confirmed samples |
| 99.76% final-list / 97.01% original-list | Latest 200 qualifying Closed records | MLS list-price basis; seller credits absent | Confirmed |
| 51.5% closed below final list | 103 / 200 | Frequency does not measure discount size | Confirmed |
| Temple $300Ks: 86 Active DOM / 37 Closed DOM | Active n=133; Closed n=31 | Different groups, not the same homes | Confirmed |
| Temple $300Ks: 60.9% Active reduced / 99.73% Closed-original ratio | 81/133; median ratio across n=31 | No acceptance promise | Confirmed |
| Builder-identified share 25.5% | 222 / 870 | Current exact Active snapshot only | Confirmed |
| Builder/non-builder Active median DOM 110 / 64 | n=222 / 648 | Not a guaranteed concession or causal result | Confirmed |
| 2026 YTD sales -0.9%, median -1.4%, DOM +3 days | Deduplicated Jan. 1–July 17 history versus 2025 | Medians and changing mix; no crash forecast | Confirmed historical series |

## Script decisions

| Section | Decision | Reason |
|---|---|---|
| Exact hook | KEEP after exact-source revision | Strongest proprietary insight and immediate buyer consequence |
| Answer-first rule | KEEP | Prevents viewers from treating age as value |
| Full staircase | KEEP, compressed | Shows the missing middle step without implying causation |
| May comparison | KEEP with explicit limitation | Useful continuity context; July exact, May inferred |
| Closed-DOM guardrail | KEEP | Prevents blanket lowball interpretation |
| Price-cut example | KEEP | Makes original versus final list understandable |
| Temple $300Ks | KEEP | Best concrete proof that stale survivors and aligned winners coexist |
| New construction | KEEP | Material at 25.5% of exact Active inventory; no time-sensitive promotion |
| Three-number test | KEEP | Core practical buyer value |
| Buy now or wait | KEEP | Separates fixed and flexible relocation timing without forecasting |
| Method limitation | KEEP late | Necessary trust layer without slowing the opening |
| CTA | KEEP | Gives one operational next step and preserves the `when/how → where` handoff |

## Scores

| Dimension | Score |
|---|---:|
| Evidence and numerical analysis | 98 |
| Click package | 95 |
| First 30 seconds | 96 |
| Retention architecture | 94 |
| Buyer usefulness | 97 |
| Relocation specificity | 96 |
| Compliance and privacy | 97 |
| Conversion fit | 93 |
| Production feasibility | 96 |
| **Overall** | **97** |

## Public source notices

Active:

`Based on information from Central Texas MLS as of July 20, 2026. Temple + Belton Residential listings with Status = Active; source export covers multiple cities and was post-filtered to Temple/Belton; DOM groups are cross-sectional.`

Current Closed:

`Based on information from Central Texas MLS for June 21, 2026 through July 20, 2026. Temple + Belton Residential listings with Status = Closed; 200 records at or above $25,000; medians; seller credits unavailable.`

May–July Active continuity:

`Based on information from Central Texas MLS as of May 14 and July 20, 2026. Temple + Belton; July uses Residential listings with Status = Active, while the May file lacks Status and PropertyType and uses its best-comparable first status block. Directional continuity only; changing mix.`

Closed-sample comparison:

`Based on information from Central Texas MLS for April 15–May 14 and June 21–July 20, 2026. Temple + Belton; n=187 and n=200; medians; different samples and mixes; seller credits unavailable. July uses Residential listings with Status = Closed.`

YTD comparison:

`Based on information from Central Texas MLS for Jan. 1–July 17, 2025 and Jan. 1–July 17, 2026. Temple + Belton Closed records at or above $25,000; deduplicated; medians; seller credits unavailable.`

## Remaining release gates

- [x] FILMING GATE — CLEARED from explicit July 20 fields and exact Temple/Belton filters.
- [ ] Taylor approves the title/thumbnail pair and the exact plus safety hooks.
- [ ] Refresh the point-in-time source and all dated claims if filming is delayed beyond the freshness window.
- [ ] Taylor’s public social profiles make `Taylor Dasch` and `EG Realty` readily noticeable wherever profile-level identity is relied upon.
- [ ] Verify whether Central Texas MLS has issued a newer subscriber/public-representation rule than the publicly indexed August 2019 document; preserve at least the current source-and-period notices.
- [ ] Refresh the stale companion page before adding the July charts link to the live description.
- [ ] Add the public video ID, final chapters, end screen, and VideoObject schema after the video exists.
- [ ] Give the separate Temple-versus-Belton upload an adequate launch window before this update publishes.
- [ ] Obtain Taylor’s explicit publication approval before upload or release.

No live site, upload, message, external system, or publication was changed.
