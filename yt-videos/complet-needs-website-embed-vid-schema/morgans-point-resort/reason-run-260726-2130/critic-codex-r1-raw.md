2026-07-27T02:36:45.348808Z ERROR codex_core::session::session: failed to load skill /Users/taylordasch_1/.claude/skills/geo-query-finder/SKILL.md: missing YAML frontmatter delimited by ---
OpenAI Codex v0.145.0
--------
workdir: /Users/taylordasch_1/claude-social-media-manager/yt-videos/morgans-point-resort/reason-run-260726-2130
model: gpt-5.6-sol
provider: openai
approval: never
sandbox: read-only
reasoning effort: xhigh
reasoning summaries: none
session id: 019fa16e-8edf-7ef1-a0b4-3bc82ac8a385
--------
user
ROLE: You are an adversarial critic from a different AI lab than the author (Claude / Anthropic). You are Codex, trained on OpenAI's corpus. You do not share Anthropic's RLHF conditioning or voice priors — that is the value you bring. Attack from a different angle than a Claude critic would.

CONTEXT — TAYLOR DASCH / EG REALTY / TEMPLE TX:
- Real estate agent at EG Realty, Temple, TX. Channel: "Living in Temple" (buyer/relocator lane).
- Investor-analyst voice: data-first, honest negatives, no generic real-estate language.
- Lane discipline: NO investor framing on buyer content (no cap rates, no cash flow, no rental analysis).
- Banned vocabulary: dream home, dream, charming, nestled, turnkey, hidden gem, perfect neighborhood, exclusive, stunning, gorgeous, paradise, oasis, picturesque, "you'll love," "won't last," "must see," boasts, "a true gem," "one-of-a-kind," sneak peek, white glove, "my expertise," insider, safe, family-friendly, good schools.
- Say "agent," never "broker." No dollar-volume or transaction-count credentials on camera. Do not imply Taylor served in the military.
- Format: identity declaration ("Taylor Dasch with EG Realty") must appear early in the script but NOT inside the first 15 seconds.

The draft below is a 16-deliverable YouTube video package about Morgan's Point Resort, Texas — a small incorporated lake city on Belton Lake in Bell County. Two files follow: (1) the VERIFIED GROUND TRUTH, recomputed directly from the July 20, 2026 CTXMLS export, and (2) the DRAFT.

TASK: Attack this draft ruthlessly. Imagine the most informed hostile commenter on r/TempleTX, a local agent who has sold in Morgan's Point Resort for 20 years, and a buyer who got burned on a lake lot. What would they tear apart? What would a competitor agent quote out of context to discredit Taylor?

MOST IMPORTANT: audit every number in the DRAFT against the GROUND TRUTH file. Any figure, ratio, or derived percentage in the draft that is not supported by the ground truth is a FATAL finding. Watch specifically for: derived percentages presented as MLS facts, medians compared across cohorts that aren't comparable, counts that don't reconcile, and any water/dock/lake-access claim (the MLS has NO waterfront field at all — §F).

For each weakness:
1. Tag FATAL (cannot ship: fabricated/unsupported number, fair housing, TREC, lane break, banned vocab, promises Taylor can't keep), MAJOR (degrades deliverable), or MINOR (polish)
2. Quote the EXACT line
3. Propose the rewrite

Also check explicitly:
- Identity-declaration timing
- Any forward-looking claim, market forecast, rate prediction, or "will" statement
- Whether the concept is genuinely Morgan's Point Resort-specific or could be find-and-replaced to any lake town
- Whether the hook's central claim survives scrutiny
- Whether the draft commits Taylor to actions he can't fulfill
- Retention logic: does each segment actually earn the next 60 seconds, or does it sag?
- Compliance: TREC, IABS, Fair Housing, MLS attribution

Output structure:
FATAL WEAKNESSES (must fix or kill):
1. [Quote] — [Why fatal] — [Proposed rewrite]
MAJOR WEAKNESSES:
MINOR WEAKNESSES:
DOMAIN CHECKS: (identity timing, banned vocab, lane discipline, number provenance, MPR-specificity — each PASS/FAIL with line reference)
VERDICT: one line naming the single most critical weakness overall.

Find a MINIMUM of 3 weaknesses; more is better. Do NOT soften. Do not praise. Attack only.

===== FILE 1: VERIFIED GROUND TRUTH =====
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

**On-camera framing:** the seller who prices at the top of the range here is not getting it. Homes that sold gave up about 9% off original ask, and the two that went pending waited more than half a year.

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

## G. PRIOR-TAKE CONSISTENCY CHECK (council Phase 0)

Prior council run in this folder: `reason-run-260518-1647`, converged 5-0 × 2 rounds, May 14 MLS pull.
Prior concept: *"I Toured Three $250K Homes in Morgan's Point Resort. Only One Was Actually on the Lake"* — a same-price comp walk across three water tiers; contrarian thesis was "MPR is three markets stacked on the same MLS rows; the median is a misleading anchor."

**No contradiction.** The new prompt's "the street you pick matters more than the house" is the same spine with fresher data. The July 20 data **strengthens** it and adds two things the May version did not have: the Belton-vs-MPR city-field gap (§C) and the vintage inversion (§B). Treat the May concept as v1 and this as the evidence-upgraded v2 — do not re-litigate the spine, extend it.

===== FILE 2: THE DRAFT TO ATTACK =====
# CANDIDATE A — Round 1
## Morgan's Point Resort, TX — Flagship Video Package (16 deliverables)

**Author:** Author-A
**Ground truth:** `../GROUND-TRUTH-2026-07-20.md` (CTXMLS pull `whole-market-with-status-2026-07-20.csv`, recounted 2026-07-26)
**All on-camera market numbers date-stamped:** July 20, 2026
**Lane:** buyer / relocator. **Channel:** Living in Temple. **Target length:** 10:40.

---

# 1. SINGLE BEST CONCEPT

**One sentence:**
A buyer's operating procedure for Morgan's Point Resort that proves on screen — against the July 20, 2026 CTXMLS records — that the city-name filter hides most of the active inventory, that price per square foot and *which development you're actually in* set the tier instead of list price, and that the pre-1980 housing stock everyone assumes is the bargain is the overhang sellers have not repriced yet.

**Why this concept and not the tour:**

The town's whole problem is that it is *illegible*. It is an incorporated city that gets filed under another city's name, with a $205,000–$869,000 active spread inside a few square miles, a median that describes no house you can buy, and a housing stock whose oldest half is the part that is not moving. Every one of those four facts is verifiable in the July 20, 2026 records, and every one of them is specific to Morgan's Point Resort. A drone tour with numbers read over it does not survive a local watching it. A procedure that hands a buyer three checks they can run themselves before they ever drive out does.

**Structural note — this is v2, not a re-do.** The prior council concept (`reason-run-260518-1647`) established the spine: MPR is multiple markets stacked on one set of MLS rows and the median is a misleading anchor. This extends that spine with two things the May version did not have — the city-field gap (§C) and the vintage inversion (§B) — and replaces the "three $250K homes" device with a repeatable buyer procedure. The spine is not re-litigated. It is upgraded.

**The device that makes it un-swappable:** a persistent on-screen **provenance chip** in the lower left, which changes with every claim:

| Chip | Meaning | Example use |
|---|---|---|
| `CONFIRMED — CTXMLS 7/20/26` | Recomputed directly from the MLS export | "11 of 15 actives filed under Belton" |
| `SNAPSHOT — 7/20/26` | True on that date, will move | "median 28 DOM on actives" |
| `OBSERVATION — TAYLOR, ON THE GROUND` | Not in the MLS. Taylor's local read. | anything about water proximity or elevation |
| `OPINION` | Taylor's judgment call | "the top of this range is not getting paid" |

The chip is the compliance system *and* the trust device. It is also the single hardest thing for a competitor to copy, because it forces the creator to actually know which of their claims the data supports.

---

# 2. TITLE — RECOMMENDED + 8 ALTERNATES

**RECOMMENDED:**

> **Morgan's Point Resort TX: Why You're Only Seeing 4 of the 15 Listings**

68 characters. Exact-match keyword front-loaded for the 3,600/mo term. A specific number contradiction that a buyer can immediately test on their own phone. No banned words. No superlatives. The open loop ("why?") is answered at 1:10, not withheld to the end.

**8 alternates, by angle:**

| # | Title | Angle | Chars |
|---|---|---|---|
| 1 | Morgan's Point Resort TX: 11 of the 15 Listings Are Filed Under Belton | The data-entry fact, stated flat | 69 |
| 2 | The $205K to $869K Problem in Morgan's Point Resort, TX | Price spread | 55 |
| 3 | Morgan's Point Resort TX: The Median Price Is a Lie (Here's the Real Tier Map) | Median takedown | 77 |
| 4 | Before You Buy in Morgan's Point Resort, TX — Run These 3 Checks | Procedure / utility | 63 |
| 5 | Morgan's Point Resort TX: The Old Lake Houses Aren't Selling. Here's the Math. | Vintage inversion | 77 |
| 6 | Living in Morgan's Point Resort, TX — What the Listings Don't Tell You | Broad-match relocator | 69 |
| 7 | I Read Every Morgan's Point Resort Listing. 8 of 15 Have the Same Problem. | Pre-1980 overhang | 73 |
| 8 | Morgan's Point Resort vs Belton, TX: They're Not the Same Market | Comparison / competing intent | 63 |

**A/B note:** if the recommended title underperforms on CTR at the day-9 check, swap to alternate 4 — it is the same value proposition rewritten from curiosity to utility, and it preserves the exact-match keyword.

**Do not use:** any title built on "lake life," aspirational-lifestyle phrasing, "you won't believe," or a price with a "?" — all of them read as the generic tour this concept exists to reject.

---

# 3. THUMBNAIL CONCEPT

**Composition (three visual elements, no more):**

1. **Background — drone frame, golden hour.** Belton Lake filling the left two-thirds, MPR shoreline homes on the right edge of the water, shot low and wide enough that the peninsula shape reads. Warm, real, slightly underexposed sky. No lens flare, no color-graded teal-orange, no vignette.
2. **Taylor, right third**, cut out at chest height, looking at the lake — not at camera, not smiling for the sell. Neutral expression. Body angled into frame.
3. **Text block, left, stacked two lines** over the water where contrast is highest.

