# Phase 1 — Anchor

**Run:** deepmode-run-260517-1620
**Date:** 2026-05-17 4:22 PM CDT
**Mission:** Flagship Living-in-Temple YouTube market-read video, May 2026
**Lane:** Living in Temple (buyer/relocator) — explicitly NOT Investing
**Length:** 10–12 minutes
**Primary audience cohorts:** BSW medical hires (residents, fellows, attendings, nurses on relocation contract), military PCS-window buyers (Fort Hood, transfers in/out, including dual-mil), general Texas-to-Temple relocators.

---

## Ground-Truth Data Pulled (MLS source of truth: ~/market-monitor/)

**Source CSV:** `05-14-2026-mls-templebelton.csv` — 3,326 rows
**MLS data age:** 3 days (within 7-day freshness window — DO NOT FLAG STALE)
**City filter:** Temple only — 2,341 rows
**Snapshot taken:** 2026-05-14
**Filming target:** week of 2026-05-19. Re-pull data 24–48hr before filming to refresh numbers.

### Headline metrics (Temple only, 05-14 snapshot)

| Metric | Value | Comp (05-08, 6 days prior) |
|---|---|---|
| Active inventory | **856** | 869 (−13 / −1.5%) |
| Sold last 30 days | **147** | 137 (+10) |
| Median list price (active) | **$286,950** | $287,500 (−$550 / −0.2%) |
| Median $/sqft (active) | **$165** | — |
| Median close price (last 30d) | **$286,990** | $285,000 (+$1,990) |
| Median DOM (last 30d sales) | **84 days** | 89 days (−5) |
| Mean DOM (last 30d sales) | **132 days** | — (skewed by long-tail) |
| Active listings with price drops | **459 / 856 = 53.6%** | 459 / 869 = 52.8% |
| Drops ≥10% off original | **86 listings** | — |
| Median price-drop amount | **$15,000 (−4.5%)** | — |
| Sale-to-original-list ratio (median, 30d) | **96.2%** | — |
| Months of supply (active ÷ 30d sales) | **~5.8 months** | 6.3 months (prior CSV) |

### 12-month sold-median trend (Temple)

| Month | Sales | Median close |
|---|---|---|
| May 2025 | 103 | $279,990 |
| Jun 2025 | 157 | $282,341 |
| Jul 2025 | 143 | $279,900 |
| Aug 2025 | 139 | $265,000 |
| Sep 2025 | 139 | $261,308 |
| Oct 2025 | 112 | $277,050 |
| Nov 2025 | 90 | $295,825 |
| Dec 2025 | 122 | $271,250 |
| Jan 2026 | 74 | $262,750 |
| Feb 2026 | 93 | $264,000 |
| Mar 2026 | 119 | $268,255 |
| Apr 2026 | 123 | $285,000 |
| May 2026 (partial) | 60 | $284,500 |

**YoY median (May'25 vs May'26 partial):** $279,990 → $284,500 = **+1.6%** — flat, NOT crashing.
**YoY volume (May'25 vs May'26 partial):** 103 → 60 (partial, 2 weeks remaining) — pace likely matches.

### Specific listings (for B-roll / verification at filming)

10%+ price-drop sample (anonymized to subdivision + sqft + year-built; will re-verify and source addresses at filming):
- Lakeaire Sec I: $1.2M → $898K (−25.2%, 2,775 sqft, YB 1999)
- Cliffs Of Canyon Creek Ph V: $1,175K → $999K (−15.0%, 5,891 sqft, YB 1994)
- Crooked Creek Sub: $865K → $750K (−13.3%, 2,351 sqft, YB 2011)
- Wildflower Country Club Ph: $1,000K → $900K (−10.0%, 3,684 sqft, YB 1994)
- Whatley Acres: $799,900 → $699,900 (−12.5%, 2,784 sqft, YB 2025 — NEW CONSTRUCTION)
- The Woods At Cedar Oaks: $795K → $699,900 (−12.0%, 3,420 sqft, YB 2005)

NOTE: $1.99M → $199.9K row at "Shady Hill" is almost certainly an MLS data-entry typo (90% drop). Exclude.

---

## Brain Query Results — Prior Taylor Position (Maintain Consistency)

Source: `Temple Real Estate Market Analysis.txt` (sim 0.570 — highest hit).

