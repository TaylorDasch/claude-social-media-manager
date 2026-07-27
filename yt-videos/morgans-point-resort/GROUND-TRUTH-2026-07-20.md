# Morgan's Point Resort — Verified Ground Truth Pack
**Source:** `/Users/taylordasch_1/market-monitor/whole-market-with-status-2026-07-20.csv`
**Filter:** `City == "Morgans Point Resort"` OR `subdivisionNAME contains "Morgan"` → **29 rows**
**Verified:** 2026-07-26 by direct CSV recount (stdlib csv, not estimated)
**Date-stamp all on-camera numbers as: July 20, 2026**

---

## A. CONFIRMED — every council-prompt number recomputed and matched

| Claim in prompt | Recount | Status |
|---|---|---|
| 29 rows | 29 | ✅ |
| Active 15 | 15 | ✅ |
| Active range $205,000–$869,000 | $205,000–$869,000 | ✅ |
| Active median $330,000 | $330,000 | ✅ |
| Active median 1,791 sqft | 1,791 | ✅ |
| Active median 28 DOM | 28 | ✅ |
| Active Under Contract 4, median $273,250 | 4 / $273,250 | ✅ |
| Pending 2, median $232,450 | 2 / $232,450 | ✅ |
| Closed 7, median close $220,000 | 7 / $220,000 | ✅ |
| Closed median 93 DOM | 93 | ✅ |
| Active year built 1966–2026, median 1979 | 1966–2026, median 1979 | ✅ |
| Belton ISD on all 29 | 29/29 | ✅ |
| HOA None 27 / Mandatory 2 | 27 / 2 | ✅ |

**Status total reconciles:** 15 Active + 4 AUC + 2 Pending + 7 Closed + **1 Coming Soon ($299,900)** = 29.
The prompt omits the Coming Soon row. Say "15 active listings" — do NOT say "15 homes for sale total."

---

## B. ⚠️ CORRECTION — the prompt contains one factual error

**Prompt says (Scars-and-All bullet 2):** *"what's actually SELLING is the older, smaller stock"*

**The data says the opposite on vintage:**

| | Active (n=15) | Closed (n=7) |
|---|---|---|
| Median year built | **1979** | **2000** |
| Median sqft | 1,791 | 1,356 |
| Median $/sqft | $188 | $175 |

- **Smaller: TRUE.** Closed median 1,356 sqft vs active median 1,791 sqft.
- **Older: FALSE.** Closed median build year is 2000 — 21 years *newer* than the active median.
- **The hard version:** closed build years were 2025, 2007, 2003, 2000, 1999, 1997, 1985. **Zero homes built before 1985 closed in this window.** Meanwhile **8 of the 15 active listings were built before 1980.**

**Corrected framing (use this on camera):**
> The 1970s stock isn't what's selling — it's what's *sitting*. Eight of the fifteen homes for sale here were built before 1980. Not one home built before 1985 closed in this window. Buyers are voting against the old stock with their feet, and the sellers haven't repriced for it yet.

This is a stronger, more useful, and more defensible version of the aging-stock thesis than the prompt's original bullet.

---

## C. 🔑 NEW FINDING — the search-mechanics gap (strongest contrarian asset in the dataset)

**22 of 29 MPR rows are entered in the MLS with `City = "Belton"`. Only 7 say "Morgans Point Resort."**

Active listings specifically: **11 of 15 are filed under Belton. Only 4 say Morgans Point Resort.**

| Status | Filed "Belton" | Filed "Morgans Point Resort" |
|---|---|---|
| Active (15) | 11 | 4 |
| Active Under Contract (4) | 3 | 1 |
| Pending (2) | 2 | 0 |
| Closed (7) | 5 | 2 |
| Coming Soon (1) | 1 | 0 |

**Why this matters and why it's video-worthy:** 3,600 people a month search "morgans point resort tx." A buyer who then types "Morgan's Point Resort" into a portal city filter is shown roughly **a quarter** of the actual active inventory — because the listing agents filed the rest under Belton. This is a concrete, verifiable, MPR-specific mistake that costs buyers real options, and it is the single most useful thing this video can hand a viewer.

**Compliance phrasing:** state it as what the MLS records show as of July 20, 2026 — a data-entry pattern, not an accusation about any agent. Portal behavior varies; tell the viewer to search by **map area or zip, not city name**, and verify against the map.

---

## D. NEGOTIATION LEVERAGE — hard numbers for the "this is not a fast-turn market" thesis

**Price cuts: 7 of 15 active listings (47%) have already cut from original list.**

