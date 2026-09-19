# Bell County Property Tax Rates — Verified Reference
> Full verification report. Generated 2026-09-19.
> Method: Bell CAD 2025 Tax Rate Chart + per-parcel jurisdiction records pulled from
> Bell CAD's own property search (250+ Bell County parcels, two independent samplers).
> The operational summary lives in `reference/TEMPLE-TX-DATA-VAULT.md`; this is the audit trail.

## PROPERTY TAX (Bell County CAD — 2025 Certified Rates, per $100 Valuation)

> **Rebuilt from primary sources 2026-09-19.** This section replaces the previous "County + City + ISD + ESD1" table, which was wrong for every city. See **What Changed and Why** below before reusing any number from old content.

### 1. HEADLINE NUMBER — TEMPLE

**Temple, inside city limits, Temple ISD — tax year 2025 combined rate: `2.387677` per $100 = `2.39%`**

- Tax year: **2025** (rate adopted Aug–Sep 2025, billed Oct 2025, due **Jan 31, 2026**)
- Verified: **2026-09-19**
- Source: Bell CAD 2025 Tax Rate Chart (30-Sep-25) + Bell CAD per-parcel jurisdiction records
- Status: **CONFIRMED** — matches Taylor's published page at templetxhomes.net/temple-tx-property-taxes/ to six decimals

This number replaces the disputed **2.25%** (vault) and **2.366%** (market_data.json). Both were wrong.

**This is not the only Temple rate.** In-city Temple has four combined rates depending on school district and watershed overlay:

| In-city Temple variant | Combined rate | Notes |
|---|---|---|
| **Temple ISD, no Elm Creek (modal — use this)** | **2.387677** | 11 of 14 sampled in-city parcels |
| City of Temple **+ Belton ISD** | 2.399877 | Confirmed on 8501 Iowa Ave, 76502 |
| Temple ISD **+ Elm Creek Watershed** | 2.410477 | Confirmed on 1111 Hillcrest Rd and 1930 E Young Ave, 76501 |
| Belton ISD + Elm Creek | 2.422677 | [VERIFY — arithmetic only, not observed on a parcel] |

**A "Temple, TX" mailing address does not mean inside city limits and does not mean Temple ISD.** Bell CAD counts 47,787 City of Temple accounts but only 32,059 Temple ISD accounts. Always say "verify the exact address."

---

### 2. TEMPLE ENTITY-BY-ENTITY (auditable sum)

| Code | Entity | M&O | I&S | Rate per $100 |
|---|---|---|---|---|
| STEM | Temple ISD | 0.802200 | 0.335000 | **1.137200** |
| TTE | City of Temple | 0.375400 | 0.324500 | **0.699900** |
| CB | Bell County | 0.267300 | 0.045500 | **0.312800** |
| JTC | Temple College (Temple Junior College District) | 0.146000 | 0.055700 | **0.201700** |
| RRD | Bell County Road District | 0.019900 | 0.000000 | **0.019900** |
| RSBIO | Temple Health & Bioscience District | 0.013947 | 0.000000 | **0.013947** |
| WCLW | Clearwater UWCD | 0.002230 | 0.000000 | **0.002230** |
| | **COMBINED** | | | **2.387677** |

**The arithmetic:**
`1.137200 + 0.699900 + 0.312800 + 0.201700 + 0.019900 + 0.013947 + 0.002230 = 2.387677`

**Entities that do NOT apply inside Temple city limits (all confirmed absent on 14 sampled in-city parcels):**

| Code | Entity | Rate | Why it does not apply |
|---|---|---|---|
| ESD1 | Bell County ESD #1 | 0.100000 | Salado-area emergency services district serving **unincorporated** Bell County (9,324 accounts countywide). Temple runs Temple Fire & Rescue. **This is the vault's central error.** |
| JCTC | Central Texas College | 0.090000 | Tracks Killeen ISD territory. A parcel is in Temple College's district **or** CTC's, never both. |
| WWC3 / WWC6 | Bell Co WCID #3 / #6 | 0.0358 / 0.0243 | Absent on all 14 in-city Temple parcels sampled |
| MUD1 / MUD2 / MUDRF | Bell Co MUDs | 0.783 / 0.950 / 1.000 | See MUD warning, §5 |
| WXC | Donahoe Creek | 0.022400 | Rural east/southeast Bell County |
| All other cities / ISDs | — | — | Municipal and school boundaries are mutually exclusive |