**Anchor position to maintain:**
> "The frenzy of the pandemic era has subsided, [but] appropriately priced, move-in-ready homes are still generating localized scarcity and competitive multiple-offer scenarios. Buyers who rely exclusively on heavy price-cut strategies will find themselves continually outmaneuvered by better-prepared purchasers willing to pay market value for pristine assets."

> "Highly functional, structural recalibration."

**Translation for this video:**
1. Position is NOT "crash" and NOT "boom." Frame is **"structural recalibration with two markets inside it."**
2. The 53.6% price-drop figure is real and matters — but it does NOT mean every house has a price cut available. The market splits into:
   - **Aging listings** (84-day median DOM, dropping prices) — buyer leverage IS real here
   - **Priced-right, move-in-ready, in-demand corridor** — still moves fast at or near ask
3. The viewer's job is to recognize which type they're shopping. The video's job is to give them the recognition criteria.

Prior cited figure: "Temple at 5.38 months of supply." Current calc: ~5.8 months. Use current. Acknowledge slight increase from prior public stat.

Other consistency anchors from brain:
- Living in Temple = buyer/relocator only. Never mix in investor underwriting.
- Voice: data-first, sourced, honest negatives, "honest counter" pattern in every section (see temple-caution-areas reference).
- No banned words: dream, nestled, perfect, charming, turnkey, hidden gem, paradise, oasis, stunning, gorgeous, exclusive, insider, broker.
- Identity declaration: "I'm Taylor Dasch with EG Realty" — placement varies; rule says "first 3 sentences but NOT first 15s." Use ~0:18–0:24 placement.
- Lender pipeline is the BSW workaround. Reference it only if natural to the buyer pathway question.

---

## Success Rubric — This Artifact Wins If

1. **A BSW medical hire researching Temple in May 2026 watches to minute 6 and walks away with:** (a) a concrete read on whether to act now vs wait, (b) one specific data point they can repeat to their spouse, (c) saved Taylor's contact OR clicked the description link.
2. **A military relocator with PCS window in next 90 days can answer "buy or rent" by minute 9** with specific data, not a vibes call.
3. **Every cited number ties to a specific source** (MLS pull date stamped on-screen, FBI/USDA/Bell CAD/HUD URL in description). Zero generic "the market is..." claims.
4. **Honest negatives appear by minute 4** — not stockpiled at the end. Trust signal: shows credibility, not delayed gratification.
5. **Lane discipline holds:** zero investor language (cap rate, gross yield, BRRRR, 1% rule, cash-on-cash). The word "investment" appears once max, and only in context like "your largest single financial decision," not investor strategy.
6. **First 15s is hook-only (entity declaration deferred to ~0:18–0:24).** First 3 sentences after entity declaration include identity. ONE strong visual element (not three). Single creative hook = the **two-snapshot reveal** (05-08 CSV vs 05-14 CSV side-by-side on a laptop — physical rotation toward camera).
7. **Anti-duplication clean:** no overlap with the 24 existing yt-videos. Closest neighbors checked — temple-caution-areas (corridor inspection, not market read) and bsw-residents-temple-new-construction (builder incentives, not market read). Clear separation.
8. **Description block includes** dated MLS-pull stamp, every source URL referenced on-screen, BAH calculator + builder-incentive scanner CTAs, lender pathway disclosure, license + EHO line.

## Inverse-Fail Rubric — This Artifact Embarrasses Taylor If

1. **Hyperbolizes either direction.** "Crash incoming" — wrong, gets clipped against him in a quarter. "Strong seller's market" — also wrong, ignores the 53.6% price-drop data. Crash-narrative video on Temple TX channel in May 2026 = permanent screenshot trophy.
2. **Generic macro-narrative.** "Mortgage rates are still high, demand has cooled, blah blah" — that's any AI summary. Viewer has no reason to subscribe. The video must say things only a working Temple agent could.
3. **Citing a stat that doesn't survive 30 days.** No naming a single ZIP-code average that flips with two transactions. Use ranges + the methodology, not point estimates that decay.
4. **Investor lane creep.** If "cap rate," "gross yield," "BRRRR," "cash-on-cash," "ROI," or "investment property" shows up — failure. The Investing in Temple channel exists for those terms.
5. **Banned words present** (Taylor brand voice — auto-fail).
6. **Weak CTA.** "DM me for a list" / "Reach out" / "Hit subscribe" alone = failure. CTA must be specific (BAH calculator URL, builder-incentive scanner, relocation packet, calendar link), and ideally **tied to which audience cohort the viewer is in**.
7. **First 15s violates format rule** (entity declaration in first 15s = failure of brief; identity NOT declared in first 3 sentences after the hook = also failure).
8. **Honest-negatives deferred past minute 5** — looks like a sales video. Pattern-match to the temple-caution-areas script: counter inside every section, not stockpiled.
9. **More than one strong visual creative hook.** ONE element rule. Two-snapshot laptop reveal is THE element; no second physical-prop reveal, no second "watch this" moment.
10. **Filename/folder naming violation** — must save to `temple-market-read-may-2026/` not `may-2026-market-update/` etc. Anti-duplication check requires consistent folder taxonomy.