| Street | Original | Current | Cut |
|---|---|---|---|
| Morgans Point | $395,000 | $355,000 | −10.1% |
| Cliffside | $219,900 | $205,000 | −6.8% |
| Cliffside | $289,000 | $272,500 | −5.7% |
| Wrangler | $750,000 | $715,000 | −4.7% |
| Morgans Point | $249,900 | $244,900 | −2.0% |
| Sherwood | $269,900 | $265,000 | −1.8% |
| Oakmont | $425,000 | $420,000 | −1.2% |

**Closed sales vs ORIGINAL list price** (the number that actually shows negotiating room):

| Close | Orig list | % of original | DOM |
|---|---|---|---|
| $195,000 | $225,000 | 86.7% | 112 |
| $255,000 | $299,900 | 85.0% | 145 |
| $205,000 | $235,000 | 87.2% | 93 |
| $251,000 | $275,990 | 90.9% | 104 |
| $210,000 | $229,900 | 91.3% | 38 |
| $220,000 | $239,000 | 92.1% | 60 |
| $225,000 | $235,000 | 95.7% | 9 |

- Median close ≈ **91% of original list**.
- MLS `SP/LP %` field (vs *final* list): 90.7, 91.1, 91.3, 92.1, 95.7, 96.5, 100.0 → median **92.1%**.
- **Both pending homes sat 206 and 239 days** before going under contract.
- Longest-sitting actives: Dos Rios $869K at **193 DOM**; Wrangler $715K at **103 DOM** (already cut $35K); Daingerfield $665K at **102 DOM**.

### ⚠️ Don't oversell the "47% have cut" stat — the cuts are mostly small

The seven cuts are −10.1%, −6.8%, −5.7%, −4.7%, −2.0%, −1.8%, −1.2%. **Median cut: −4.7%.** Only two of
the seven exceed 6%. "Nearly half the listings have cut" is true but implies capitulation that the
magnitudes don't support — four of the seven are token adjustments.

**Honest version:** "Seven of the fifteen have already cut. But look at the size of the cuts — the middle
one is under five percent. That's not a market capitulating. That's sellers testing, and it tells you
where the real conversation starts, not that anyone's desperate."

The **stronger** leverage evidence is the closed side, not the active side: sales landed near 91% of
*original* list, and the two pendings sat 206 and 239 days.

### ⚠️ Never characterize identifiable listings as overpriced

Dos Rios ($869,000, 193 DOM), Wrangler ($715,000, 103 DOM, cut $35,000), and Daingerfield ($665,000,
102 DOM) are real listings with real sellers and real agents. State DOM and price-cut history as
observable record. Never render a verdict on the seller's pricing judgment — that is a professional-courtesy
and defamation-adjacent problem, and it is the exact clip a competing agent would screenshot.

**On-camera framing:** homes that sold gave up about 9% off their original ask, and the two that went
pending waited more than half a year. State the record; let the viewer draw the conclusion.

---

## E. THE ACTUAL PRICE TIERS — mapped to streets and $/sqft

Full active list, cheapest to most expensive:

| List | SqFt | $/sf | Built | DOM | Street | MLS City |
|---|---|---|---|---|---|---|
| $205,000 | 1,001 | $205 | 1979 | 21 | Cliffside | Belton |
| $230,000 | 1,435 | $160 | 2000 | 13 | Bobcat | Belton |
| $244,900 | 1,421 | $172 | 1977 | 51 | Morgans Point | Belton |
| $249,500 | 1,253 | $199 | 1979 | 4 | Hickory | Belton |
| $265,000 | 1,658 | $160 | 2006 | 28 | Sherwood | Belton |
| $272,500 | 1,791 | $152 | 1971 | 73 | Cliffside | Belton |
| $315,000 | 1,605 | $196 | 2006 | 19 | Market | Morgans Point Resort |
| $330,000 | 1,760 | $188 | 2002 | 23 | Bluebonnet | Morgans Point Resort |
| $337,777 | 1,804 | $187 | 1966 | 2 | Ridgewood | Belton |
| $349,900 | 2,323 | $151 | 1977 | 4 | Roy Bean | Belton |
| $355,000 | 2,214 | $160 | 1976 | 114 | Morgans Point | Belton |
| $420,000 | 1,925 | $218 | 1976 | 33 | Oakmont | Belton |
| $665,000 | 2,704 | $246 | 2019 | 102 | Daingerfield | Morgans Point Resort |
| $715,000 | 2,484 | $288 | 1995 | 103 | Wrangler | Belton |
| $869,000 | 2,804 | $310 | 2026 | 193 | Dos Rios | Morgans Point Resort |

**$/sqft range: $151 → $310. That spread is the real tier signal — not list price.**

### 🔑 The top of the range is partly a different subdivision, not just a better street

The two highest-$/sf listings sit in subdivisions that are **not** "Morgans Point Resort Sec 1–9":