**Watch this one:** WEC (Elm Creek Watershed, 0.022800) **does apply to part of east Temple** — confirmed on real in-city 76501 parcels. It is not a rural-only district. [VERIFY — no boundary map obtained; share of Temple parcels affected is unmeasured]

**How this was proven:** Bell CAD's own per-parcel property search (esearch.bellcad.org / esearchgsa.bellcad.org) prints each property's "Property Taxing Jurisdiction" table and computes the combined rate itself. Example — **908 N 6TH ST, TEMPLE 76501 (prop_id 219)**: Bell County 0.312800 | Temple College 0.201700 | Bell County Road 0.019900 | Temple Health and Bioscience 0.013947 | Temple ISD 1.137200 | City of Temple 0.699900 | Clearwater U.W.C.D. 0.002230 — **Combined Tax Rate: 2.387677**. Replicated on 10 more in-city Temple addresses.

---

### 3. CITY COMPARISON — TY2025 CERTIFIED (non-homestead / nominal)

| City (school district) | Combined rate | Effective % | $300K annual | $300K monthly | Confidence |
|---|---|---|---|---|---|
| **Temple** (Temple ISD) | **2.387677** | **2.39%** | $7,163.03 | $596.92 | CONFIRMED |
| **Killeen** (Killeen ISD) | **2.028430** | **2.03%** | $6,085.29 | $507.11 | CONFIRMED |
| **Belton** (Belton ISD) | **2.006830** | **2.01%** | $6,020.49 | $501.71 | CONFIRMED |
| **Harker Heights** (Killeen ISD) | **1.832730** | **1.83%** | $5,498.19 | $458.18 | CONFIRMED |

**Footnote — the stacks are NOT the same set of entities. Never hand-assemble a city's rate; each one differs.**

| City | Entities in the stack | Count |
|---|---|---|
| **Temple** | Temple ISD 1.1372 + City of Temple 0.6999 + Bell County 0.3128 + **Temple College 0.2017** + Road 0.0199 + **Health & Bio 0.013947** + Clearwater 0.00223 | 7 |
| **Killeen** | Killeen ISD 0.8778 + City of Killeen 0.7014 + Bell County 0.3128 + **Central Texas College 0.0900** + **WCID #6 0.0243** + Road 0.0199 + Clearwater 0.00223 | 7 |
| **Belton** | Belton ISD 1.1494 + City of Belton 0.5225 + Bell County 0.3128 + Road 0.0199 + Clearwater 0.00223 — **no junior college at all** | 5 |
| **Harker Heights** | Killeen ISD 0.8778 + City of Harker Heights 0.5300 + Bell County 0.3128 + **Central Texas College 0.0900** + Road 0.0199 + Clearwater 0.00223 | 6 |

**Within-city variants that are real and must be disclosed:**

| Variant | Rate | Incidence in parcel sampling |
|---|---|---|
| Temple + Elm Creek Watershed (+0.0228) | 2.410477 | 2 of 14 in-city Temple parcels (east Temple) |
| Belton + WCID #6 (+0.0243) | 2.031130 | 49 of 154 in-city Belton parcels (~32%, two independent samples) |
| Killeen **without** WCID #6 (−0.0243) | 2.004130 | 22 of 70 in-city Killeen parcels (~31%) |
| Harker Heights + WCID #6 (+0.0243) | 1.857030 | ~25–40% of Heights parcels [VERIFY — samples of 8 and 12 disagree; true split unmeasured] |