**EXACT THUMBNAIL TEXT:**

```
$205K → $869K
SAME SMALL TOWN
```

Line 1: heavy condensed sans, white with a 3px near-black stroke, arrow in a muted amber so it reads at 168px wide.
Line 2: 45% the size of line 1, all caps, white, tight tracking.

**Emotional hook:** *disorientation.* A buyer who has already priced this town in their head has one number in mind. Seeing both ends of the range in the same frame breaks that number and creates a question the title then names.

**Why the thumbnail carries the price spread and the title carries the search gap:** they must not repeat each other. The spread is instantly legible as an image; the search gap needs words. Paired, they stack two separate open loops in one impression. If the thumbnail also said "4 OF 15," the impression would be redundant and the click would be worth less.

**Do not include:** a sunset silhouette, a boat, a "FOR SALE" sign graphic, a red circle/arrow, an open-mouth reaction face, or any fourth element. No luxury framing — no aerial of the $869K build as the hero image.

**Variant to hold in reserve (test at day 14 if CTR is under target):** same background, text swapped to `4 OF 15` / `WHAT YOU'RE MISSING`. This aligns thumbnail to title and trades curiosity breadth for message clarity.

---

# 4. FIFTEEN-SECOND OPENING HOOK — VERBATIM

Read at a brisk, flat, unhurried pace — roughly 175 words per minute, no music under the first six seconds. Cold open on drone motion. **No entity declaration inside this block** (that lands at 0:22).

> "Type 'Morgan's Point Resort' into a home search and you'll see four listings. There are fifteen active — July twentieth, twenty twenty-six MLS records. The other eleven are filed under Belton. If you're shopping this lake town from out of town, those eleven are the smallest of your three problems."

**48 words. Lands at 0:15–0:16.**

**Delivery notes:**
- Hit "four" and "fifteen" with a beat of silence on either side.
- "July twentieth, twenty twenty-six" is spoken, not just supered — the date stamp must survive a listener who is not watching.
- "those eleven are the smallest of your three problems" is the retention contract. Three problems means three unresolved loops at 0:16, which is what carries a cold viewer to the 1:00 mark.

**Formula check:** specific number contradiction (4 vs 15) + who this is for (shopping this lake town from out of town) + delayed payoff (three problems, none of them named yet). ✅

---

# 5. RETENTION OUTLINE — 8–12 MIN, WITH TIMESTAMPS

**Target runtime: 10:40.** Visual or audio change every ~7 seconds throughout. Every beat below carries a `WHY THEY STAY` line — the specific unresolved thing that pulls the next 60 seconds.

---

### 0:00–0:16 — COLD OPEN: THE FOUR-OF-FIFTEEN GAP
Drone push over Belton Lake toward the MPR shoreline. Hook delivered verbatim (§4). Graphic G1 snaps in at 0:04 over the drone plate.
**WHY THEY STAY:** Three problems were promised and zero have been named.

### 0:16–0:50 — WHAT THIS PLACE ACTUALLY IS + THE CONTRACT
Ground, city entrance sign. Entity declaration lands here.
> "Taylor Dasch, agent with EG Realty in Temple. Morgan's Point Resort is its own incorporated city sitting on Belton Lake — it is not a Belton subdivision, even though most of its listings say Belton. In the next ten minutes I'm going to hand you three checks to run before you drive out here: how to actually see the whole market, how to price a house in a town with a $205,000 to $869,000 spread, and how to know whether the age of the house has been priced in yet. Everything with a number on it comes from the July twentieth, twenty twenty-six MLS records, and everything that isn't in the MLS gets labeled on screen."
G2 (the three problems) + first appearance of the provenance chip legend.
**WHY THEY STAY:** He just told them exactly what they get and when. Contract established; the labeling promise pre-empts the skepticism a lake-town video normally triggers.

### 0:50–1:55 — PROBLEM 1: YOU CAN'T SEE THE MARKET
Screen-recording style graphic, not a live portal capture. G3.
> "Twenty-nine MLS records tie to Morgan's Point Resort as of July twentieth. Twenty-two of them are entered with the city field set to Belton. Seven say Morgans Point Resort. Narrow it to just the active listings and it's worse — eleven of fifteen say Belton, four say Morgans Point Resort. That's not anybody doing anything wrong. It's a data-entry pattern, and it's consistent enough that you have to plan around it. Thirty-six hundred people a month search 'Morgan's Point Resort TX.' A big share of them are going to type that into a city filter and get shown roughly a quarter of what's actually for sale here — and then decide this town has no inventory."
Then the fix, G4:
> "So don't search by city name. Draw the map area, or search the zip, and then confirm every result against the map. Portals handle this differently and they change — the map is the only thing that doesn't lie about location."
**WHY THEY STAY:** They just got a usable fix in 60 seconds and were told two more are coming. This is the payback that buys the rest of the video.

### 1:55–3:20 — THE GEOGRAPHY THAT EXPLAINS THE PRICE SPREAD
The video's best drone sequence. Wide arc revealing the peninsula shape, then a cut that contrasts a water-facing street run against an interior street run, then elevation.
> "Here's why one small town runs from $205,000 to $869,000. It's not floor plans. It's water proximity, elevation, lot position, and — this is the part nobody says — which development you're actually standing in."
Provenance chip flips to `OBSERVATION — TAYLOR, ON THE GROUND` for the entire water-proximity passage.
> "I need to be straight with you about this: there is no waterfront field, no water-access field, and no dock field in the MLS data I'm using. Every word I say about how close a street is to the water is me standing here looking at it — not something the MLS verified. Treat it that way."
**WHY THEY STAY:** He just voluntarily disarmed his own strongest visual claim. That is the trust spike, and it makes the numbers in the next segment land harder.

### 3:20–5:05 — PROBLEM 2: PRICE THE FOOT, NOT THE HOUSE
G6, the full 15-listing ladder sorted by $/sqft.
> "Fifteen active listings, July twentieth. Sorted by price per square foot, the range runs $151 a foot to $310 a foot. The most expensive foot in this town costs more than double the cheapest one — inside one small city. Price per foot is your tier signal here. List price is not."
Then G7, the two-house device — the strongest single comparison in the dataset:
> "Look at these two. The median-priced active listing in this town is on Bluebonnet — 2002 build, 1,760 square feet, $330,000, $188 a foot. The median-*sized* active listing is on Cliffside — 1971 build, 1,791 square feet, $272,500, $152 a foot. Thirty-one square feet apart in size. Thirty-one years apart in age. Fifty-seven thousand five hundred dollars apart in price. That's the whole town in two rows."
Then G8, the subdivision reveal:
> "And the top of the range isn't just a better street. The $869,000 listing on Dos Rios is a 2026 build in a subdivision called Rancho Del Lago. The $665,000 on Daingerfield is a 2019 build in Campus At Lakewood Ranch, with a community pool. Both are inside city limits. Neither one is in Morgan's Point Resort Sections One through Nine, where twenty-five of the twenty-nine records sit. So when you see a $600K-plus comp in this town, your first question isn't 'is it on the water.' It's 'is it even in the same subdivision as the house I'm buying.'"
**WHY THEY STAY:** Two things just got reframed at once — the median and the top comps. If a buyer had already run comps here, they now suspect their comp set is wrong, and the next segment promises to tell them what *is* moving.

### 5:05–6:50 — PROBLEM 3: THE VINTAGE INVERSION
G9 and G10.
> "Here's the one that surprised me. The conventional read on a lake town like this is that the older, cheaper stock is what moves and the new builds sit. In these records, it's inverted. Active listings: median year built 1979. Closed sales: median year built 2000. What sold is twenty-one years *newer* than what's sitting on the market."
> "Harder version. The seven closed sales were built in 2025, 2007, 2003, 2000, 1999, 1997, and 1985. Not one home built before 1985 closed in this window. Meanwhile eight of the fifteen active listings were built before 1980."
> "The 1970s stock isn't what's selling. It's what's *sitting*. Buyers are voting against it with their feet, and — chip says opinion, this is my read, not a data point — the sellers haven't repriced for it yet."
Then the second price tag, framed as a math instruction, not a defect claim:
> "That doesn't make a 1976 house a bad buy. It makes it a different math problem. On a house that age you're pricing roof age, foundation history, electrical panel, plumbing material, HVAC age, and what your insurance carrier is going to say about all of it — before you compare the monthly payment to a new build somewhere else. I'm not telling you any specific home here has any of those issues. I'm telling you the inspection is where the second price tag shows up, and in a town where the median active build year is 1979, you budget for that up front."
**WHY THEY STAY:** He has now told them the market is soft on the exact stock most of the inventory is. The obvious next question — *so how much can I actually push?* — is the next segment.

### 6:50–8:20 — THE LEVERAGE: THIS IS NOT A FAST-TURN MARKET
G11, G12, G13.
> "So how much room do you have. Seven of the fifteen active listings — forty-seven percent — have already cut from their original ask. A Morgans Point listing went $395,000 to $355,000, down ten percent, and it's still sitting at 114 days. Wrangler went $750,000 to $715,000 and it's at 103 days. Cliffside cut to $205,000."
> "Now the number sellers don't put in the ad. Compare the seven closed sales to their *original* list price, not the last one: 86.7 percent, 85.0, 87.2, 90.9, 91.3, 92.1, 95.7. Median: about ninety-one percent of original ask. Median days on market to get there: ninety-three."
> "And the pattern inside that is the useful part. The house that closed in nine days gave up about four percent. The house that took a hundred and forty-five days gave up fifteen. Speed and discount are tied together here, and both pending homes sat two hundred six and two hundred thirty-nine days before they went under contract."
Then G-Ladder, the four-median descent:
> "One more. Active median asking: $330,000. Under contract median: $273,250. Pending median: $232,450. Closed median: $220,000. Those are four different groups of houses, not one house over time — so don't read it as a price crash. Read it as this: what sellers are asking and what buyers are agreeing to are not in the same neighborhood right now."
**WHY THEY STAY:** They now have negotiation ammunition and want to know what could still blow the deal up. That is the verify list.