- **$869,000 Dos Rios — subdivision `Rancho Del Lago`, built 2026** (193 DOM)
- **$665,000 Daingerfield — subdivision `Campus At Lakewood Ranch Ph`, built 2019**, community pool

Both are inside MPR city limits but are distinct, newer developments. **This is the structural explanation for the $205K–$869K spread** and it sharpens the prompt's "street tier" thesis: the spread isn't only water proximity — it's *which development you're actually buying into*, and two of them are modern builds carrying modern pricing into an otherwise 1970s housing stock.

Subdivision counts across all 29: MPR Sec 1 (6), Sec 2 (5), Sec 3 (3), Sec 8 (3), Sec 5 (2), Sec 7 (2), Sec 9 (2), Sec 4 (1), Sec 6 (1), MPR City Sec (1), **Campus At Lakewood Ranch (1)**, **Rancho Del Lago (1)**, Morgans Point (1).

**Pool field across 29:** None 20 · Community 6 · Private 3.

---

## F. 🚫 WHAT THE MLS CANNOT VERIFY — do not assert these as data

The May 18 concept in this folder built its thesis on **three water tiers** (lakefront / lake-view / inland). That framing is consistent with the current data, but be precise about provenance:

- **The CSV contains no waterfront, water-access, dock, or shoreline field.** Water proximity per street is Taylor's local observation, **not an MLS-verified fact**. Label it on camera as observation.
- Do **not** promise lake access, water rights, or dock permissions for any lot — direct viewers to the City of Morgan's Point Resort and the USACE Belton Lake Resource Manager's Office.
- Do **not** state drive times that have not been measured — measure them on the shoot or tell viewers to test at their own commute hour.
- HOA is 27 None / 2 Mandatory — **verify per property**, never state as universal.
- Schools: "All 29 MLS records show Belton ISD — verify your exact address with Belton ISD."
- Belton Lake levels fluctuate — send viewers to USACE for current levels before believing any "lake view" listing.

---

## H. 🔥 ROUND-1 CRITIC FINDINGS — VERIFIED BY RECOUNT 2026-07-26. THESE OVERRIDE §C.

### H1. The city-filter gap is a PRICE illusion, not an inventory illusion

§C framed the finding as "you see a quarter of the inventory." That is true but it is the *weak* version
and it points the buyer's conclusion in the wrong direction. Recount of the 15 actives split by MLS city field:

| | n | Prices | Median | Cheapest |
|---|---|---|---|---|
| **Visible** under city = "Morgans Point Resort" | 4 | $315,000 · $330,000 · $665,000 · $869,000 | **$497,500** | **$315,000** |
| **Hidden** under city = "Belton" | 11 | $205,000 → $715,000 | $272,500 | **$205,000** |
| All actives | 15 | $205,000 → $869,000 | $330,000 | $205,000 |

- The visible median ($497,500) is **50.8% above** the true active median ($330,000).
- **Cheapest visible $315,000 vs cheapest actual $205,000 — a $110,000 gap.**
- **All 6 actives under $275,000 are filed under Belton. Every single one:**
  Cliffside $205,000 · Bobcat $230,000 · Morgans Point $244,900 · Hickory $249,500 ·
  Sherwood $265,000 · Cliffside $272,500.

**The corrected buyer mistake:** a buyer who filters by the town's name doesn't conclude "there's nothing
here." They see a town that starts at $315,000 and runs to $869,000, decide it's out of budget, and cross
it off — when the actual entry point is $205,000. **The filter doesn't hide inventory; it hides the entire
affordable half of the town.** That is the video.

### H1b. 🔥 The city field sorts by VINTAGE too — a 35-year median gap. This is the joint of the whole video.

Verified by recount 2026-07-26 from the §E active table:

| | n | Build years | Median build year |
|---|---|---|---|
| Name-carrying (city = "Morgans Point Resort") | 4 | 2002 · 2006 · 2019 · 2026 | **2012.5** |
| Belton-filed (city = "Belton") | 11 | 1966 · 1971 · 1976 · 1976 · 1977 · 1977 · 1979 · 1979 · 1995 · 2000 · 2006 | **1977** |

- **Not one listing carrying the town's own name was built before 2002.**
- **All 8 pre-1980 actives are on the Belton side. 8 of 8.**

**Why this is the spine:** the MLS city field doesn't just hide the affordable half — it hides the *old*
half, and they are the same half. Search Morgan's Point Resort by name and you see a town with a median
build year of 2012 and a median price of $497,500. The actual town has a median build year of 1977 and a
median asking price of $272,500 on that side of the split.

So the buyer who shops by name gets a doubly false picture: too expensive **and** too new. They either
cross the town off as unaffordable, or — worse — they form a mental model of newer construction, find the
one affordable listing that leaks through, and walk into a 1970s inspection with 2019 expectations.