**Safe phrasing for each city:**
- Temple: "about 2.39%"
- Killeen: "about 2.0% — 2.00% to 2.03% depending on the flood-control district"
- Belton: "about 2.01%, or about 2.03% in the Nolan Creek water district"
- Harker Heights: "about 1.83% to 1.86%"

**Evidence base:** 154 in-city Belton parcels (two independent samplers, 100% agreement), 70 in-city Killeen parcels (state truth-in-taxation database), 14 in-city Temple parcels, 20 Harker Heights parcels + the City of Harker Heights' own .gov explainer listing exactly those six entities. Bell County ESD #1 appeared on **zero** in-city parcels in any city.

---

### 4. INVESTOR vs HOMEOWNER — $300,000 HOME, TY2025

#### Temple — NO HOMESTEAD (investor / non-owner-occupied)

| Entity | Taxable | Rate | Tax |
|---|---|---|---|
| Temple ISD | $300,000 | 1.137200 | $3,411.60 |
| City of Temple | $300,000 | 0.699900 | $2,099.70 |
| Bell County | $300,000 | 0.312800 | $938.40 |
| Temple College | $300,000 | 0.201700 | $605.10 |
| Bell County Road | $300,000 | 0.019900 | $59.70 |
| Health & Bioscience | $300,000 | 0.013947 | $41.84 |
| Clearwater UWCD | $300,000 | 0.002230 | $6.69 |
| **TOTAL** | | **2.387677** | **$7,163.03/yr — $596.92/mo — 2.3877%** |

#### Temple — WITH STANDARD HOMESTEAD (owner-occupied, under 65)

| Entity | Exemption | Taxable | Tax |
|---|---|---|---|
| Temple ISD | $140,000 (state) | $160,000 | $1,819.52 |
| City of Temple | greater of 20% or $5,000 → $60,000 | $240,000 | $1,679.76 |
| Temple College | greater of 20% or $5,000 → $60,000 | $240,000 | $484.08 |
| Bell County | **none** | $300,000 | $938.40 |
| Bell County Road | **none** | $300,000 | $59.70 |
| Health & Bioscience | **none** | $300,000 | $41.84 |
| Clearwater UWCD | **none** | $300,000 | $6.69 |
| **TOTAL** | | | **$5,029.99/yr — $419.17/mo — 1.6767% of market value** |

**Homestead is worth $2,133.04/yr in Temple at $300K.** That is the single biggest line separating an owner-occupant pro forma from an investor pro forma.

#### All four cities, $300,000 home

| City | Investor (no exemption) | Homeowner (homestead) | Investor penalty |
|---|---|---|---|
| Temple | $7,163.03 / $596.92 mo / 2.3877% | $5,029.99 / $419.17 mo / 1.6767% | **$2,133.04/yr** |
| Killeen | $6,085.29 / $507.11 mo / 2.0284% | $4,856.37 / $404.70 mo / 1.6188% [VERIFY] | $1,228.92/yr |
| Belton | $6,020.49 / $501.71 mo / 2.0068% | $4,411.33 / $367.61 mo / 1.4704% | $1,609.16/yr |
| Harker Heights | $5,498.19 / $458.18 mo / 1.8327% | $4,269.27 / $355.77 mo / 1.4231% | $1,228.92/yr |

[VERIFY — Killeen homeowner figure] The Killeen homestead number above applies **only** the $140,000 school exemption. The chart shows City of Killeen $20,000 and Central Texas College $15,000, but column-geometry re-extraction of the PDF shows the equivalent Bell County / Harker Heights / Road / Clearwater figures sit in the **Local Over-65 and Local Disabled** columns, not homestead. If Killeen's $20,000 and CTC's $15,000 turn out to be general homestead exemptions, the Killeen homeowner bill drops to about **$4,647**. Confirm on a live homesteaded 76541/76542 parcel before publishing a Killeen owner-occupant number.

#### ⭐ WORKING NUMBERS FOR INVESTOR UNDERWRITING