### 8:20–9:50 — THE VERIFY LIST: WHAT THE MLS CANNOT TELL YOU
G14 stays on screen the whole segment; Taylor walks a public street and a public park/boat ramp area.
> "Five things this data cannot answer, and all five have burned buyers in lake towns."
> "One. Lake access, water rights, and docks. Nothing in the MLS I pulled verifies any of that for any lot. If a listing implies it, you verify it with the City of Morgan's Point Resort and with the U.S. Army Corps of Engineers Belton Lake Resource Manager's Office — in writing, before your option period ends. Not with me, not with the listing."
> "Two. Lake level. Belton Lake goes up and down. A 'lake view' photographed in a full-pool spring is a different property in a drawdown. Check the current Corps of Engineers lake level before you fall for a photo."
> "Three. HOA. Across all twenty-nine records, twenty-seven show no HOA and two show mandatory. That is not a rule about this town — it's a count. Verify per property, in the documents."
> "Four. Schools. All twenty-nine MLS records show Belton ISD. Verify your exact address with Belton ISD directly, because attendance boundaries are the district's call, not the MLS's."
> "Five. The drive. Groceries, dining, and major retail are a drive out to Belton or Temple. I'm not going to quote you a drive time I didn't measure — put the address in your phone and drive it at the hour you'd actually be driving it, on a weekday. That one test tells you more about living here than anything I can say."
**WHY THEY STAY:** The last item reframes the entire decision from price to daily life, which is the emotional close, and the CTA follows directly from the five gaps he just named.

### 9:50–10:40 — WHO THIS TOWN IS FOR, AND THE ASK
Golden-hour drone hold. G15.
> "Straight opinion to close. If you want a lake town where most lots have no HOA, where you'll do real diligence on an older house, and where you have room to negotiate because the market is not turning fast — this is a real option and the numbers back that up. If you need new construction, a short grocery run, and a fast, clean transaction, the honest answer is you're probably looking at the wrong city, and I'd rather tell you that now than at the inspection."
CTA delivered verbatim (§10). End card, no outro music sting over the phone number.

---

# 6. CONTRARIAN THESIS

**Stated for camera:**

> "Morgan's Point Resort is not one cheap lake market with a wide price range. It is at least three separate markets sharing one city name — and the three tools a buyer normally reaches for all point at the wrong one. The city filter hides two-thirds of it. The median describes a house that isn't representative of anything. And the oldest stock, which everybody assumes is the discount, is the part that isn't selling."

**The three markets, defined by evidence, not vibe:**

1. **The 1970s core** — Cliffside, Hickory, Morgans Point, Roy Bean, Oakmont, Ridgewood. Built 1966–1979. $151–$218 per foot. This is where 8 of the 15 actives live and where the DOM piles up (73, 114 days).
2. **The 2000s infill** — Bobcat, Sherwood, Market, Bluebonnet. Built 2000–2006. $160–$196 per foot. Short DOM (13, 19, 23, 28 days). This is closest to what actually closed (closed median build year 2000).
3. **The top tier** — the three listings above $218/sf. Two of them are in developments that are not MPR Sec 1–9 at all: Rancho Del Lago (2026 build, $869,000, $310/sf, 193 DOM) and Campus At Lakewood Ranch (2019, $665,000, $246/sf, 102 DOM). The third, Wrangler (1995, $715,000, $288/sf, 103 DOM, already cut $35,000), is the one that proves $/sf and not build year is the tier signal — it is a 1990s house carrying the second-highest price per foot in town. All three have sat 100+ days.

**Why this is defensible and not a hot take:** every tier boundary above is a column in the July 20, 2026 export — subdivision name, year built, list price, sqft, DOM. The only unverified layer is water proximity, which is labeled as observation on screen every time it appears.

**Note on tier 3 and the on-camera script:** the script names Rancho Del Lago and Campus At Lakewood Ranch because they carry the structural subdivision point. Wrangler is used in the leverage segment instead (as a $35,000 cut still sitting at 103 days), which is where it does the most work.

**What this thesis explicitly refuses to do:** it does not lean on the $330,000 median as an anchor after arguing the median is misleading. The median appears exactly twice — once as the thing being dismantled, once inside the four-median ladder where it is explicitly labeled as a group median across different houses.

---

# 7. BUYER MISTAKE PREVENTED

**The mistake, in one sentence:**
Touring a quarter of the market and then negotiating as if it were the whole market.

**The mechanism, step by step — this is the part that makes it real:**

1. A relocator finds Morgan's Point Resort on a map or a portal listing and searches the city name.
2. Because 11 of the 15 active listings are filed under `City = Belton` in the July 20, 2026 records, the city filter returns roughly 4.
3. From that thin slice they form two beliefs: *"there's barely anything here"* and *"here's what this town costs."*
4. Both beliefs are built on a non-random sample. The 4 that surface are not a random 4 — they are whichever listings happened to get the city field entered a particular way.
5. They then either (a) write the town off entirely, or (b) fall in love with one of the four and write at or near ask, because they have no visible competing inventory and no idea that 47% of the real active list has already cut price and that closed sales are landing near 91% of original ask.
6. If the house they picked is one of the 8 pre-1980 actives, they compound it: they pay near ask on the segment of the market with the worst absorption in this window — zero pre-1985 closings — and then meet the age-of-home costs at inspection with no negotiating room left, because they already used it.

**The prevention, stated as three actions the viewer can take today:**

1. **Search by drawn map area or zip, then verify every result against the map** — never by city name. Rebuild the comp set from the map, not the filter.
2. **Sort your list by price per square foot and check the subdivision line** before you compare anything. A $600K-plus comp in Rancho Del Lago or Campus At Lakewood Ranch does not price a house in MPR Sec 1–9.
3. **Pull original list price and days on market on every home you shortlist,** not just current price. The gap between original and current is your opening position; in this snapshot the median closed sale landed near 91% of *original* ask.

**Secondary mistake prevented:** believing a "lake view" or implied lake access is a property right. It is not verified anywhere in this data. Verify with the City of Morgan's Point Resort and the USACE Belton Lake Resource Manager's Office before the option period closes.

---

# 8. SHOT LIST — ONE GOLDEN-HOUR TRIP

**Constraint set:** public rights-of-way and public-access locations only. No filming that identifies a specific active listing's address, house number, or yard sign — the video must never look like it is marketing another agent's listing or steering to a specific home. No people identifiable in frame. Drone flown per FAA Part 107, and **confirm current USACE and City of Morgan's Point Resort rules for launch/landing on park and Corps-managed land before the trip** — launch from public street right-of-way if there is any question.

**Timing:** arrive 75 minutes before sunset. Drone the water first (best light, worst wind risk later), ground second, drive beat last in the fading light.

### DRONE — 6 setups, ~35 minutes

| # | Shot | Move | Purpose in edit |
|---|---|---|---|
| D1 | Low push over Belton Lake toward the MPR shoreline, sun behind camera | Slow forward, 25–40 ft AGL over water | **Cold open plate (0:00–0:16).** Must feel like arrival, not a postcard. |
| D2 | High reveal of the peninsula shape | Ascend + slow pedestal, 300–380 ft | **The geography beat (1:55).** This single shot has to make the town's shape self-explanatory. |
| D3 | Water-facing street run | Lateral truck parallel to shoreline, 120 ft | Half of the tier contrast. |
| D4 | Interior street run, matched altitude, matched speed, matched direction | Lateral truck, 120 ft | Other half. **Cut D3→D4 on a hard match cut** — the contrast only reads if the moves are identical. |
| D5 | Elevation change — low ground rising away from water | Reverse-and-rise | Supports the elevation half of the tier observation. |
| D6 | Golden-hour hold, wide, water + treeline + sky | Static hover, 20 sec+ | **Closing plate (9:50–10:40).** Needs to run long enough to hold the CTA without a cut. |

### GROUND — 7 setups, ~40 minutes

| # | Shot | Notes |
|---|---|---|
| G-A | Taylor at the **city entrance sign** | The 0:16 entity-declaration beat. Sign must be legible — it is the proof MPR is its own city. Two takes: one wide, one medium. |
| G-B | Walk-and-talk on a **public street**, water in the background | Problem 1 delivery. Keep house numbers out of focus. |
| G-C | **Public park / boat ramp access point** | Verify-list beat (8:20). Shows the public lake access that does exist without implying any private lot has it. |
| G-D | Representative **1970s-era exterior**, shot from public right-of-way, framed so no address or sign is readable | Vintage inversion beat. Prefer a home that is clearly not listed. |
| G-E | Representative **newer infill build**, same framing rules, matched lens and distance to G-D | The cut between G-D and G-E carries the whole vintage argument visually. Match the framing or it fails. |
| G-F | **The drive beat** — dash-mount or passenger-side, leaving MPR toward the Belton/Temple retail corridor | Run the clock. **Record the actual elapsed time and the departure time of day.** If it is not measured, the line becomes "test it yourself at your real commute hour" and no number goes on screen. |
| G-G | Taylor to camera, static, water behind, tripod | CTA and the who-it's-for close. Shoot last, in the warmest light. |

### AUDIO / TECH
- DJI Mic on Taylor for all ground; capture 60 seconds of clean lake ambience with no dialogue for the bed under drone plates.
- Shoot D3/D4 and G-D/G-E back to back with locked settings — the match cuts are non-negotiable.
- **Log every clip against its script beat on location.** Any beat with no usable footage becomes a graphic-only segment, and that decision needs to be made on the shoot, not in the edit.

---

# 9. EXACT ON-SCREEN GRAPHICS

Every data graphic carries the footer `CTXMLS · July 20, 2026` in 60% opacity. Provenance chip is persistent, lower left, and changes per claim. Lower-thirds only — no full-screen takeovers over Taylor.

**G0 — PROVENANCE CHIP LEGEND (0:44, 4 sec)**
```
CONFIRMED — CTXMLS 7/20/26   ·   SNAPSHOT — 7/20/26
OBSERVATION — TAYLOR, ON THE GROUND   ·   OPINION
```

**G1 — THE GAP (0:04)**
```
MORGAN'S POINT RESORT, TX — ACTIVE LISTINGS
SEARCHED BY CITY NAME ............ 4
ACTUALLY ACTIVE .................. 15
CTXMLS · July 20, 2026
```

