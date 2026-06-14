# Ground Truth Pack — Temple TX Investor Buy Boxes (video)

**Date:** 2026-06-13 | **MLS source:** `market-monitor/june-13-market-data.csv` (pulled 09:47, 4,987 records, 996 Temple SOLD)
**Lane:** INVESTOR ONLY. No BSW/military/relocation/buyer pivots.
**Math:** `cashflow_model.py` (this folder). All numbers computed, not estimated.

---

## A. THE CENTRAL HONEST FINDING (the spine of the video)

> ⚠️ **SUPERSEDED by §E2 (self-managed, canonical, 2026-06-13).** The table in this section reflects the early CONSERVATIVE (third-party-PM + 10% capex) run. Taylor confirmed he self-manages; under his profile THREE boxes are positive at 25% down (MTR +$301, renovated hospital 3-2 +$218, duplex +$183). Use §E2 for shipping numbers; this section is kept for the "passive owner" downside framing.

At standard investor leverage (**25% down, ~7.5% rate**) **and passive (third-party) management**, **every Temple buy box is negative or breakeven monthly cash flow.** This is not a flaw in the thesis — it IS the thesis. Most of Temple does NOT cash flow. The skill is knowing the *handful* of boxes where the rent-to-price ratio is good enough that positive cash flow is reachable — via self-management, a real rehab/buy-right discount, or more money down.

This matches Taylor's published position (`investing-temple-tx-v3.html`): positive CF requires "30–40% down" investors or buying well below market; public skepticism warning against ">15% CoC" promises.

**Relative ranking (rent-to-price, best→worst) — validates Taylor's thesis order:**
| Rank | Box | Rent-to-Price (mo) | CF @25% down | Verdict |
|---|---|---|---|---|
| 1 | 2-1 rehab → MTR (self-managed) | 1.15% | **+$122** | Best cash flow — IF self-managed + $1,900+ |
| 2 | Older duplex LTR | 0.88% | −$226 (→+$63 @40%) | Cash flows at moderate down |
| 3 | 3-2 rehab hospital/historic LTR | 0.89% | −$112 (→+$46 @40%) | 2nd best; needs down or buy-right |
| 4 | 76502 Cimarron/older (light CF) | 0.85% | −$244 | Mix play, light CF |
| 5 | Morgan's Point | 0.76% | −$521 | **Appreciation play, NOT cash flow @ leverage** |
| 6 | West Temple (Western Hills) | 0.69% | −$650 | Appreciation only ✓ |
| 7 | Canyon Creek 76502 (stretch) | 0.57% | −$1,064 | Appreciation only ✓ |

Rule of thumb surfaced by the model: **gross monthly rent-to-price ≥ ~0.8%** is the rough cash-flow line in a 7%+ world. Below that, you're buying appreciation.

---

## B. MLS ACQUISITION FACTS (verified today, 365-day Temple SOLD)

| Cohort | n (sold) | Median price | Median sqft | Median vintage | DOM | SP/LP |
|---|---|---|---|---|---|---|
| All Temple 3BR | 480 | $247,400 | 1,598 | 2008 | 69 | 100.0% |
| All Temple 2BR | 46 | $137,000 | 994 | 1952 | 39 | 96.3% |
| 3BR ≤ $180K (turnkey box) | 62 | $151,000 | 1,381 | 1962 | 81 | 95.7% |
| **Truly turnkey 3BR ≤$180K (SP/LP≥98% & DOM≤30)** | **6** | — | — | — | — | — |
| YearBuilt ≤1970, 3BR (hospital/historic proxy) | 88 | $190,000 | 1,660 | 1960 | 56 | 97.7% |
| 2BR pre-1975 (rehab→MTR candidates) | 33 | $129,000 | — | — | — | — |
| Canyon Creek (76502) | 26 | $330,684 | 2,046 | 1984 | 63 | 98.0% |
| Western Hills (West Temple) | 15 | $237,000 | 1,782 | 1979 | **27** | 99.6% |
| Cimarron (76502 entry) | 6 | $169,500 | — | 1953–2019 | — | — |
| Morgan's Point Resort (**Belton-addressed**) | 26 | $246,500 | 1,374 | 1998 | 75 | 99.8% |
| Older duplex / MF keyword (Temple+Belton) | ~4 | — | — | — | — | — |