- **Temple: use 2.39% of assessed value — $23.88 per $1,000 — $7,163/yr per $300K — $597/mo.**
- Killeen: 2.03% — $20.28 per $1,000
- Belton: 2.01% — $20.07 per $1,000
- Harker Heights: 1.83% — $18.33 per $1,000

**Three rules that go with these numbers:**
1. **Out-of-state buy-and-hold investors never get the homestead exemption.** The no-exemption number is the only correct one for a rental pro forma.
2. **Bell CAD reassesses annually, and assessed value drives the bill, not purchase price.** The 10% homestead appraisal cap (Tax Code §23.23) is unavailable to investors, and it resets for a new owner-occupant buyer too.
3. Bell CAD does **not** appraise below purchase price. The Texas Comptroller's 2025 Appraisal District Ratio Study (Bell CAD, updated 2026-08-25) puts the **median level of appraisal on single-family at 1.00** (2,046 ratios, COD 7.04), and the 2023 study put it at 1.02. **Underwrite at full market value.** (This retires the old vault line "Bell County CAD typically appraises below purchase price.")

#### Exemption facts confirmed for TY2025

- School district general residence homestead: **$140,000** (state, raised by Texas Prop 13 in Nov 2025, retroactive to 1-Jan-2025). The old vault figure of $100,000 is stale.
- Additional over-65 / disabled: **$60,000** school (up $10,000).
- **Bell County, Bell County Road, Clearwater, Health & Bio, City of Belton, City of Harker Heights, and CTC grant NO general homestead exemption.** Their chart figures (16,670 / 10,000 / 5,000 / 15,000) are **Local Over-65 and Local Disabled** amounts. Confirmed by PDF column geometry and by live parcels where those entities show taxable = full market value.
- **City of Temple and Temple College each grant greater of 20% or $5,000.** Confirmed: 18,553 city homesteads totaling $940,326,129 = $50,683 average on an average value that makes it exactly 20%.
- City of Killeen and Central Texas College are flagged **FRZ/ONLY** for over-65 — a tax ceiling, not a dollar exemption. [VERIFY — confirm the FRZ reading with Bell CAD before publishing retiree content]

---

### 5. MUD WARNING — AND THE REAL TEMPLE TRAP

**No MUD taxes any property inside Temple city limits.** Zero of 14 sampled in-city Temple parcels carried a MUD. All three Bell County MUDs are elsewhere and small:

| Code | District | Rate | Where it actually is | Size (2025) |
|---|---|---|---|---|
| MUD1 | Bell County MUD #1 | **0.783000** | ~534 acres near FM 1670 / Lampasas River, Belton–Morgan's Point side (Stoneoak area). Created by HB 2521 (82R) | 1,687 accounts, $334M |
| MUD2 | Bell County MUD #2 | **0.950000** | South of Chaparral & Trimmier Roads, **outside** Killeen city limits | 426 accounts, $32.4M |
| MUDRF | River Farm MUD No. 1 | **1.000000** | 6101 Toll Bridge Road, Belton 76513 — a new, developing district | 3 accounts, $935,627 |

**If a buyer does land in one**, the MUD rate stacks on top of the base rate for that location:

| Scenario | Base stack | + MUD | Total | Status |
|---|---|---|---|---|
| Unincorporated Belton-ISD parcel (CB + RRD + SBEL + WCLW) | 1.484330 (confirmed on 5647 Wagon Rd) | MUD #1 +0.783 | **≈ 2.26733** | [VERIFY — arithmetic; no MUD #1 parcel pulled] |
| Unincorporated Killeen-ISD parcel (CB + RRD + SKIL + JCTC + WCLW) | 1.302730 | MUD #2 +0.950 | **≈ 2.25273** | [VERIFY — one such parcel observed, full stack not captured] |
| Unincorporated Belton-ISD parcel | 1.484330 | River Farm +1.000 | **≈ 2.48433** | [VERIFY — arithmetic only] |