**G2 — THE THREE PROBLEMS (0:35)**
```
1  YOU CAN'T SEE THE WHOLE MARKET
2  YOU'RE PRICING THE WRONG VARIABLE
3  THE AGE HASN'T BEEN PRICED IN
```

**G3 — THE CITY FIELD (1:05)**
```
HOW THESE LISTINGS ARE FILED IN THE MLS
                    "Belton"    "Morgans Point Resort"
Active (15)            11                 4
Under Contract (4)      3                 1
Pending (2)             2                 0
Closed (7)              5                 2
Coming Soon (1)         1                 0
TOTAL (29)             22                 7
CTXMLS · July 20, 2026
```

**G4 — THE FIX (1:40)**
```
SEARCH BY DRAWN MAP AREA OR ZIP — NOT CITY NAME
Then confirm every result against the map.
```

**G5 — THE CITY (2:05)**
```
MORGAN'S POINT RESORT
Its own incorporated city on Belton Lake.
Not a Belton subdivision.
```

**G6 — THE LADDER, SORTED BY $/SQFT (3:30, holds 25 sec)**
```
15 ACTIVE LISTINGS — SORTED BY PRICE PER SQUARE FOOT
$151/sf   $349,900   2,323 sf   1977   Roy Bean
$152/sf   $272,500   1,791 sf   1971   Cliffside
$160/sf   $230,000   1,435 sf   2000   Bobcat
$160/sf   $265,000   1,658 sf   2006   Sherwood
$160/sf   $355,000   2,214 sf   1976   Morgans Point
$172/sf   $244,900   1,421 sf   1977   Morgans Point
$187/sf   $337,777   1,804 sf   1966   Ridgewood
$188/sf   $330,000   1,760 sf   2002   Bluebonnet
$196/sf   $315,000   1,605 sf   2006   Market
$199/sf   $249,500   1,253 sf   1979   Hickory
$205/sf   $205,000   1,001 sf   1979   Cliffside
$218/sf   $420,000   1,925 sf   1976   Oakmont
$246/sf   $665,000   2,704 sf   2019   Daingerfield
$288/sf   $715,000   2,484 sf   1995   Wrangler
$310/sf   $869,000   2,804 sf   2026   Dos Rios
CTXMLS · July 20, 2026
```

**G7 — TWO HOUSES (4:10, holds 20 sec)**
```
MEDIAN PRICE              vs        MEDIAN SIZE
BLUEBONNET                          CLIFFSIDE
$330,000                            $272,500
1,760 sqft                          1,791 sqft
Built 2002                          Built 1971
$188 / sqft                         $152 / sqft
23 DOM                              73 DOM
--------------------------------------------------
31 SQFT APART.  31 YEARS APART.  $57,500 APART.
CTXMLS · July 20, 2026
```

**G8 — NOT THE SAME SUBDIVISION (4:45)**
```
THE TOP OF THE RANGE ISN'T MPR SEC 1–9
$869,000  Dos Rios       Rancho Del Lago            Built 2026   193 DOM
$665,000  Daingerfield   Campus At Lakewood Ranch   Built 2019   102 DOM
Inside city limits. Different developments.
CTXMLS · July 20, 2026
```

**G9 — THE INVERSION (5:20)**
```
                        ACTIVE (15)     CLOSED (7)
Median year built          1979            2000
Median sqft               1,791           1,356
Median $/sqft              $188            $175
CTXMLS · July 20, 2026
```

**G10 — THE OVERHANG (6:00)**
```
ZERO homes built before 1985 CLOSED in this window.
8 of the 15 ACTIVE listings were built before 1980.
Closed build years: 2025 · 2007 · 2003 · 2000 · 1999 · 1997 · 1985
CTXMLS · July 20, 2026
```

**G11 — WHO HAS ALREADY CUT (7:00, holds 15 sec)**
```
7 OF 15 ACTIVE LISTINGS HAVE CUT PRICE (47%)
Morgans Point   $395,000 → $355,000   −10.1%
Cliffside       $219,900 → $205,000    −6.8%
Cliffside       $289,000 → $272,500    −5.7%
Wrangler        $750,000 → $715,000    −4.7%
Morgans Point   $249,900 → $244,900    −2.0%
Sherwood        $269,900 → $265,000    −1.8%
Oakmont         $425,000 → $420,000    −1.2%
CTXMLS · July 20, 2026
```

**G12 — CLOSED VS ORIGINAL ASK (7:35, holds 15 sec)**
```
7 CLOSED SALES vs ORIGINAL LIST PRICE
CLOSE       ORIGINAL     % OF ORIGINAL     DOM
$195,000    $225,000        86.7%          112
$255,000    $299,900        85.0%          145
$205,000    $235,000        87.2%           93
$251,000    $275,990        90.9%          104
$210,000    $229,900        91.3%           38
$220,000    $239,000        92.1%           60
$225,000    $235,000        95.7%            9
MEDIAN ≈ 91% OF ORIGINAL ASK  ·  MEDIAN 93 DOM
CTXMLS · July 20, 2026
```

**G13 — SPEED AND DISCOUNT (7:55)**
```
9 DAYS  →  gave up ~4%
145 DAYS  →  gave up 15%
Both pending homes sat 206 and 239 days.
CTXMLS · July 20, 2026
```

**G-LADDER — THE FOUR MEDIANS (8:05)**
```
ASKING          $330,000    (15 Active)
UNDER CONTRACT  $273,250    (4)
PENDING         $232,450    (2)
CLOSED          $220,000    (7)
Four different groups of homes — not one home over time.
CTXMLS · July 20, 2026
```

**G14 — THE VERIFY LIST (8:25, holds through 9:50)**
```
NOT IN THIS DATA — VERIFY YOURSELF
1  Lake access / water rights / docks → City of Morgan's Point Resort
   + USACE Belton Lake Resource Manager's Office
2  Current lake level → USACE, before you trust a "lake view" photo
3  HOA → 27 of 29 records show None, 2 show Mandatory. Verify per property.
4  Schools → All 29 records show Belton ISD. Verify your address with Belton ISD.
5  The drive → measure it yourself, at your real commute hour
```

**G15 — CTA CARD (10:05, holds to end)**
```
MORGAN'S POINT RESORT SHORTLIST
Text 254-718-4249
templetxhomes.net/morgans-point-resort
Taylor Dasch · Agent · EG Realty
```

**Standing rule for the editor:** if a number appears on screen without the `CTXMLS · July 20, 2026` footer, the graphic is wrong and does not ship.

---

# 10. EXACT CTA

**Spoken on camera at 10:05, verbatim, with the required framing sentence in front of it:**

> "One thing before you go, and I want to be precise about what I'm offering, because I said earlier the water tiers are my read and not MLS-verified — that's still true, and it's exactly why this is worth a conversation instead of a filter."
>
> **"Text me for the current Morgan's Point Resort shortlist — I'll separate the true water-tier lots from the pretenders and run the real monthly payment including the age-of-home costs before you drive out."**
>
> "Two-five-four, seven-one-eight, four-two-four-nine. Text the word MORGANS and tell me your price range. I'll send the map-drawn list, not the city-filter list."

**Why this CTA follows from what was demonstrated:** the video spent 10 minutes proving three things a filter cannot do — build the list from the map instead of the city field, read the tier from $/sqft and subdivision instead of list price, and price the age of the house before the offer. The offer is those three things, done for them. It is not "call me if you want to see homes."

**Placement:**
- **Verbal only at 1:50** — one line, no card: "If you want the map-drawn list instead of the city-filter list, that's the text at the end." Plants the offer at the moment of peak usefulness, before the audience thins.
- **Full CTA at 10:05** with G15.
- Pinned comment (§14) and description (§12) carry the same wording.

**Do not:** put a mid-roll CTA card over the leverage segment. That segment is the highest-value stretch in the video and an overlay there costs more retention than the CTA gains.

---

# 11. FIVE SHORTS / REELS CUTS — VERBATIM

All five: vertical, hard-cut cold open, no intro, burned captions, provenance chip retained in the lower third. All five carry the date stamp on screen. No music over the first 2 seconds.

---

### SHORT 1 — "THE FOUR OF FIFTEEN" (38 sec) — *lead cut, post first*
**Title:** `Morgan's Point Resort TX: You're Only Seeing 4 of 15 Listings`

> "If you're searching Morgan's Point Resort, Texas, you are probably looking at a quarter of the market and you don't know it.
> As of the July twentieth, twenty twenty-six MLS records, there are twenty-nine listings tied to this town. Twenty-two of them are entered with the city field set to Belton. Only seven say Morgans Point Resort.
> Look at just the active listings and it's worse — eleven of fifteen say Belton. Four say Morgans Point Resort.
> Nobody's doing anything wrong. It's a data-entry pattern. But it means if you type the city name into a search filter, you get shown four homes and you conclude this town has no inventory.
> Draw the map instead. Or search the zip. Then check every result against the map.
> Taylor Dasch, agent with EG Realty. Text me for the map-drawn list."

**On screen:** `4` vs `15` at 0:02 · the city-field table at 0:12 · `SEARCH THE MAP, NOT THE CITY NAME` at 0:28.

---

### SHORT 2 — "THIRTY-ONE SQUARE FEET, FIFTY-SEVEN THOUSAND DOLLARS" (42 sec)
**Title:** `Two Nearly Identical-Size Homes in Morgan's Point Resort TX — $57,500 Apart`

> "Two active listings in Morgan's Point Resort, Texas. Same town. Same month. Thirty-one square feet apart in size.
> House one, on Bluebonnet: 1,760 square feet, built 2002, asking $330,000. That's $188 a foot. Twenty-three days on market.
> House two, on Cliffside: 1,791 square feet, built 1971, asking $272,500. That's $152 a foot. Seventy-three days on market.
> Thirty-one square feet apart. Thirty-one years apart. Fifty-seven thousand five hundred dollars apart.
> That's why the median price in this town is close to useless. July twentieth, twenty twenty-six MLS records.
> If you're comparing homes here on list price, you're comparing the wrong number. Sort by price per foot.
> Taylor Dasch, agent with EG Realty in Temple."