**Validated claims:**
- ✅ "Only a few places cash flow" — median 3BR is $247K; at $1,650 rent that's deeply negative. True.
- ✅ "Turnkey 3-2 under $180K, don't come up often" — only **6 truly turnkey** in a full year of sales. Strong.
- ✅ "Get it under $180,000" — the sub-$180K 3BR cohort exists (62) but median vintage 1962 = most need work.
- ✅ "76502 = 1970s–2000s vintage" — Canyon Creek/Western Hills/Cimarron are 1979–1996 dominant. True.
- ✅ "Morgan's Point: good price + appreciation, deals come up but rare" — $246K median, n=26, SP/LP 99.8%.
- ✅ "Older duplex thin deal flow" — ~4 keyword hits in a year, mostly noise. Patient niche confirmed.

**Nuances / corrections the council must handle:**
- ⚠️ **West Temple "lower deal flow" + DOM 27**: Western Hills sells FAST (27 DOM, 99.6% SP/LP). Low *inventory*, not slow sales. Frame as "few come up, and when they do they go fast and at ask" — that's WHY the rent ratio is bad.
- ⚠️ **Morgan's Point is Belton-addressed** (Morgans Point Resort, Belton ISD-area lake community) — NOT a Temple ZIP. Must say "Belton-addressed lake community" on screen. Also distinct from **Lake Pointe** (Taylor's `best-areas-ltr.html` calls Belton/Lake Pointe negative-CF, cap 3.27%). Morgan's Point = the cheaper, older ($246K, 1998) lake stock.
- ⚠️ **No bath data in MLS** — "2-1" vs "3-2" is bed count + sqft proxy. State methodology honestly if a number is bed-based.
- ⚠️ **No lease data in any MLS pull** — all rents below are OPERATOR numbers (Taylor's P&L) + external triangulation, NOT MLS.

---

## C0. MLS LEASE COMPS — NOW VERIFIED (rental-data-bell.csv, 432 Temple, mostly leased; added 2026-06-13 10:40)

| Cohort | n (leased) | Median rent | IQR | Top 10% |
|---|---|---|---|---|
| Temple 2BR | 38 (28) | $1,100 | $950–$1,212 | $1,395 |
| Temple 3BR (all) | 269 (215) | $1,550 | $1,395–$1,750 | $1,870 |
| Temple 4BR | 104 (80) | $1,998 | $1,850–$2,200 | $2,500 |
| **Hospital 3BR 800–1,300sf (as-is)** | 81 (63) | **$1,395** | $1,250–$1,425 | $1,550 |
| **3BR 1,300–1,800sf (renovated/larger)** | 142 (117) | **$1,675** | $1,499–$1,795 | $1,850 |
| **Duplex (per-side)** | 81 (65) | **$1,300** | $1,200–$1,400 | $1,475 |
| Canyon Creek | 5 (5) | $1,595 | $1,500–$1,688 | — |
| Western Hills | 3 (3) | $1,650 | $1,600–$1,700 | — |

**THE NEW INSIGHT (rehab is the rent lever):** a small as-is hospital 3-2 leases at **$1,395** (−$222/mo @25% down). The same home renovated leases at **$1,650** (MLS 1,300–1,800sf median $1,675) → **breakeven @25% down, +$156 @40%**. The $30K rehab buys a ~$255/mo rent swing — the rehab IS the cash flow, not cosmetics.
**Reconciliation of operator claims:** $1,300/side duplex = **EXACT MLS match** ✅. Hospital $1,500–$1,650 = the *renovated* number (above the as-is median) ✅ with nuance. Canyon Creek $1,700–$1,750 = slightly above MLS leased median $1,595, reachable only at the top/larger end (4BR median $1,998 supports "some get $1,900").

## C. RENT ASSUMPTIONS (now MLS-VERIFIED, not just operator)

| Box | Operator rent | Triangulation verdict |
|---|---|---|
| 3-2 by hospital, 900–1,200 sqft | $1,500–$1,650 | ✅ Rentometer Temple 3BR SFR median **$1,695** (IQR $1,500–$1,850); live 76504 comps: 2019 S 9th (1,300sf) $1,550, 1809 S 13th $1,350, 1615 S 15th (updated) $1,850. Operator sits at/below median = conservative. |
| MTR by hospital (rehabbed 2-1) | $1,900 median | ✅ Furnished Finder Temple: **143 listings, stated median $2,000**, 2BR furnished median **$1,986**. $1,900 is ~4% BELOW market = conservative. Upside to ~$2,000. |
| Duplex 3-2 LTR | ~$1,300/side | ✅ Plausible-conservative (duplex sides often 2BR; 3BR side could fetch more). |
| Canyon Creek 76502 | $1,700–$1,750 (some $1,900 larger) | ✅ 76502 larger 3BR; Rentometer 3BR IQR top $1,850, 4BR median $2,000 supports "some get $1,900." |
| Historic district 3-2 | $1,500–$1,650 | ✅ = hospital district band. |

LTR baselines: Temple 2BR SFR median $1,100 (avg $1,252), 3BR median $1,695, 4BR median $2,000 (Rentometer 2026-06-13). MTR premium ~58% over LTR.

**ADU note:** Both hospital + historic districts occasionally allow an additional dwelling unit. Taylor's rule: NEVER underwrite on the ADU — too rare to count. (Do not promise it on camera.)

---

## D. CASH-FLOW MODEL ASSUMPTIONS (brain-anchored)

- Down: 25% base (sensitivity 40%/cash) | Rate: **7.375%** (verified June 2026) | Term 30yr
- Property tax: **2.0% EFFECTIVE** (Taylor 2026-06-13 — statutory 2.0–2.35% but Bell County assessed value runs ~10% under purchase when the owner protests + stays on it) | Insurance: **$2,400/yr**
- **Profile = Taylor's reality (set 2026-06-13):** LTR PM **7%** (his management fee; market 3rd-party = 10%); MTR **self-managed** (Furnished Finder). Vacancy 5% LTR / 10% MTR. **CapEx 5% on rehabbed homes / 10% on turnkey or as-is older homes** (old systems). MTR +$250/mo (utilities/furnishing). Rehab paid cash; finance only the purchase. Closing 3% (CoC denominator).
- **The lever = BUY RIGHT + REHAB**, not management: renovated hospital 3-2 **+$152** vs the *same house* turnkey-retail (no discount, 10% capex) **−$176** = a ~$330/mo swing. Management is secondary (winners stay positive even at the market 10% rate; e.g. renovated 3-2 still +$105). The MTR is the one box where self-management decides it (20% MTR mgmt → +$11).
- Earlier runs used 2.35% tax + a 3rd-party-or-0% PM split; this 2.0%-tax + 7%-PM set is canonical (per Taylor's operating numbers). Prior versions in git history.

---

## E. RESEARCH FINDINGS (external — verified June 2026)

**Financing (high confidence):**
- Investment 30yr fixed conventional (20–25% down): **7.1–7.6%, ~7.375% typical** (themortgagereports.com June 2026). ~0.5–1.0 pt above owner-occupied (~6.5%). DSCR ~6.75–7.25%.
- **Effective property tax 2.35%** (Bell CAD 2025: County 0.3128 + Temple City 0.6999 + Temple ISD 1.1372 + Temple College 0.2017 = 2.3516%). No homestead for investors. (Prior 2.2% anchor was low; use 2.35%.)
- Landlord/DP3 insurance: **$1,800–$2,500/yr** typical older Temple SFR (use ~$2,400 pier-and-beam upper-mid).
- PM: LTR **8–10%**; lease-up ~75% of one month. MTR PM **15–25%** (~20%) or self-managed.

**MTR demand (high confidence) — validates $1,900:**
- Furnished Finder Temple: **143 furnished listings (89 available), stated median $2,000/mo**, avg $1,946. 2BR furnished median **$1,986** (range $1,700–$2,600); 3BR median ~$2,300.
- $1,900 for a hospital-district 2-1 = ~4% below market = realistic-to-conservative.
- BSW Temple: ~**12,000 local employees**, 640-bed academic medical center, **125+ residency/fellowship programs** → structural MTR demand. MTR gross premium ~58% over LTR.

**LTR (high confidence):** Rentometer Temple 3BR SFR median **$1,695** (IQR $1,500–$1,850); 2BR $1,100; 4BR $2,000. Live 76504 (south-numbered streets) comps land $1,350–$1,850 by condition.

## E2. FINAL CASH FLOW — MLS-VERIFIED RENTS, TAYLOR'S INPUTS (rate 7.375%, tax 2.0% effective, ins $2,400, LTR PM 7%/MTR self-managed, capex 5% rehabbed/10% turnkey-older, vac 5% LTR/10% MTR; @25% / @40% down)

| Box | Rent (MLS) | RtP | CF @25% | CoC@25% | CF @40% | Verdict |
|---|---|---|---|---|---|---|
| **2-1 rehab → MTR, self-managed** | $1,900 | 1.15% | **+$353** | 5.4% | +$477 | ✅ strongest positive (7.1% cap); 20% MTR mgmt → +$11 |
| **3-2 hospital RENOVATED** | $1,650 | 0.92% | **+$152** | 2.5% | +$308 | ✅ positive even at market 10% mgmt (+$105) — rehab gets you here |
| **Older duplex LTR ($1,300/side)** | $2,600 | 0.88% | **+$91** | 1.1% | +$376 | ✅ positive; rent MLS-exact, ~0 sales = footnote (no price anchor) |
| 3-2 hospital AS-IS (no rehab, 10% capex) | $1,395 | 0.90% | −$127 | −3.2% | +$28 | negative until more down — why you rehab |
| Turnkey 3-2 (retail, 10% capex) | $1,550 | 0.86% | −$176 | −3.9% | +$5 | the buy-right gap vs renovated (+$152) |
| 76502 Cimarron/older | $1,500 | 0.73% | −$213 | −3.6% | — | appreciation mix |
| West Temple (Western Hills) | $1,650 | 0.67% | −$522 | −8.2% | — | appreciation only ✓ |
| Morgan's Point (Belton lake) | $1,650 est | 0.67% | −$508 | −8.0% | — | ⚠️ appreciation, NOT cash flow at leverage |
| Canyon Creek 76502 | $1,595 | 0.51% | −$1,041 | −12.6% | — | cleanest appreciation proof ✓ |

**The honest line for camera:** buy right and rehab, and **three** boxes throw off real cash at 25% down — even after paying management — the self-managed MTR (**+$353**), the renovated hospital 3-2 (**+$152**), and the older duplex (**+$91**). The **lever is buy-right + rehab**, not management: the renovated hospital 3-2 makes +$152 while the *same house* bought turnkey-retail loses −$176 (a ~$330/mo swing from the discount + the rehab dropping capex 10%→5%). The as-is and turnkey boxes go positive only with more money down (40%). Rent-to-price ≥ ~0.8%/mo is necessary but NOT sufficient — note as-is (0.90%) and turnkey (0.86%) are above the line yet still negative because of old-home capex; the rehab and the buy price decide it.

---

## F. CONSISTENCY ANCHORS (brain — maintain or consciously evolve)

- Hospital district = best cash-flow play (pier-and-beam, $55–150K acq, $15–40K rehab) — `neighborhoods.html`
- 76502 = power zip / growth corridor, $220–350K entry, Canyon Creek/Cimarron/Western Hills — `investing-in-temple-tx.html`
- South Pointe = newer no-rehab MTR play (10 min to BSW + Meta data center) — `investing-neighborhoods.html`
- "We post math, not price drops"; 100+ deals personally; speaks from P&L — voice anchor
- Foundation warning: nearly all hospital-district homes pier-and-beam on clay; budget structural engineer report + 5–10% ARV for foundation — `neighborhoods.html`