**THE ACTUAL TEMPLE NEW-CONSTRUCTION TRAP IS A PID, NOT A MUD.**
Chapter 372 **Public Improvement District assessments** — including the **North Point PID** in north Temple — are **assessments collected by the city, not ad valorem taxes**, so they appear **nowhere** on the Bell CAD tax rate chart and nowhere in the 2.39%. Bell CAD's chart lists only one PID in the entire county (Salado Sanctuary East). A "2.39%" quote can understate a new-construction buyer's real annual obligation by roughly **$1,000–$4,000/yr**. [VERIFY — no complete list of Temple-area PIDs or their per-lot assessments obtained]

**Content line that is accurate and nobody else is saying it:** "There's no MUD inside Temple city limits. The thing that actually shows up on a new-construction buyer's bill here is a PID assessment — and it isn't on the tax rate chart at all, so nobody catches it until closing."

**Second trap, east Temple:** Elm Creek Watershed adds 0.0228 → 2.410477. Confirmed on real 76501 residential streets.

---

### 6. WHAT CHANGED AND WHY THE OLD 2.25% WAS WRONG

The old vault table was labeled **"Combined Effective Tax Rates (County + City + ISD + ESD1)"**. That formula is the bug. It is wrong for every incorporated city in Bell County, in the same two ways.

**Old Temple: 2.2499 = 0.3128 (county) + 0.6999 (city) + 1.1372 (ISD) + 0.1000 (ESD1)**

**Error 1 — wrongly INCLUDED:**
- ESD1, Bell County ESD #1, **0.100000**. It serves **unincorporated** Bell County, contracts with Salado Fire & Rescue (HQ 3520 FM 2484, Salado), and covers 9,324 accounts countywide — 4.9% of the county. It appeared on **zero** in-city parcels in Temple, Belton, Killeen or Harker Heights. Temple has its own fire department.

**Error 2 — OMITTED four real entities totaling 0.237777:**
- Temple College (JTC) **0.201700**
- Bell County Road District (RRD) **0.019900** — countywide, not rural-only; the county publishes it as part of one combined county rate
- Temple Health & Bioscience (RSBIO) **0.013947** — boundaries coextensive with the City of Temple by statute (Tex. Spec. Dist. Local Laws Code §3831.004)
- Clearwater UWCD (WCLW) **0.002230** — all of Bell County

**Net error: 0.237777 − 0.100000 = 0.137777 per $100, understated.**
- On a $300,000 property: **$413.33/yr** too low
- On a $280,000 property: **$385.78/yr** too low

**Every city row was wrong the same way:**

| City | Old vault | Correct | Direction | Error on $300K |
|---|---|---|---|---|
| Temple | 2.2499 | **2.387677** | understated 0.1378 | −$413.33/yr |
| Belton | 2.0847 | **2.006830** | **overstated** 0.0779 | +$233.61/yr |
| Killeen | 1.9920 | **2.028430** | understated 0.0364 | −$109.29/yr |
| Harker Heights | 1.8206 | **1.832730** | understated 0.0121 | −$36.39/yr |

Old "$280K annual" column was also wrong. Correct TY2025 values on $280K, non-homestead: Temple **$6,685.50**, Killeen **$5,679.60**, Belton **$5,619.12**, Harker Heights **$5,131.64**. That column was always a no-exemption figure and must be labeled as such so nobody quotes it to an owner-occupant.

**market_data.json** (`/home/user/claude-social-media-manager/market_data.json`): `county_effective_non_homestead ~2.366%` is low by 0.021677 per $100 = **$65.03/yr on $300K**. The `"2.4%-2.7%"` range has no support in any Bell CAD document for an in-city Temple parcel. Remove or replace both.

**Also retired from this section:**
- "Bell County CAD typically appraises below purchase price" — contradicted by the state ratio study (median 1.00). What was probably meant is the 10% homestead **cap**, which is a value limitation for existing owners and does not help a buyer.
- "reference approximately 2.1–2.3% for Temple" — both ends are below the verified 2.39%.
- "use 2.25% for pro formas" — replaced by 2.39%.
- "Homestead exemption: $100K off school taxes" — it is $140,000.
- "Killeen is lowest of the three major cities" — **false**. Harker Heights is lowest (1.83%); Belton is lowest of Temple/Belton/Killeen (2.01%).