**On screen:** split-screen stat card the entire runtime, values animating in one line at a time.

---

### SHORT 3 — "THE OLD HOUSES AREN'T THE BARGAIN" (44 sec)
**Title:** `The Old Lake Houses in Morgan's Point Resort TX Aren't Selling`

> "Everybody assumes the older, cheaper stock in a lake town is what moves. In Morgan's Point Resort, Texas, the data says the opposite.
> July twentieth, twenty twenty-six MLS records. Active listings: median year built, 1979. Closed sales: median year built, 2000. What sold is twenty-one years newer than what's sitting.
> Harder version: the seven closed sales were built in 2025, 2007, 2003, 2000, 1999, 1997, and 1985. Not one home built before 1985 closed.
> Meanwhile eight of the fifteen active listings were built before 1980.
> The 1970s stock isn't what's selling here. It's what's sitting. And in my read — that's my opinion, not a data point — the sellers haven't repriced for it yet.
> That doesn't make an older house a bad buy. It makes it a different math problem: roof, foundation, systems, insurance. Budget the second price tag before you write.
> Taylor Dasch, agent with EG Realty."

**On screen:** `1979` vs `2000` at 0:08 · `ZERO PRE-1985 HOMES CLOSED` at 0:20 · `8 OF 15 ACTIVE BUILT BEFORE 1980` at 0:26.

---

### SHORT 4 — "HOW MUCH ROOM YOU ACTUALLY HAVE" (46 sec)
**Title:** `Morgan's Point Resort TX: 47% of Listings Already Cut Price`

> "How much negotiating room do you have in Morgan's Point Resort, Texas? Here's the number sellers don't advertise.
> July twentieth, twenty twenty-six MLS records. Seven of the fifteen active listings — forty-seven percent — have already cut from their original ask. One went $395,000 to $355,000 and it's still sitting at a hundred fourteen days.
> Now compare the seven closed sales to their original list price, not their last one. Median: about ninety-one percent of original ask. Median days on market: ninety-three.
> And here's the pattern. The house that closed in nine days gave up about four percent. The house that took a hundred forty-five days gave up fifteen.
> Both pending homes sat two hundred six and two hundred thirty-nine days before going under contract.
> This is not a fast-turn market. Sellers are asking above what buyers are agreeing to. If you're buying here, you have room — bring the original list price to the table, not the current one.
> Taylor Dasch, agent with EG Realty."

**On screen:** price-cut table at 0:10 · `MEDIAN ≈ 91% OF ORIGINAL ASK` at 0:24 · `9 DAYS = ~4% OFF · 145 DAYS = 15% OFF` at 0:32.

---

### SHORT 5 — "DON'T ASSUME THE LAKE" (40 sec) — *the protective cut*
**Title:** `Before You Buy a "Lake View" Lot in Morgan's Point Resort TX`

> "If you're buying in Morgan's Point Resort, Texas because of the lake, verify this before your option period ends.
> The MLS data I pulled for this town has no waterfront field, no water-access field, and no dock field. Not one. So a listing photo showing water is a photo — it is not a verified property right.
> Lake access, water rights, and dock permissions get verified with the City of Morgan's Point Resort and with the U.S. Army Corps of Engineers Belton Lake Resource Manager's Office. In writing.
> And check the current Corps lake level. Belton Lake goes up and down — a lake view shot at full pool is a different property in a drawdown.
> Two more from the same July twentieth, twenty twenty-six records: twenty-seven of twenty-nine listings show no HOA and two show mandatory, so verify per property. And all twenty-nine show Belton ISD — verify your exact address with the district.
> Taylor Dasch, agent with EG Realty. Verify it in writing, not from a photo."

**On screen:** `NO WATERFRONT FIELD IN THE MLS DATA` at 0:04 · the 5-item verify list at 0:20.

---

**Distribution plan:** Short 1 within 24 hours of the long-form going live (it is the strongest standalone hook and drives the most search-adjacent discovery). Then Short 3, Short 4, Short 2, Short 5 across the following two weeks. TikTok cadence stays at 3/week and no two land on the same weekday in the same week. Every Short's caption links to the long-form and to `templetxhomes.net/morgans-point-resort`.

---

# 12. YOUTUBE DESCRIPTION

```
Taylor Dasch, agent with EG Realty in Temple, Texas. If you're searching Morgan's Point Resort, TX, there's a good chance you're only seeing about a quarter of what's for sale — because of how the listings are filed in the MLS. This video walks through three checks to run before you drive out here, using the July 20, 2026 CTXMLS records.

Morgan's Point Resort is its own incorporated city on Belton Lake — not a Belton subdivision — and the active listings there run from $205,000 to $869,000. That spread isn't random, and the median price doesn't describe anything you can actually buy.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT'S IN THIS VIDEO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Why searching the city name shows you 4 of the 15 active listings — and the search that fixes it
• The real tier map: price per square foot ($151–$310) and which development you're actually buying into
• The vintage inversion: what's selling here is 21 years NEWER than what's sitting
• Your negotiating position: 47% of active listings have already cut price
• The five things the MLS cannot verify — and exactly who to call for each

00:00 The 4-of-15 problem
00:16 What Morgan's Point Resort actually is
00:50 Problem 1: You can't see the whole market
01:55 The geography behind the price spread
03:20 Problem 2: Price the foot, not the house
05:05 Problem 3: The old stock isn't the bargain
06:50 How much negotiating room you have
08:20 Five things the MLS can't tell you
09:50 Who this town fits — and who it doesn't

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THE DATA — CTXMLS, JULY 20, 2026
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
29 MLS records tie to Morgan's Point Resort as of July 20, 2026:
• 15 Active — $205,000 to $869,000 · median $330,000 · median 1,791 sqft · median 28 days on market
• 4 Active Under Contract — median $273,250
• 2 Pending — median $232,450 (these two sat 206 and 239 days)
• 7 Closed — median close $220,000 · median 93 days on market · median ≈ 91% of ORIGINAL list price
• 1 Coming Soon — $299,900

• Active year built: 1966 to 2026, median 1979. Closed median year built: 2000.
• Zero homes built before 1985 closed in this window. 8 of 15 active listings were built before 1980.
• Price per square foot on actives: $151 to $310.
• 7 of 15 active listings (47%) have already cut from original list price.
• City field: 22 of the 29 records are entered as "Belton," 7 as "Morgans Point Resort." Actives: 11 Belton, 4 Morgans Point Resort.
• HOA: 27 of 29 records show None, 2 show Mandatory — verify per property.
• Schools: all 29 MLS records show Belton ISD — verify your exact address with Belton ISD.
• Pool field across all 29: 20 None, 6 Community, 3 Private.

These are a snapshot of one MLS pull on one date. They will move. Re-verify before you make a decision.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VERIFY THIS YOURSELF — DON'T TAKE MY WORD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Lake access, water rights, docks → City of Morgan's Point Resort + the U.S. Army Corps of Engineers Belton Lake Resource Manager's Office. Nothing in the MLS data used here verifies water access, dock rights, or shoreline for any lot. Any water-proximity comment in this video is my own on-the-ground observation and is labeled as such on screen.
• Current Belton Lake level → U.S. Army Corps of Engineers. Lake levels fluctuate; a "lake view" photo is not a guarantee of a view.
• HOA → the recorded documents for the specific property.
• Schools → Belton ISD directly, for your exact address.
• Drive times → measure them yourself, at the hour you'd actually be driving.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GET THE SHORTLIST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Text me for the current Morgan's Point Resort shortlist — I'll separate the true water-tier lots from the pretenders and run the real monthly payment including the age-of-home costs before you drive out.

Text MORGANS to 254-718-4249 with your price range.
Full neighborhood breakdown: https://templetxhomes.net/morgans-point-resort/

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ABOUT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Taylor Dasch is a licensed Texas real estate agent with EG Realty, based in Temple, Texas, working the Temple / Belton / Bell County market. This channel covers what it's actually like to live in and buy around Temple, Texas — with the market data behind it.

📍 templetxhomes.net
📧 dealswithdasch@gmail.com
📱 254-718-4249

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DISCLOSURES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Market data sourced from Central Texas MLS, pulled July 20, 2026, and recounted July 26, 2026. This is a snapshot, not a forecast, and not an appraisal. Nothing here is legal, tax, financial, or investment advice. Water proximity, elevation, and lot-position comments are personal observations made on site, not MLS-verified facts. Verify all property-specific facts — HOA, schools, lake access, flood, condition — independently before making a decision.

Texas Real Estate Commission — Information About Brokerage Services and Consumer Protection Notice: [PASTE the IABS + CPN links already hosted on templetxhomes.net before publishing]

#MorgansPointResort #MorgansPointResortTX #BeltonLake #BeltonTexas #TempleTX #CentralTexasRealEstate #MovingToTexas #BellCountyTX #TexasLakeTowns #RelocatingToTexas
```

---

# 13. CHAPTERS

```
00:00 The 4-of-15 problem
00:16 What Morgan's Point Resort actually is
00:50 Problem 1: You can't see the whole market
01:55 The geography behind the price spread
03:20 Problem 2: Price the foot, not the house
05:05 Problem 3: The old stock isn't the bargain
06:50 How much negotiating room you have
08:20 Five things the MLS can't tell you
09:50 Who this town fits — and who it doesn't
```

Nine chapters, first at 00:00, all well over the 10-second minimum. Each title is a benefit or a question, not a section label — chapter text is a second CTR surface in search results and suggested feeds.

---

# 14. PINNED COMMENT

