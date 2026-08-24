# Generative AI Search Baseline + YouTube Packaging Test

**Captured:** 2026-08-23 CT  
**Properties:** `sc-domain:templetxhomes.net` and Living In Temple, TX | Taylor Dasch  
**Change boundary:** Analytics read-only. The YouTube test changes only the title variants on one older video; its thumbnail, description, cards, and end screen stay fixed.

## 1. Google Search generative AI baseline

Google Search Console's beta **Generative AI features** report is available for `templetxhomes.net`.

- Date range: 2026-05-22 through 2026-08-21
- Total generative-AI impressions: **17K** (Google's rounded display)
- Pages represented: **178**
- Last update when captured: **6 hours ago**

### Top pages in the generative AI report

| Rank | Page | AI impressions |
|---:|---|---:|
| 1 | `/data-center-impact/` | 1,912 |
| 2 | `/temple-vs-waco/` | 1,268 |
| 3 | `/best-neighborhoods-temple-tx/` | 1,261 |
| 4 | `/is-temple-tx-safe/` | 1,218 |
| 5 | `/centex/` | 1,193 |
| 6 | `/neighborhoods/` | 1,046 |
| 7 | `/investing/temple-tx-market-report/` | 985 |
| 8 | `/fort-hood-bah-calculator/` | 773 |
| 9 | `/stylecraft/` | 741 |
| 10 | `/top-5-neighborhoods/` | 700 |

The top ten account for **11,097 displayed impressions**, roughly **65%** of the rounded 17K total. Treat that percentage as directional because Google rounds the account total.

### Standard Search cross-check for the same dates

| Page | Clicks | Search impressions | CTR | Avg. position |
|---|---:|---:|---:|---:|
| `/data-center-impact/` | 189 | 14,004 | 1.35% | 7.2 |
| `/best-neighborhoods-temple-tx/` | 36 | 2,065 | 1.74% | 10.0 |
| `/is-temple-tx-safe/` | 36 | 3,922 | 0.92% | 7.7 |
| `/temple-vs-waco/` | 27 | 5,614 | 0.48% | 7.4 |
| `/fort-hood-bah-calculator/` | 23 | 8,762 | 0.26% | 8.2 |
| `/investing/temple-tx-market-report/` | 23 | 5,515 | 0.42% | 6.9 |
| `/stylecraft/` | 50 | 5,137 | 0.97% | 9.0 |
| `/neighborhoods/` | 16 | 2,839 | 0.56% | 8.8 |

### Decision

1. **Protect `/data-center-impact/`.** It leads both the AI report and standard clicks. Refresh its dated facts before adding another broad data-center page.
2. **Fix click packaging before adding more URLs** for `/temple-vs-waco/`, the BAH calculator, the market report, and `/neighborhoods/`. Each has meaningful AI exposure and a standard-search CTR below 0.60%.
3. **Treat AI impressions as reach, not leads.** The report does not provide query or conversion attribution. Lead-capture and UTM reporting still have to prove business value.

## 2. YouTube title test

### Candidate

- Video: `cQzNXV9Y7NM`
- Current title: **Hillside Village Temple TX: New Construction with the LOWEST Tax Rate in Town**
- Published: 2026-04-17
- Eligibility check: public, 7:54 long-form, and not made for kids
- Public views at selection: **153**
- Why this video: an internal 2026-04-23 review flagged its click layer after it ran at 11 views/day during its first six days, below channel long-form benchmarks. By 2026-08-23, it had added only 85 more public views. The same review found the channel's proven long-form comparators at **44.85%** and **32.49%** average percentage viewed, so this is a packaging test on a stalled asset, not a format rewrite.
- Why not the current breakout: `q2qWEGJ-z54` has **14,646** public views and is still the channel's clear long-form winner. Leave the winner alone while testing on the stalled video.

### Hypothesis

**Observation:** The current title is data-first but does not name the buyer. It also makes an absolute `LOWEST Tax Rate in Town` claim that is not supported by a current authoritative comparison set in the local evidence reviewed. The channel's earlier directional review found audience-named packaging stronger than a data-only title, while explicitly noting the sample was small.

**Hypothesis:** If the title names the buyer or frames the video as practical decision support, qualified watch time will improve because the viewer can identify the video's job before clicking.

### Variants

Keep the current thumbnail unchanged so the title angle is the only variable.

| Variant | Title | Angle |
|---|---|---|
| A — descriptive baseline | Hillside Village Temple TX: New Construction Community Tour | Claim-safe topic match |
| B | Temple TX New Construction for First-Time Buyers: Hillside Village | Audience relevance |
| C | Hillside Village Temple TX Tour: What Buyers Need to Know | Decision support |

### Measurement and decision rule

- Primary metric: YouTube's native **watch-time share** for title testing.
- Diagnostics: impressions, CTR, average view duration, and average percentage viewed.
- Test window: let YouTube run the native test to its own conclusion; do not call a winner from the first few days.
- Winner rule: accept a title only when YouTube reports a winner. If the result is inconclusive, keep variant A and schedule a thumbnail-only test next.
- Guardrails: no tax-rate comparison or superlative, current price, incentive, or guaranteed savings in a variant; no concurrent title/thumbnail experiment on this video; no change to the 2026-08-25 DR Horton release.

### Launch status

**LAUNCHED — 2026-08-23 at approximately 18:09 CT.** In YouTube Studio, the prior completed test was replaced, **Title only** was selected, A/B/C above were entered and visually re-read from the live controls, and **Set test** was clicked. The modal closed immediately after the action, which is Studio's launch behavior. The thumbnail, description, cards, and end screen were not changed. Studio's vidIQ-injected accessibility layer prevented a second clean status read after reload, so the first follow-up should confirm the report shows the new three-title test as running; do not recreate it unless Studio shows no active test.

### Prior test preserved before replacement

Studio showed one completed **thumbnail-only** test on this video. It ran from 2026-04-23 09:56 to 2026-05-07 10:46, received 43 views during the test period, and ended with **not enough impressions to declare a winner**. YouTube requires deleting that finished test record before a new test can be created; these decision-relevant results were recorded here first.

## Sources and provenance

- Google Search Console Generative AI features report, live authenticated UI, captured 2026-08-23.
- [`gsc-generative-ai-ui-snapshot-2026-08-23.json`](./gsc-generative-ai-ui-snapshot-2026-08-23.json) preserves the transcribed beta UI values and explicitly records that no screenshot/API export was available.
- [`gsc-standard-search-pages-2026-05-22-to-2026-08-21.json`](./gsc-standard-search-pages-2026-05-22-to-2026-08-21.json) is the authenticated Search Analytics export for the same dates (top 100 pages).
- YouTube Data API v3 public channel/video data, captured 2026-08-23.
- [YouTube Help: A/B test titles & thumbnails](https://support.google.com/youtube/answer/16391400) for eligibility, setup, concurrent testing, watch-time-share evaluation, and the up-to-two-week test window.
- `claude-video/reviews/2026-04-23-batch-pattern-last-10.md` for the earlier Studio-derived retention and packaging diagnosis.