**Content audit needed:** any investor pro forma, DOTW cash-flow table, GMB post, blog or video that used 2.25% / 2.1–2.3% for Temple is understating taxes by about $413/yr per $300K of value. Search and correct.

---

### 7. RATE-YEAR GUIDANCE — WHAT TO SAY ON CAMERA

**The trap:** entities publish rates by **fiscal year**, and fiscal years do not line up. City of Temple runs Oct 1–Sep 30, so its "FY2026" rate **is the 2025 tax-year rate**. Temple College, Temple ISD and Central Texas College run Sept 1–Aug 31, so CTC's "FY2026" rate of 0.090 is also **tax year 2025**, while Temple ISD's "2026-27" rate of 1.0619 is **tax year 2026**. Two entities, two meanings of "2026." **This is how the vault's numbers rotted.**

**Three hard rules:**
1. **Never say "the FY____ tax rate." Always say "the 2025 tax-year rate."** Tax year is unambiguous across every entity; fiscal year is not.
2. **Anchor to the bill, not the budget.** "The rate on the bill you get this October" is something a homeowner can verify. "FY2027" is not.
3. **Never mix years inside one combined rate.** A stack must be all-2025 or all-2026.

#### TY2026 status as of 2026-09-19 — rates HAVE moved

| Entity | TY2025 | TY2026 | Status |
|---|---|---|---|
| Temple ISD | 1.137200 | **1.061900** | CONFIRMED — adopted Sept 14, 2026 (M&O 0.7509 + I&S 0.3110); lowest in 15+ years |
| City of Temple | 0.699900 | **0.750000** | CONFIRMED — adopted Aug 27, 2026 (M&O 0.4008 + I&S 0.3492) |
| Bell County | 0.312800 | **0.299500** | CONFIRMED — adopted Aug 24, 2026, 3-1 |
| Bell County Road | 0.019900 | **0.046800** | CONFIRMED — county total published as 0.3463 |
| Temple College | 0.201700 | 0.249800 | [VERIFY — proposed = voter-approval rate, hearing Aug 24, 2026; no adoption record found] |
| Health & Bioscience | 0.013947 | 0.013947 | [VERIFY — no 2026 rate published; held flat] |
| Clearwater UWCD | 0.002230 | 0.002216 | [VERIFY — single source, state TNT database] |
| **TY2026 Temple combined** | | **≈ 2.4242 (~2.42%)** | [VERIFY — rests on the unconfirmed Temple College number] |

Four confirmed components alone sum to **2.1582**; with the proposed college rate, **2.4080**. **Do not publish 2.42% as a certified figure yet.**

#### ⭐ EVERGREEN VIDEO / BLOG — safe phrasing (no year lock)

> "Temple property taxes run right around **two and a half percent** of assessed value — call it **$600 a month per $300,000** if you're not getting a homestead exemption. Your exact rate depends on the address, because Temple homes sit in two different school districts and some sit in a watershed district. Look up the parcel at bellcad.org before you underwrite anything."

Rules for evergreen: no decimal precision, no tax-year number, "right around," and always the "verify the address" close. This stays true through several rate cycles.

#### ⭐ TIME-STAMPED VIDEO — safe phrasing (late Sept 2026)

> "Two numbers, and don't mix them up. The bill you **paid** back in January was the **2025 tax year**: combined **$2.3877 per $100** in Temple — about **2.39%**. The bill **coming** in October is the **2026 tax year**, and the rates just changed. Temple ISD came **down** seven and a half cents to **1.0619**, lowest in fifteen years. Bell County came **down** to **0.2995**. But the City of Temple went **up** to **0.7500**, the county road rate more than doubled to **0.0468**, and Temple College is proposing a jump to **0.2498**. Net, you're looking at roughly **2.42%** — slightly up, even though the two biggest line items went down.
>
> One honest caveat: the City's 0.75 is actually **below** its no-new-revenue rate, so on an average homestead the city's own numbers show the bill going **down** about $103 a year. Higher rate, lower bill — that's exemptions and taxable values moving, not spin.
>
> I'm still verifying Temple College's final adopted number and two small districts. Bell CAD publishes the consolidated chart around the end of September — when it's up, I'll post the exact figures. I'm Taylor Dasch with EG Realty."