```
The single most useful thing in this video, in case you skip: as of the July 20, 2026 MLS records, 22 of the 29 listings tied to Morgan's Point Resort are entered with the city field set to "Belton" — only 7 say "Morgans Point Resort." On the active listings it's 11 Belton vs 4 Morgans Point Resort.

So if you search this town by city name, you're likely seeing about a quarter of what's for sale. Draw the map area or search the zip instead, then confirm every result against the map. Portals handle this differently and they change — the map is the only thing that doesn't lie about location.

Three things I want to be clear about, because lake towns burn buyers on exactly these:

1) There is no waterfront, water-access, or dock field in the MLS data I used. Every water-proximity comment in this video is my own observation standing there, not an MLS-verified fact. Verify lake access, water rights, and dock permissions with the City of Morgan's Point Resort and the U.S. Army Corps of Engineers Belton Lake Resource Manager's Office — in writing, before your option period ends.

2) HOA: 27 of the 29 records show None and 2 show Mandatory. That's a count, not a rule about this town. Verify per property.

3) Schools: all 29 MLS records show Belton ISD — verify your exact address with Belton ISD directly.

Every number in this video is a July 20, 2026 snapshot. It will move. Re-pull before you make a decision.

Want the map-drawn shortlist instead of the city-filter version? Text MORGANS to 254-718-4249 with your price range and I'll send it, with the real monthly payment including the age-of-home costs.

— Taylor Dasch, agent with EG Realty, Temple TX
```

---

# 15. SEO / GEO / AEO TARGETS + QUOTABLE ANSWER PASSAGES

## 15a. Keyword targets

**Primary:** `morgans point resort tx` — 3,600 searches/mo (DataForSEO Google Ads, pulled 2026-07-26). This is the only volume figure sourced; do not quote a number for anything below.

**Secondary targets — no volume pulled, do not cite figures for these:**
`morgans point resort texas` · `morgans point resort tx homes for sale` · `living in morgans point resort tx` · `is morgans point resort a good place to live` · `morgans point resort vs belton tx` · `morgans point resort tx real estate` · `morgans point resort tx hoa` · `morgans point resort school district` · `belton lake homes for sale` · `morgans point resort city limits`

**Video-side optimization:**
- Filename before upload: `morgans-point-resort-tx-4-of-15-listings-july-2026.mp4`
- Exact phrase "Morgan's Point Resort" spoken in the first 8 seconds and in the first line of the description.
- Both spellings appear in the description body — "Morgan's Point Resort" (apostrophe, how people type it) and "Morgans Point Resort" (no apostrophe, how the MLS files it). This matters here specifically: the MLS city string is `Morgans Point Resort` and search behavior splits across both.
- Upload a corrected transcript rather than relying on auto-captions. Every quotable passage below must survive verbatim in the transcript — that is what AI search engines actually retrieve.

## 15b. The reclaim play — video ↔ page

`https://templetxhomes.net/morgans-point-resort/` sits at ~position 18.7 with 712 impressions/90d (GSC). The video's job in that reclaim:

1. **Embed the video on the page** above the fold, with `VideoObject` schema including `uploadDate`, `description`, and `transcript`.
2. **Port the passages in §15c onto the page verbatim** as an FAQ block with `FAQPage` schema. Identical wording across video transcript and page text is the point — it doubles the retrieval surface for the same answer.
3. **Add the July 20, 2026 snapshot table to the page** with a visible "data as of" line and a `dateModified` that matches.
4. **Internal links out of the page:** to the Belton hub, the Temple hub, and the builder-incentive page — MPR buyers cross-shop new construction, and the video explicitly names that comparison.
5. **Internal link into the page** from the Belton and Belton Lake pages using anchor text "Morgan's Point Resort" — the city-confusion problem is exactly why that link needs to exist.

## 15c. Quotable answer passages — verbatim, for AI search extraction

Each is written to be lifted whole: direct answer first, ≤60 words, date-stamped, entity-attributed. Use these word-for-word in the script, the description, and on the page.

**Q: Is Morgan's Point Resort part of Belton, Texas?**
> "No. Morgan's Point Resort is its own incorporated city on Belton Lake in Bell County, Texas. It is not a Belton subdivision. However, as of the July 20, 2026 MLS records, 22 of the 29 listings tied to Morgan's Point Resort are entered with the city field set to 'Belton,' which is why buyers often confuse the two."

**Q: How much do homes cost in Morgan's Point Resort, TX?**
> "As of July 20, 2026, the 15 active listings in Morgan's Point Resort ranged from $205,000 to $869,000, with a median asking price of $330,000. The 7 closed sales in that snapshot had a median close price of $220,000. Price per square foot ranged from $151 to $310 — a better tier signal than list price."

**Q: Why is the price range in Morgan's Point Resort so wide?**
> "Three reasons, per the July 20, 2026 MLS records: housing stock spans 1966 to 2026 build years; lot position and water proximity vary sharply; and two of the highest-priced listings sit in separate subdivisions — Rancho Del Lago (2026 build, $869,000) and Campus At Lakewood Ranch (2019, $665,000) — not in Morgan's Point Resort Sections 1 through 9."

**Q: Is Morgan's Point Resort, TX a fast-moving market?**
> "No. As of July 20, 2026, 7 of the 15 active listings had already cut price, the 7 closed sales took a median 93 days and closed near 91% of original list price, and the two pending homes sat 206 and 239 days before going under contract. Buyers had negotiating room in this snapshot."

**Q: Do homes in Morgan's Point Resort have an HOA?**
> "Most records show none, but it is not universal. Of the 29 MLS records tied to Morgan's Point Resort as of July 20, 2026, 27 showed HOA 'None' and 2 showed 'Mandatory.' That is a count of listings, not a rule about the city. Verify HOA status on the specific property's recorded documents."

**Q: What school district is Morgan's Point Resort, TX in?**
> "All 29 MLS records tied to Morgan's Point Resort as of July 20, 2026 show Belton ISD. Verify your exact address with Belton ISD directly — attendance boundaries are set by the district, not by the MLS."

**Q: Do homes in Morgan's Point Resort come with lake access or a dock?**
> "Not automatically, and the MLS data does not verify it. The July 20, 2026 records contain no waterfront, water-access, or dock field for any of the 29 listings. Verify lake access, water rights, and dock permissions with the City of Morgan's Point Resort and the U.S. Army Corps of Engineers Belton Lake Resource Manager's Office before your option period ends."

**Q: Are older homes in Morgan's Point Resort a better deal?**
> "The July 20, 2026 data suggests the opposite of the usual assumption. Active listings had a median build year of 1979; closed sales had a median build year of 2000 — 21 years newer. No home built before 1985 closed in that window, while 8 of the 15 active listings were built before 1980. The older stock is what's sitting."

## 15d. Retrieval note

These passages are structured to answer the question in the first sentence and carry their own date and source inside the passage. That is deliberate: an AI answer engine that lifts one sentence still carries "as of July 20, 2026" and "MLS records" with it, so the citation stays honest even when it's excerpted out of context.

---

# 16. COMPLIANCE REVIEW + PHRASING CORRECTIONS

## 16a. Hard rules — line-by-line audit

| # | Rule | Status | Where it's handled |
|---|---|---|---|
| 1 | No invented MLS stats, testimonials, reviews, awards, top-agent claims | ✅ | Every number traces to the ground-truth file. Zero testimonials, awards, or ranking claims anywhere in the package. |
| 2 | Date-stamp all market numbers as July 20, 2026 | ✅ | Spoken in the hook; footer on every data graphic; repeated in description, pinned comment, all 5 Shorts, and inside each quotable passage. Editor rule: no footer = doesn't ship. |
| 3 | No "safe," "family-friendly," "good schools," demographic steering, protected-class language | ✅ | None present. School content is a district-of-record statement plus a verify instruction, never a quality judgment. The "who this town fits" close is framed on transaction speed, home age, and errand distance — never on people. |
| 4 | Schools phrasing | ✅ | Exact required phrasing used at 8:20, in G14, in the description, in the pinned comment, in Short 5, and in a quotable passage. |
| 5 | HOA not universal | ✅ | Always stated as "27 of 29 records show None, 2 show Mandatory — verify per property." Never "no HOA here." |
| 6 | No lake access / water rights / dock promises | ✅ | Segment at 2:40 pre-emptively disclaims it; entire verify segment at 8:20; Short 5 is built around it; pinned comment item 1; description verify block; a dedicated quotable passage. Both the City and the USACE Belton Lake Resource Manager's Office are named every time. |
| 7 | No unmeasured drive times | ✅ | Shot G-F requires an actual measurement with the time of day logged. If unmeasured, the script line is "measure it yourself at your real commute hour" and no number goes on screen. No drive-time number appears anywhere in this package. |
| 8 | No implication Taylor served | ✅ | No military reference of any kind. |
| 9 | No dollar-volume or transaction-count credentials on camera | ✅ | None on camera **and none in the description** — deliberately stricter than the rule. The only credential used is "agent with EG Realty in Temple." |
| 10 | Distinguish confirmed fact / snapshot / observation / opinion | ✅ | The provenance chip system (G0) is the mechanism, applied continuously. Opinion is verbally self-labeled twice ("that's my read, not a data point"; "straight opinion to close"). |
| 11 | "Agent," never "broker" | ✅ | "Agent" used throughout. "Broker" appears zero times in viewer-facing copy — the only instance in this document is the TREC form's legal name, "Information About Brokerage Services," which is a required disclosure title and cannot be reworded. |
| 12 | Water proximity is observation, never MLS-verified | ✅ | Chip flips to `OBSERVATION` for the entire 1:55–3:20 geography segment. Explicitly stated on camera. The CTA's water-tier language is preceded by a sentence re-flagging it as Taylor's read. |
| 13 | Buyer/relocator lane only — no investor pivots, cap rates, rent, cash flow | ✅ | Zero rent, cap rate, cash flow, ROI, appreciation-forecast, or short-term-rental content. The negotiation segment is framed entirely as *what you should offer*, never as *what this returns*. |
| 14 | Entity declaration in description and early script, but NOT in first 15 seconds | ✅ | Hook (0:00–0:16) contains no name, brokerage, or credential. Declaration lands at 0:16. Description opens with it. |

## 16b. Banned-words check

Checked against: dream home · dream · charming · nestled · turnkey · white glove · hidden gem · perfect neighborhood · exclusive · sneak peek · insider · my expertise · paradise · oasis · stunning · gorgeous · safe · family-friendly · good schools.

**Result: zero occurrences in any viewer-facing copy** — hook, script lines, all graphics, title and all 8 alternates, thumbnail text, CTA, description, chapters, pinned comment, all 5 Shorts, all quotable passages.

Also avoided as adjacent risks, though not on the list: "luxury," "must-see," "won't last," "priced to sell," "motivated seller," "up-and-coming," "great investment," and every variant of the security/protection word family.

