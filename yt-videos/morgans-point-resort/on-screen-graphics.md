# On-Screen Graphics

> **Morgan's Point Resort — council rebuild, On-Screen Graphics**
> Council run `reason-run-260726-2130` · Data: CTXMLS `whole-market-with-status-2026-07-20.csv`, pulled July 20 2026, recounted July 26 2026
> Ground truth: `GROUND-TRUTH-2026-07-20.md` · Supersedes the May 18 2026 version (archived in `archive-2026-05-18/`)

# 9. EXACT ON-SCREEN GRAPHICS

**Universal rules — every data graphic, no exceptions:**
- Footer, always: `Source: Central Texas MLS (CTXMLS) · Pulled July 20, 2026`
- Any graphic using closed data adds: `7 closed sales · May 18 – July 16, 2026`
- Provenance chip lives **upper-left**, four states only: `CONFIRMED — CTXMLS 7/20/26` · `SNAPSHOT — 7/20/26`
  · `OBSERVATION — TAYLOR, ON SITE` · `OPINION`
- **No graphic ever shows the $330,000-active vs $220,000-closed median side by side as negotiating room.**
  That gap is a size artifact — actives are 32% bigger (§H3).
- **No pending or under-contract median appears as a "price."** Those are list prices (§H4).

| ID | Beat | Hold | On-screen text (literal) | Chip |
|---|---|---|---|---|
| **G-1** | B1 0:04 | 5s | `MORGAN'S POINT RESORT, TX`<br>`15 active listings`<br>`Lowest: $205,000  ·  Highest: $869,000` | CONFIRMED |
| **G-2** | B2 0:38 | 6s | `SEARCH BY MAP AREA OR ZIP —`<br>`NOT BY CITY NAME`<br><br>`Then confirm every result against the map.` | — |
| **G-3** | B3 1:05 | 8s | **THE SPLIT** — two columns, built one at a time:<br>`Listings whose MLS city field says` <br>`"MORGANS POINT RESORT" — 4`<br>`$315,000 · $330,000 · $665,000 · $869,000`<br>`median $497,500`<br>—<br>`Listings whose MLS city field says`<br>`"BELTON" — 11`<br>`$205,000 → $715,000`<br>`median $272,500` | CONFIRMED |
| **G-4** | B3 1:40 | 7s | `THE FLOOR YOU SEE:  $315,000`<br>`THE FLOOR THAT EXISTS: $205,000`<br><br>`Difference: $110,000` <br><small>`derived: $315,000 − $205,000`</small> | CONFIRMED |
| **G-5** | B3 1:55 | 6s | `ACTIVE LISTINGS UNDER $275,000`<br>`Cliffside $205,000 — filed Belton`<br>`Bobcat $230,000 — filed Belton`<br>`Morgans Point $244,900 — filed Belton`<br>`Hickory $249,500 — filed Belton`<br>`Sherwood $265,000 — filed Belton`<br>`Cliffside $272,500 — filed Belton`<br>**`6 of 6`** | CONFIRMED |
| **G-TIER** | B4 2:20 | 8s | `PRICE PER SQUARE FOOT — 15 ACTIVE LISTINGS`<br>horizontal ladder, **sorted by $/sqft, not by list price**<br>`Low $151/sf ——————————— High $310/sf` | CONFIRMED |
| **G-6** | B4 3:00 | 7s | `TWO OF THE TOP FOUR AREN'T IN`<br>`MPR SECTIONS 1–9`<br><br>`$869,000 — Rancho Del Lago — built 2026`<br>`$665,000 — Campus At Lakewood Ranch — built 2019` | CONFIRMED |
| **G-VINTAGE** | B5 3:40 | 8s | **THE SPLIT, AGAIN — BY AGE**<br>`Filed "Morgans Point Resort" — median built 2012`<br>`Filed "Belton" — median built 1977`<br><br>`Not one listing carrying the town's name`<br>`was built before 2002.`<br>`All 8 pre-1980 listings are on the Belton side. 8 of 8.` | CONFIRMED |
| **G-7** | B5 4:15 | 6s | `WHAT'S FOR SALE vs WHAT SOLD`<br>`Active — median built 1979  (n=15)`<br>`Sold — median built 2000  (n=7)`<br><br>`No home built before 1985 sold.`<br><small>`7 closed sales · May 18 – July 16, 2026`</small> | CONFIRMED |
| **G-8** | B5 4:35 | 5s | `SEVEN SALES. SIXTY DAYS.`<br>`That's a small sample and I'm going to treat it like one.` | OPINION |
| **G-9** | B6 5:10 | 7s | `THE SECOND PRICE TAG`<br>`Roof age · Foundation history · Electrical panel`<br>`Plumbing material · HVAC age · Septic vs city sewer`<br><br>`Median active build year: 1979` | CONFIRMED |
| **G-10** | B7 6:05 | 8s | `THE HONEST GAP`<br>`Asking, per square foot (active):  $188`<br>`Sold, per square foot:            $175`<br>`Gap: 6.9%`<br><br><small>`Not the 33% you get comparing median prices — active homes are 32% larger.`</small> | CONFIRMED |
| **G-11** | B7 6:30 | 8s | `WHAT SOLD, vs WHAT IT FIRST ASKED`<br>`$195,000 ← first asked $225,000`<br>`$205,000 ← first asked $235,000`<br>`$210,000 ← first asked $229,900`<br>`$220,000 ← first asked $239,000`<br>`$225,000 ← first asked $235,000`<br>`$251,000 ← first asked $275,990`<br>`$255,000 ← first asked $299,900`<br>**`Median: about 91% of the original ask`**<br><small>`7 closed sales · May 18 – July 16, 2026`</small> | CONFIRMED |
| **G-12** | B7 6:50 | 6s | `7 OF 15 ACTIVE LISTINGS HAVE CUT PRICE`<br>`Cuts: −10.1% −6.8% −5.7% −4.7% −2.0% −1.8% −1.2%`<br>`Middle cut: −4.7%`<br><br><small>`Sellers testing — not sellers capitulating.`</small> | CONFIRMED |
| **G-13** | B8 7:15 | 9s | `FIVE THINGS THE MLS DIDN'T TELL ME`<br>`1. Lake access / dock — no such field exists. Zero of 29.`<br>`2. HOA — 27 of 29 say None. 2 say Mandatory.`<br>`3. Schools — 29 of 29 say Belton ISD.`<br>`4. Drive times — not in the data. Measure them yourself.`<br>`5. Condition — not in the data. That's the inspection.` | CONFIRMED |
| **G-14** | B8 7:50 | 7s | `VERIFY WITH:`<br>`Lake access, water rights, docks →`<br>`City of Morgan's Point Resort +`<br>`USACE Belton Lake Resource Manager's Office`<br>`HOA → the property's recorded documents`<br>`Schools → Belton ISD, for your exact address` | — |
| **G-15** | B10 9:20 | held | CTA card — see §10 | — |

**15 graphics specified.** Longest hold 9s (G-13, a five-item list that needs the time). No static frame
exceeds 9 seconds; the 7-second visual-change rule is satisfied by chip changes, build-on reveals, and
drone substrate running under every card.

## 9a. Two graphics that were cut, and why

- **The four-median ladder** ($330,000 → $273,250 → $232,450 → $220,000). Cut. Three of those four are
  *asking* prices — under-contract and pending homes have no sale price until they close — so the ladder
  narrates seller ask as buyer agreement, across four different cohorts of different-sized homes (§H4).
- **"Active median $330,000 vs sold median $220,000 = your negotiating room."** Cut. That 33% gap is
  mostly a size difference, not a discount (§H3). **G-10** replaces it with the real number, and says on
  screen why the bigger number is wrong — which is worth more trust than the bigger number was worth drama.

## 9b. Graphic-to-narration integrity check

Each graphic was checked against the line it plays under. The specific failure being guarded against: a
graphic sorted by list price under narration saying "list price is not the signal." **G-TIER is sorted by
$/sqft** for exactly that reason. If the edit re-sorts it by price to look tidier, the video contradicts
itself on screen.