That script is publishable today, accurate, flags its own uncertainty, and builds in a reason to come back.

#### Never say
- "the FY2026 rate" (ambiguous — two different tax years depending on the entity)
- "2.25%" or "2.1–2.3%" (wrong)
- "Temple is 2.39%" with no address caveat (Belton ISD and Elm Creek parcels differ)
- "Killeen is the lowest of the three major cities" (Harker Heights is lower)
- "a MUD could add 1% in Temple" (no Temple MUD — say **PID** instead)

#### Bell County annual tax calendar (Bell CAD 2025 Annual Report)
| Date | Event |
|---|---|
| January 1 | Valuation date; exemption eligibility set |
| January 31 | Prior-year taxes due |
| February 1 | Delinquent — 6% penalty + 1% interest begins; 12% penalty July 1 |
| April 1 | Appraisal notices mailed (Tax Code §25.19) |
| May 15 | ARB protest deadline, or 30 days after the notice is **mailed**, whichever is later (§41.44) |
| July 25 | CAD certifies the appraisal roll |
| Aug–Sep 30 | Taxing units adopt rates (§26.05) |
| October | Tax statements mailed |

TY2026 bills mail October 2026, due **Jan 31, 2027** — which is a **Sunday**. [VERIFY — under Tax Code §1.06 payment Monday Feb 1, 2027 should be timely, but Bell CAD has not published this; confirm with the tax office before putting it in content, the margin is one day and the penalty is 6%]

---

### 8. FRESHNESS BLOCK

```
PROPERTY TAX SECTION
Rates:            Tax year 2025 (certified)
Verified:         2026-09-19
Verified by:      Bell CAD 2025 Tax Rate Chart + per-parcel jurisdiction records
                  (2 independent samplers, 250+ Bell County parcels)
Primary source:   https://bellcad.org/wp-content/uploads/2025/09/2025-Tax-Rate-Chart.pdf
Parcel source:    https://esearch.bellcad.org/Property/View/<prop_id>
                  https://esearchgsa.bellcad.org/Property/View/<prop_id>   (no captcha)
                  https://bell.countytaxrates.com  (state TNT database, per-parcel)
Local copy:       /home/user/claude-social-media-manager/data/2025-Tax-Rate-Chart.pdf
Adopted rates:    https://bellcad.org/adopted-tax-rates-and-exemptions/
2026 TNT data:    https://bellcad.org/tax-rate-calculation-data/

NEXT RE-CHECK:    2026-10-05  — Bell CAD 2026 chart is expected within 1-3 weeks
                              of 2026-09-19 (the 2025 chart was dated 30-Sep-25)
ANNUAL TRIGGER:   September 1  (NOT October 1 — rates are adopted in AUGUST;
                              an Oct 1 flag fires six weeks after the data changes)
HARD BLOCK:       Do not publish a TY2026 combined rate until the Bell CAD 2026
                  chart posts or Temple College's adopted rate is confirmed.
```

---

### 9. OPEN ITEMS