---

## Anti-Duplication Check Against ~/claude-social-media-manager/yt-videos/

24 existing video folders reviewed. Closest semantic neighbors:

| Folder | Overlap risk | Differentiator |
|---|---|---|
| `temple-caution-areas` | LOW — corridor inspection thesis, not market read | Different job: prescriptive inspection rules vs market state |
| `bsw-residents-temple-new-construction` | LOW — builder incentives flagship | Different job: residency-cohort builder-deal scorecard vs market state |
| `warning-3-mistakes` | LOW — older (May 6), generic buyer mistakes | Different job: error catalog vs market read |
| `top-3-builders-temple` | LOW — builder roundup | Different job: builder shortlist vs market state |
| `top-3-neighborhoods-under-250k` | LOW — sub-$250K neighborhood shortlist | Different job: price-tier neighborhood guide vs market read |
| `temple-vs-round-rock` | LOW — geographic comparison | Different job: A vs B vs market state of A |
| `pcs-fort-cavazos` | LOW — military move guide | Different job: relocation logistics vs market state |

**No prior Temple-market-read video exists.** First in the lane. Clean.

---

## Phase 2 Reference Bank — Patterns to Carry Forward

Going into Phase 2, the patterns I'm pulling from:

1. **temple-caution-areas/script.md** (5/13, council-run, 50K chars)
   - Pattern: data-first, every claim has a URL or file source, "honest counter" inside each section
   - Pattern: HUD/TREC/Fair Housing compliance frame opens the video
   - Pattern: open-loop hook ("one looks worse than the data") paid off mid-script
   - Pattern: deliverable-numbered chapter list with timestamps
   - Pattern: phrases-to-avoid table on-screen — visible compliance signal

2. **bsw-residents-temple-new-construction** (5/14, reason-run)
   - Pattern: cohort-specific CTA (residency hires arriving June)
   - Pattern: builder-deal scorecard with named incentives + expiration
   - Pattern: lender pipeline disclosure (Stark Law workaround framed honestly)

3. **One external reference (best-in-class market-read pattern):** competitor agents in Austin/Round Rock who do monthly market reads. The good ones (Justin Havre format, ASU real-estate report style) anchor every claim to a dated number and reject viral-hook framing.

4. **Contrarian — what NOT to do:** generic Realtor "market update" with stock-photo B-roll, vague "the market is..." opening, and "DM me to learn more" CTA. The contrarian reference is "every Temple-area Realtor doing a Reels market update in May 2026 with no MLS source on-screen." That's the bar I'm beating.

---

## Phase 1 Output — Files Created

- `phase-1-anchor.md` (this file)

## Phase 1 Decisions Locked

1. Title-direction interpreted as a frame, not literal. Will produce 3 title options where ONE matches the brief literally, two are alternatives that may outperform.
2. ONE creative element = the two-snapshot laptop reveal (05-08 CSV vs 05-14 CSV).
3. Identity declaration at ~0:18–0:24, post-hook, in 3 sentences.
4. Length target: 10:30 (mid-range of 10–12).
5. Lender pipeline disclosure included naturally (compliance + audience-cohort signal).
6. Filming target: week of 2026-05-19; re-pull MLS data 24–48hr before camera-on; flag any number movement >3 percentage points.
7. Cohort-specific CTAs: BAH calculator (military), builder-incentive scanner (residency hires + general), relocation packet (general relocators).

Phase 1 complete. Moving to Phase 2 — Reference Deepening.
