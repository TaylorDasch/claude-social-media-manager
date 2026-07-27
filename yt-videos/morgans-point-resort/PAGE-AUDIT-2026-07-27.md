# templetxhomes.net/morgans-point-resort/ — Live Page Audit
**Scraped:** 2026-07-27 · Page published 2026-06-18, last modified 2026-07-13 · HTTP 200
**Why this matters:** the video's job is to reclaim this page (~position 18.7, 712 impressions/90d).
Shipping a July-data video at a May-data page creates a visible contradiction on Taylor's own property.

---

## 🚨 P1 — FIX BEFORE ANYTHING ELSE

### 1. The page publicly displays Taylor's local filesystem path — twice

Live on the public page, in two places:

> "Data verified **May 2026** · MLS pull of 40 sold + 12 active listings from
> `/Users/taylordasch_1/market-monitor/05-14-2026-mls-templebelton.csv` · Taylor Dasch, EG Realty"

> "Source: Direct MLS pull from `/Users/taylordasch_1/market-monitor/05-14-2026-mls-templebelton.csv`."

This exposes the OS username and internal directory structure, and to any technical reader it reads as
unedited AI output pasted straight to production. It also undercuts the page's central credibility claim
at the exact moment it's making it.

**Fix:** replace both with `Source: Central Texas MLS (CTXMLS), pulled May 14, 2026.`

### 2. Fair-housing exposure in the FAQ

> **"Is Morgan's Point Resort safe?"** → *"Yes. Crime is very low — it's a small community with strong
> full-time and retiree population."*

Answering a safety question with a crime characterization plus a population descriptor is squarely in
steering territory, and "safe" is on Taylor's own banned list. This is live right now.

**Fix:** remove the Q entirely, or answer with sources not characterizations — "Crime statistics are
published by the Morgan's Point Resort Police Department and the Texas DPS Uniform Crime Reports. I don't
characterize neighborhoods; pull the current numbers and visit at the hours you'd actually be there."

---

## ⚠️ P2 — DATA CONFLICT WITH THE NEW VIDEO

The page's numbers are a **May 14, 2026** pull. The video runs on **July 20, 2026**. They disagree, and the
page's own framing ("40 sold + 12 active") uses a different filter than the video's 29-row town filter.

| Metric | Page (May 14) | Video (July 20) |
|---|---|---|
| Active listings | 12 | 15 |
| Median sold / close | $249,500 | $220,000 |
| Median DOM | 62 | 93 (closed) |
| Sold-to-list | 95.6% (of original) | ~91% of original |
| Price range | $160K–$825K | $205K–$869K (active) |
| Median year built | 1998 (sold) | 1979 (active) / 2000 (closed) |

**These are not reconcilable as-is** — different pull dates, different cohorts, different filters. Either
refresh the page to the July 20 pull when the video ships, or clearly scope each block ("May 14 sold cohort,
n=40" vs "July 20 active snapshot, n=15"). Do not leave two undated conflicting medians on the same domain.

## ⚠️ P3 — WATER-TIER PRICING IS ASSERTED WITHOUT A VISIBLE SOURCE

The page publishes per-tier medians — Tier 1 lakefront "~$211/sqft median," Tier 3 off-water "~$177/sqft
median," and a "~15% premium" conclusion — but the July export contains **no waterfront/water-access/dock
field at all** (ground truth §F). If those tiers were hand-classified from a May dataset, the page never
says so.

This is the same provenance defect the council flagged in the video's CTA. Whatever the video decides about
labeling water claims as observation, **the page must match** — otherwise the video's honesty moment
("there is no water field in this data") directly contradicts the page it's driving traffic to.

---

## ✅ What the page already does well — keep

- Strong FAQ block (11 Qs) — ready for `FAQPage` schema and a direct source for AEO passages
- TREC IABS + Consumer Protection Notice links present and correct
- Equal Housing Opportunity notice present
- License number displayed (#0775435)
- Genuinely honest sections: "Who This Place Is NOT For," the SUP/Airbnb reality, flood/windstorm cost table,
  marina wait list, no-boat-ramp-in-city-limits
- Good internal linking to Temple/Belton hubs and Lake Pointe alternative

## Gaps the video can fill

- **No video embedded.** That's the entire reclaim play — embed with `VideoObject` schema.
- **No mention of the city-field problem** (11 of 15 actives filed under Belton). This is the strongest
  finding in the July data and the page doesn't have it. Adding it is a real differentiator.
- **No "data as of" freshness discipline** — dates appear in prose, not in a `dateModified`-backed block.
- Page is investor-heavy (STR, DSCR, rent ranges). Fine for the page; the **video must stay buyer-lane**.