| # | Open item | Impact | What closes it |
|---|---|---|---|
| 1 | **Temple College TY2026 adopted rate** (proposed 0.2498, hearing Aug 24 2026) | Only unconfirmed component of the ~2.4242 TY2026 Temple rate. Proposed = voter-approval, so it cannot be higher, but could be lower | Bell CAD 2026 chart, or templecollege.edu board minutes |
| 2 | **Temple Health & Bio and Clearwater TY2026 rates** | 0.016177 combined = 0.7% of the Temple total. Estimate is robust either way | Bell CAD 2026 chart |
| 3 | **Elm Creek Watershed boundary inside Temple** | Determines how many Temple homes pay 2.410477 instead of 2.387677 (+$68/yr per $300K). Confirmed on 2 of 14 parcels but unmeasured | Pull 50+ east-Temple 76501 parcels via esearchgsa.bellcad.org, or obtain a WEC boundary map |
| 4 | **WCID #6 share in Belton / Killeen / Harker Heights** | ±0.0243 = $72.90/yr per $300K. Sampling gives ~32% Belton, ~31% Killeen (absent), 25–40% Heights. bcwc6.com boundary map is behind a login | Larger parcel sample, or a boundary shapefile |
| 5 | **City of Killeen $20,000 and CTC $15,000 — homestead or over-65?** | $209/yr on a Killeen owner-occupant bill; the homeowner figure in §4 is marked [VERIFY] because of it | Pull one homesteaded 76541/76542 parcel and read the per-entity taxable values |
| 6 | **Temple-area PID list and per-lot assessments** (North Point and others) | $1,000–$4,000/yr understatement for new-construction buyers — the largest single gap in this section | City of Temple finance department — Chapter 372 service and assessment plans |
| 7 | **TY2026 rates single-sourced from the state TNT database**: Killeen ISD 0.8622, CTC 0.0943, Clearwater 0.002216; City of Killeen 0.7301; City of Belton 0.5619; Belton ISD 1.1177 | Needed before any 2026 comparison table | Bell CAD 2026 chart |
| 8 | **Harker Heights TY2026 city rate** — sources conflict: held at 0.5300 vs 0.5472 proposed, final vote ~Sept 8, 2026 | Blocks a 2026 Harker Heights number entirely | harkerheights.gov council minutes, or Bell CAD 2026 chart |
| 9 | **Jan 31, 2027 falls on a Sunday** — §1.06 next-business-day reading is unpublished | One-day margin, 6% penalty | Call the Bell County Tax Assessor-Collector |
| 10 | **Belton ISD / Killeen ISD homestead behavior on non-school entities** confirmed on parcels; **City of Temple 20% homestead** confirmed from exemption-roll aggregates only | Low — two independent confirmations exist | Pull one homesteaded in-city Temple parcel and read City of Temple taxable value |

**Reusable tooling:** a parcel-jurisdiction lookup script is at `/tmp/claude-0/-home-user-claude-social-media-manager/196cb4ed-49d7-5311-8c03-c7a98b607e11/scratchpad/survey.py`. It takes Bell CAD prop_ids and returns the CAD's own entity stack per parcel — a primary source, and the fastest way to settle any "which entities tax X" question. **Recommend promoting it into `scripts/`** so tax content stays defensible. Parcel IDs come from `/home/user/claude-social-media-manager/data/BELL_CAD_RESIDENTIAL.csv`.

**Note on citations:** do **not** cite Tex. Educ. Code §130.171 or §130.202 as authority for which junior college taxes a property. Both statutes define **service areas**, which are far larger than the taxing districts — §130.202 lists Belton ISD inside Temple College's service area, and Belton pays no Temple College tax. Cite the per-parcel Bell CAD records instead.

---

**Files needing correction from this section:**
- `/home/user/claude-social-media-manager/reference/TEMPLE-TX-DATA-VAULT.md` — replace the whole PROPERTY TAX section (lines ~64–90), and change the section-freshness line from `Property Tax (CAD): 2025 rates — next refresh due 2026-10-01` to `next refresh due 2026-09-01`
- `/home/user/claude-social-media-manager/market_data.json` — remove `county_effective_non_homestead ~2.366%` and the `2.4%-2.7%` range
- `https://templetxhomes.net/temple-tx-property-taxes/` — **currently correct for TY2025**, but its 2.3877 becomes last year's number the moment the Bell CAD 2026 chart posts. Queue the refresh now; the page title already says "(2026)"