**This welds the price problem to the inspection problem into one video instead of two.** The affordable
half and the aging half are the same eleven houses.

### H2. Do NOT assert portal behavior — assert the field value

The export proves the MLS **city field**, not what Zillow/Realtor/Redfin do with it. Portals ingest, geocode,
and filter differently, and they change. Any line saying "Zillow only shows you 4" or "you're only seeing 4"
is an unprovable claim about a third party and must not ship.

**Say instead:** "In the July 20, 2026 MLS records, 11 of the 15 active listings here have their city field
set to Belton — including every home under $275,000. If your search keys on the town name, ask where those
eleven went." Then instruct: search by **map area or zip**, not city name, and confirm against the map.

### H3. The leverage claim must use $/sqft, not the median gap

| Comparison | Gap |
|---|---|
| Active median $330,000 vs closed median $220,000 | closed is **33% below** active |
| Active median $188/sf vs closed median $175/sf | closed is **6.9% below** active |
| Active median 1,791 sqft vs closed median 1,356 sqft | actives are **32% bigger** |

The 33% price gap is almost entirely a **size/composition artifact** — actives are bigger homes, not the same
homes discounted. Presenting "$330K asking vs $220K selling" as negotiating room overstates leverage by
roughly 4–5x and a sharp viewer will catch it. **The honest leverage numbers are the ones in §D:** 7 of 15
actives already cut, closed sales landed near 91% of *original* list, both pendings sat 206 and 239 days.

### H4. Pending and Active-Under-Contract medians are LIST prices, not agreed prices

AUC median $273,250 and Pending median $232,450 are what sellers are **asking**. The MLS shows no sale price
until closing. Never sequence $330,000 → $273,250 → $232,450 → $220,000 as a descending "price ladder" —
three of those four are seller ask, only $220,000 is money that actually changed hands. Different cohorts,
different home sizes, and three different meanings of "price."

---

## I. THE CLOSED "WINDOW" — now defined, and it is small. Never say "in this window" again.

The critic flagged that every closed-sale claim leaned on an undefined "window." Recounted from `CloseDate`:

| Close date | Price | Built | Street | On market |
|---|---|---|---|---|
| 2026-05-18 | $225,000 | 2000 | Bobcat | 2026-04-14 |
| 2026-06-05 | $205,000 | 2007 | Morgans Point | 2026-02-18 |
| 2026-06-22 | $210,000 | 1999 | Winecup | 2026-04-17 |
| 2026-06-22 | $251,000 | 1997 | Cottonwood Loop | 2026-02-12 |
| 2026-07-02 | $255,000 | 2003 | Great West | 2026-01-12 |
| 2026-07-07 | $195,000 | 2025 | Briarwood | 2026-02-12 |
| 2026-07-16 | $220,000 | 1985 | Blackjack | 2026-05-17 |

- **The window is 2026-05-18 → 2026-07-16 — roughly 60 days.** (The export's full closed range is
  2026-05-18 → 2026-07-20 across 984 county-wide sales, so this is a ~2-month export, not a 12-month one.)
- **Correct phrasing:** "the seven homes that closed in the roughly sixty days ending July 20, 2026."
  Never "in this window," never "recently," never an implied year.

### ⚠️ Sample-size honesty requirement

**n = 7.** Every closed-side claim — the vintage inversion, the ~91%-of-original figure, the 93-day median
DOM — rests on seven sales in about two months. That is a real signal but it is a thin one, and a sharp
viewer or a competing agent will say so first if Taylor doesn't.

**Say it on camera, once, plainly:** "Seven homes closed here in about the last sixty days. Seven is a small
number — I'm not going to pretend it's a trend. It's what the record shows right now, and it's more than
you had before you clicked."

Owning n=7 out loud converts the single biggest attack surface in the package into a credibility moment.
Do not bury it in a disclaimer; say it in the segment where the closed data is used.

---

## G. PRIOR-TAKE CONSISTENCY CHECK (council Phase 0)

Prior council run in this folder: `reason-run-260518-1647`, converged 5-0 × 2 rounds, May 14 MLS pull.
Prior concept: *"I Toured Three $250K Homes in Morgan's Point Resort. Only One Was Actually on the Lake"* — a same-price comp walk across three water tiers; contrarian thesis was "MPR is three markets stacked on the same MLS rows; the median is a misleading anchor."

**No contradiction.** The new prompt's "the street you pick matters more than the house" is the same spine with fresher data. The July 20 data **strengthens** it and adds two things the May version did not have: the Belton-vs-MPR city-field gap (§C) and the vintage inversion (§B). Treat the May concept as v1 and this as the evidence-upgraded v2 — do not re-litigate the spine, extend it.