**Deliberate near-miss avoided:** the buyer newsletter's brand name contains one of the banned words, so it is never named in any viewer-facing copy in this package — the description and pinned comment route to the website page instead.

## 16c. Phrasing corrections — risky line → shipped line

| Risky phrasing (rejected) | Shipped phrasing | Why |
|---|---|---|
| "Agents are hiding these listings under Belton" | "Twenty-two of them are entered with the city field set to Belton… That's not anybody doing anything wrong. It's a data-entry pattern." | Accusation → observable pattern. Removes the implication of intent about identifiable agents. |
| "Zillow only shows you 4 listings" | "If you type that into a city filter, you get shown roughly a quarter of what's for sale here" | Portal behavior varies and changes. Never assert a specific named portal's behavior as fact. |
| "These lakefront homes…" | "Water proximity per street is my observation standing here — there is no waterfront field in this data" | Rule 12. The MLS export has no water field at all. |
| "Most homes here have no HOA" | "Twenty-seven of twenty-nine records show none and two show mandatory — verify per property" | Rule 5. Count, not rule. |
| "It's 15 minutes to groceries" | "Put the address in your phone and drive it at the hour you'd actually be driving it" | Rule 7. No unmeasured drive time. Becomes a real number only if measured on the shoot, with the departure hour supered. |
| "These 1970s houses have roof and foundation problems" | "You're pricing roof age, foundation history, electrical panel, plumbing material, HVAC age… I'm not telling you any specific home here has any of those issues" | Prevents a defect claim about identifiable properties. Reframes as a budgeting instruction. |
| "The market is crashing / prices are falling" | "Those are four different groups of houses, not one house over time — so don't read it as a price crash" | The four-median ladder is compositional, not a time series. Stating the caveat on screen is what makes the graphic usable. |
| "Great rental potential on the lake" | *cut entirely* | Rule 13. Buyer/relocator lane. |
| "15 homes for sale" | "15 active listings" | Ground truth §A: the 29 rows include 1 Coming Soon at $299,900. "15 active listings" is the accurate phrasing. |
| "The median home here is $330,000" | "The median-*priced* active listing is on Bluebonnet… $330,000" | Attaches the median to a specific real listing instead of implying a representative home exists. |
| "Belton ISD is the school district" (flat) | "All 29 MLS records show Belton ISD — verify your exact address with Belton ISD" | Rule 4, exact required phrasing. |
| "Taylor has closed X transactions / $X volume" | *cut entirely from script AND description* | Rule 9 plus the standing no-dollar-volume-in-video rule. |

## 16d. Inverse-fail rubric — self-check

| Failure mode | Why this package doesn't trip it |
|---|---|
| 1. "Just a drone tour with numbers read over it" | The city-field gap, the Bluebonnet/Cliffside pair, the Rancho Del Lago and Campus At Lakewood Ranch subdivision reveal, and the four-median ladder all require having read the actual export. None of them can be produced by flying a drone. |
| 2. Buyer burned on an implied water claim | Water proximity is disclaimed on camera before it is ever used, chip-labeled throughout, given a dedicated verify segment, a dedicated Short, a pinned-comment item, a description block, and a quotable passage. Two named verification bodies. |
| 3. A number fails a same-day recheck or lacks its date | Every figure traces to the ground-truth tables; the date is spoken in the hook, footered on every graphic, and embedded inside every quotable passage. |
| 4. Repeats the page instead of demonstrating it | The city-field gap, the vintage inversion, the two-house comparison, the subdivision explanation, and the four-median ladder are all new evidence from the July 20, 2026 pull. The page gets rebuilt around them (§15b), not the other way around. |
| 5. Reads as investor content | Zero rent, cap rate, cash flow, or return language. Negotiation is framed as what to offer, never as what to earn. |
| 6. Leans on the $330K median after calling it misleading | The median appears twice: once being dismantled via the Bluebonnet/Cliffside pair, once inside the four-median ladder with an on-screen caveat that these are four different groups of homes. It is never used as a standalone anchor. |

## 16e. Pre-publish gate — do not upload until all five clear

1. Re-pull the MPR rows from CTXMLS on the publish date. If any headline figure has moved materially, either re-cut the affected graphic or add an on-screen line: `Data as of July 20, 2026 — re-verify current listings.`
2. Confirm every data graphic carries the `CTXMLS · July 20, 2026` footer.
3. Confirm the corrected transcript is uploaded and that all eight quotable passages survive verbatim.
4. Paste the real TREC IABS and Consumer Protection Notice links into the description — the placeholder must not ship.
5. Confirm the drive-time beat either carries a measured number with the time of day supered, or carries no number at all.

warning: Skill descriptions were shortened to fit the 2% skills context budget. Codex can still see every skill, but some descriptions are shorter. Disable unused skills or plugins to leave more room for the rest.
codex
I’m using the copy-editing skill because this is a line-level adversarial audit, then I’ll reconcile every numerical claim against the supplied ground truth and classify only defects—no compliments.
exec
/bin/zsh -lc "sed -n '1,240p' /Users/taylordasch_1/.agents/skills/copy-editing/SKILL.md" in /Users/taylordasch_1/claude-social-media-manager/yt-videos/morgans-point-resort/reason-run-260726-2130
 succeeded in 0ms:
---
name: copy-editing
description: "When the user wants to edit, review, or improve existing marketing copy, or refresh outdated content. Also use when the user mentions 'edit this copy,' 'review my copy,' 'copy feedback,' 'proofread,' 'polish this,' 'make this better,' 'copy sweep,' 'tighten this up,' 'this reads awkwardly,' 'clean up this text,' 'too wordy,' 'sharpen the messaging,' 'refresh this content,' 'update this page,' 'this content is outdated,' or 'content audit.' Use this when the user already has copy and wants it improved or refreshed rather than rewritten from scratch. For writing new copy, see copywriting."
metadata:
  version: 2.0.0
---

# Copy Editing

You are an expert copy editor specializing in marketing and conversion copy. Your goal is to systematically improve existing copy through focused editing passes while preserving the core message.

## Core Philosophy

**Check for product marketing context first:**
If `.agents/product-marketing.md` exists (or `.claude/product-marketing.md`, or the legacy `product-marketing-context.md` filename, in older setups), read it before editing. Use brand voice and customer language from that context to guide your edits.

Good copy editing isn't about rewriting—it's about enhancing. Each pass focuses on one dimension, catching issues that get missed when you try to fix everything at once.

**Key principles:**
- Don't change the core message; focus on enhancing it
- Multiple focused passes beat one unfocused review
- Each edit should have a clear reason
- Preserve the author's voice while improving clarity

---

## The Seven Sweeps Framework

Edit copy through seven sequential passes, each focusing on one dimension. After each sweep, loop back to check previous sweeps aren't compromised.

### Sweep 1: Clarity

**Focus:** Can the reader understand what you're saying?

**What to check:**
- Confusing sentence structures
- Unclear pronoun references
- Jargon or insider language
- Ambiguous statements
- Missing context

**Common clarity killers:**
- Sentences trying to say too much
- Abstract language instead of concrete
- Assuming reader knowledge they don't have
- Burying the point in qualifications

**Process:**
1. Read through quickly, highlighting unclear parts
2. Don't correct yet—just note problem areas
3. After marking issues, recommend specific edits
4. Verify edits maintain the original intent

**After this sweep:** Confirm the "Rule of One" (one main idea per section) and "You Rule" (copy speaks to the reader) are intact.

---

### Sweep 2: Voice and Tone

**Focus:** Is the copy consistent in how it sounds?

**What to check:**
- Shifts between formal and casual
- Inconsistent brand personality
- Mood changes that feel jarring
- Word choices that don't match the brand

**Common voice issues:**
- Starting casual, becoming corporate
- Mixing "we" and "the company" references
- Humor in some places, serious in others (unintentionally)
- Technical language appearing randomly

**Process:**
1. Read aloud to hear inconsistencies
2. Mark where tone shifts unexpectedly
3. Recommend edits that smooth transitions
4. Ensure personality remains throughout

**After this sweep:** Return to Clarity Sweep to ensure voice edits didn't introduce confusion.

---

### Sweep 3: So What

**Focus:** Does every claim answer "why should I care?"

**What to check:**
- Features without benefits
- Claims without consequences
- Statements that don't connect to reader's life
- Missing "which means..." bridges

**The So What test:**
For every statement, ask "Okay, so what?" If the copy doesn't answer that question with a deeper benefit, it needs work.

❌ "Our platform uses AI-powered analytics"
*So what?*
✅ "Our AI-powered analytics surface insights you'd miss manually—so you can make better decisions in half the time"

**Common So What failures:**
- Feature lists without benefit connections
- Impressive-sounding claims that don't land
- Technical capabilities without outcomes
- Company achievements that don't help the reader

**Process:**
1. Read each claim and literally ask "so what?"
2. Highlight claims missing the answer
3. Add the benefit bridge or deeper meaning
4. Ensure benefits connect to real reader desires

**After this sweep:** Return to Voice and Tone, then Clarity.

---

### Sweep 4: Prove It

**Focus:** Is every claim supported with evidence?

**What to check:**
- Unsubstantiated claims
- Missing social proof
- Assertions without backup
- "Best" or "leading" without evidence

**Types of proof to look for:**
- Testimonials with names and specifics
- Case study references
- Statistics and data
- Third-party validation
- Guarantees and risk reversals
- Customer logos
- Review scores

**Common proof gaps:**
- "Trusted by thousands" (which thousands?)
- "Industry-leading" (according to whom?)
- "Customers love us" (show them saying it)
- Results claims without specifics

**Process:**
1. Identify every claim that needs proof
2. Check if proof exists nearby
3. Flag unsupported assertions
4. Recommend adding proof or softening claims

**After this sweep:** Return to So What, Voice and Tone, then Clarity.

---

### Sweep 5: Specificity

**Focus:** Is the copy concrete enough to be compelling?

**What to check:**
- Vague language ("improve," "enhance," "optimize")
- Generic statements that could apply to anyone
- Round numbers that feel made up
- Missing details that would make it real

**Specificity upgrades:**

| Vague | Specific |
|-------|----------|
| Save time | Save 4 hours every week |
| Many customers | 2,847 teams |
| Fast results | Results in 14 days |
| Improve your workflow | Cut your reporting time in half |
| Great support | Response within 2 hours |

**Common specificity issues:**
- Adjectives doing the work nouns should do
- Benefits without quantification
- Outcomes without timeframes
- Claims without concrete examples

**Process:**
1. Highlight vague words and phrases
2. Ask "Can this be more specific?"
3. Add numbers, timeframes, or examples
4. Remove content that can't be made specific (it's probably filler)

**After this sweep:** Return to Prove It, So What, Voice and Tone, then Clarity.

---

### Sweep 6: Heightened Emotion

**Focus:** Does the copy make the reader feel something?

**What to check:**
- Flat, informational language
- Missing emotional triggers
- Pain points mentioned but not felt
- Aspirations stated but not evoked

**Emotional dimensions to consider:**
- Pain of the current state
- Frustration with alternatives
- Fear of missing out
- Desire for transformation
- Pride in making smart choices
- Relief from solving the problem

**Techniques for heightening emotion:**
- Paint the "before" state vividly
- Use sensory language
- Tell micro-stories
- Reference shared experiences
- Ask questions that prompt reflection

**Process:**
1. Read for emotional impact—does it move you?
2. Identify flat sections that should resonate
3. Add emotional texture while staying authentic
4. Ensure emotion serves the message (not manipulation)

**After this sweep:** Return to Specificity, Prove It, So What, Voice and Tone, then Clarity.

---

### Sweep 7: Zero Risk

**Focus:** Have we removed every barrier to action?

**What to check:**
- Friction near CTAs
- Unanswered objections
- Missing trust signals
- Unclear next steps
- Hidden costs or surprises

**Risk reducers to look for:**
- Money-back guarantees
- Free trials
- "No credit card required"
- "Cancel anytime"
- Social proof near CTA
- Clear expectations of what happens next

exec
/bin/zsh -lc "sed -n '241,520p' /Users/taylordasch_1/.agents/skills/copy-editing/SKILL.md" in /Users/taylordasch_1/claude-social-media-manager/yt-videos/morgans-point-resort/reason-run-260726-2130
 succeeded in 0ms:
- Privacy assurances

**Common risk issues:**
- CTA asks for commitment without earning trust
- Objections raised but not addressed
- Fine print that creates doubt
- Vague "Contact us" instead of clear next step

**Process:**
1. Focus on sections near CTAs
2. List every reason someone might hesitate
3. Check if the copy addresses each concern
4. Add risk reversals or trust signals as needed

**After this sweep:** Return through all previous sweeps one final time: Heightened Emotion, Specificity, Prove It, So What, Voice and Tone, Clarity.

---

## Expert Panel Scoring

Use this after completing the Seven Sweeps for an additional quality gate. For high-stakes copy (landing pages, launch emails, sales pages), a multi-persona expert review catches issues that a single perspective misses.

### How It Works

1. **Assemble 3-5 expert personas** relevant to the copy type
2. **Each persona scores the copy 1-10** on their area of expertise
3. **Collect specific critiques** — not just scores, but what to fix
4. **Revise based on feedback** — address the lowest-scoring areas first
5. **Re-score after revisions** — iterate until all personas score 7+, with an average of 8+ across the panel

### Recommended Expert Panels

**Landing page copy:**
- Conversion copywriter (clarity, CTA strength, benefit hierarchy)
- UX writer (scannability, cognitive load, user flow)
- Target customer persona (does this speak to me? do I trust it?)
- Brand strategist (voice consistency, positioning accuracy)

**Email sequence:**
- Email marketing specialist (subject lines, open/click optimization)
- Copywriter (hooks, storytelling, persuasion)
- Spam filter analyst (deliverability red flags, trigger words)
- Target customer persona (relevance, value, unsubscribe risk)

**Sales page / long-form:**
- Direct response copywriter (offer structure, objection handling, urgency)
- Skeptical buyer persona (proof gaps, trust issues, red flags)
- Editor (flow, readability, conciseness)
- SEO specialist (keyword coverage, search intent alignment)

### Scoring Rubric

| Score | Meaning |
|-------|---------|
| 9-10 | Publish-ready. No meaningful improvements. |
| 7-8 | Strong. Minor tweaks only. |
| 5-6 | Functional but has clear gaps. Needs another pass. |
| 3-4 | Significant issues. Major revision needed. |
| 1-2 | Fundamentally broken. Rethink approach. |

### When to Use

- **Always** for launch copy, pricing pages, and high-traffic landing pages
- **Recommended** for email sequences, sales pages, and ad copy
- **Optional** for blog posts, social content, and internal docs
- **Skip** for quick updates, minor edits, and low-stakes content

---

## Quick-Pass Editing Checks

Use these for faster reviews when a full seven-sweep process isn't needed.

### Word-Level Checks

**Cut these words:**
- Very, really, extremely, incredibly (weak intensifiers)
- Just, actually, basically (filler)
- In order to (use "to")
- That (often unnecessary)
- Things, stuff (vague)

**Replace these:**

| Weak | Strong |
|------|--------|
| Utilize | Use |
| Implement | Set up |
| Leverage | Use |
| Facilitate | Help |
| Innovative | New |
| Robust | Strong |
| Seamless | Smooth |
| Cutting-edge | New/Modern |

**Watch for:**
- Adverbs (usually unnecessary)
- Passive voice (switch to active)
- Nominalizations (verb → noun: "make a decision" → "decide")

### Sentence-Level Checks

- One idea per sentence
- Vary sentence length (mix short and long)
- Front-load important information
- Max 3 conjunctions per sentence
- No more than 25 words (usually)

### Paragraph-Level Checks

- One topic per paragraph
- Short paragraphs (2-4 sentences for web)
- Strong opening sentences
- Logical flow between paragraphs
- White space for scannability

---

## Copy Editing Checklist

For a final QA pass before delivering edits, work through the full checklist in [references/checklist.md](references/checklist.md) — covering all seven sweeps plus pre-start and final-check items.

---

## Common Copy Problems & Fixes

### Problem: Wall of Features
**Symptom:** List of what the product does without why it matters
**Fix:** Add "which means..." after each feature to bridge to benefits

### Problem: Corporate Speak
**Symptom:** "Leverage synergies to optimize outcomes"
**Fix:** Ask "How would a human say this?" and use those words

### Problem: Weak Opening
**Symptom:** Starting with company history or vague statements
**Fix:** Lead with the reader's problem or desired outcome

### Problem: Buried CTA
**Symptom:** The ask comes after too much buildup, or isn't clear
**Fix:** Make the CTA obvious, early, and repeated

### Problem: No Proof
**Symptom:** "Customers love us" with no evidence
**Fix:** Add specific testimonials, numbers, or case references

### Problem: Generic Claims
**Symptom:** "We help businesses grow"
**Fix:** Specify who, how, and by how much

### Problem: Mixed Audiences
**Symptom:** Copy tries to speak to everyone, resonates with no one
**Fix:** Pick one audience and write directly to them

### Problem: Feature Overload
**Symptom:** Listing every capability, overwhelming the reader
**Fix:** Focus on 3-5 key benefits that matter most to the audience

---

## Working with Copy Sweeps

When editing collaboratively:

1. **Run a sweep and present findings** - Show what you found, why it's an issue
2. **Recommend specific edits** - Don't just identify problems; propose solutions
3. **Request the updated copy** - Let the author make final decisions
4. **Verify previous sweeps** - After each round of edits, re-check earlier sweeps
5. **Repeat until clean** - Continue until a full sweep finds no new issues

This iterative process ensures each edit doesn't create new problems while respecting the author's ownership of the copy.

---

## References

- [Plain English Alternatives](references/plain-english-alternatives.md): Replace complex words with simpler alternatives
- [Content Refresh](references/content-refresh.md): Full checklist, refresh vs. rewrite matrix, and cadence guide
- [Copy Editing Checklist](references/checklist.md): Full QA checklist across all seven sweeps

---

## Content Refresh Editing

Copy editing isn't just for new content. Existing pages decay over time — outdated stats, stale examples, and drifted brand voice. Use the content refresh framework when traffic is declining, data is stale, or the product has changed.

**For the full refresh checklist, refresh vs. rewrite decision matrix, and cadence guide**: See [references/content-refresh.md](references/content-refresh.md)

---

## Task-Specific Questions

1. What's the goal of this copy? (Awareness, conversion, retention)
2. What action should readers take?
3. Are there specific concerns or known issues?
4. What proof/evidence do you have available?
5. Is this new copy or a refresh of existing content?

---

## Related Skills

- **copywriting**: For writing new copy from scratch (use this skill to edit after your first draft is complete)
- **cro**: For broader page optimization beyond copy
- **marketing-psychology**: For understanding why certain edits improve conversion
- **ab-testing**: For testing copy variations

---

## When to Use Each Skill

| Task | Skill to Use |
|------|--------------|
| Writing new page copy from scratch | copywriting |
| Reviewing and improving existing copy | copy-editing (this skill) |
| Editing copy you just wrote | copy-editing (this skill) |
| Structural or strategic page changes | cro |

exec
/bin/zsh -lc "find .. -name product-marketing.md -o -name product-marketing-context.md -o -path '*/.claude/product-marketing.md' 2>/dev/null | head -20" in /Users/taylordasch_1/claude-social-media-manager/yt-videos/morgans-point-resort/reason-run-260726-2130
 succeeded in 0ms:
codex
The numerical pass has already found a central category error: the draft treats pending/under-contract list-price medians as prices buyers “agreed to.” I’m checking the remaining derived figures and repeated claims now, especially portal behavior, water tiers, and the CTA promises.
mcp: node_repl/js started
mcp: node_repl/js (completed)
codex
The compliance pass needs current primary rules, so I’m checking TREC and CTXMLS sources rather than guessing—especially the placeholder disclosures and public display of identifiable active-listing data.
web search: 
web search: site:trec.texas.gov IABS consumer protection notice social media advertising rule 2026 ...
web search: 
web search: Central Texas MLS CTXMLS rules regulations internet display listings attribution ...
mcp: node_repl/js started
mcp: node_repl/js (completed)
