# TEMPLE TX DATA VAULT — Single Source of Truth
## Every content skill pulls from this file. Prevents number drift across videos, pages, and social.
## Last verified: 2026-03-21 (Property Tax section re-verified 2026-09-19)
## Next review due: 2026-05-01
## UPDATE PROTOCOL: Review monthly on the 1st. Flag any data point older than 90 days.
## SECTION FRESHNESS:
##   Market Data (MLS): 2026-03-17 — next refresh due 2026-04-17
##   Property Tax (CAD): TY2025 certified — VERIFIED 2026-09-19 — next refresh due 2026-10-05
##     (annual trigger is SEPTEMBER 1, not Oct 1 — Bell County rates are adopted in August)
##   Assessed Values: 2025 data — next refresh due 2026-10-01
##   Military/Fort Hood: 2025 BAH — next refresh due 2027-01-01
##   BSW Medical: 2025 data — next refresh due 2026-09-01
##   Population: 2024 Census estimate — next refresh due 2026-07-01
##   Key Employers: 2026-03-21 — next refresh due 2026-06-21
##   School Districts: TEA 2024 — next refresh due 2026-10-01
##   Distances: Static — no refresh needed
##   Compliance: Review quarterly — next 2026-07-01

---

## MARKET DATA (From MLS Export — March 2026)

### Active Listings (Resale, Temple Area)
- Total active listings: ~4,982
- Median list price (all Temple): **$270,000**
- Mean list price: $288,824
- Median $/sqft: $157.41
- Price range: $1,850 – $2,000,000

### Active by ZIP
| ZIP | Active | Median List | Mean List | Primary Areas |
|-----|--------|------------|-----------|---------------|
| 76502 | 4,751 | **$300,000** | $333,942 | Canyon Creek, Lake Pointe, Bella Terra, Legacy Ranch, North Temple |
| 76504 | 1,192 | **$225,000** | $226,311 | Western Hills, South Temple, older Temple |
| 76513 | 2,800 | **$340,890** | $403,391 | Belton, Morgan's Point, Salado-adjacent |

### Sold Data (Recent Closed)
- Median close price: **$270,000**
- Mean close price: $285,690
- Total closed in dataset: 4,453

### Rental Market (Active Listings)
| ZIP | All Rentals | Median Rent | 3BR Count | 3BR Median | 3BR Range |
|-----|------------|-------------|-----------|------------|-----------|
| 76504 | 424 | $1,400 | 251 | **$1,495** | $750–$2,250 |
| 76513 | 364 | $1,895 | 174 | **$1,800** | $995–$2,850 |

### Investment Metrics
- Investor buy box: $140K–$260K
- Target cap rate range: 6–8%
- Average cap rate for 3/2 rentals: [NEEDS UPDATE — calculate from specific comps]
- $140K = MTR entry point

---

## PROPERTY TAX (Bell County CAD — 2025 Certified Rates, per $100 Valuation)

> **Rebuilt from primary sources 2026-09-19.** The previous "County + City + ISD + ESD1"
> table was wrong for **every** city. Full audit trail and open items:
> `research/BELL-COUNTY-TAX-RATES-2026-09-19.md`

### Headline — Temple

**Temple, inside city limits, Temple ISD, tax year 2025: `2.387677` per $100 = `2.39%`**

Replaces the disputed 2.25% (this file) and 2.366% (`market_data.json`). Both were wrong.
Verified against Bell CAD per-parcel records — e.g. 908 N 6TH ST, Temple 76501 (prop_id 219),
where Bell CAD itself prints "Combined Tax Rate: 2.387677". Replicated on 10 more in-city addresses.

| Code | Entity | Rate per $100 |
|------|--------|--------------|
| STEM | Temple ISD | 1.137200 |
| TTE | City of Temple | 0.699900 |
| CB | Bell County | 0.312800 |
| JTC | Temple College (Temple Junior College District) | 0.201700 |
| RRD | Bell County Road District | 0.019900 |
| RSBIO | Temple Health & Bioscience District | 0.013947 |
| WCLW | Clearwater UWCD | 0.002230 |
| | **COMBINED** | **2.387677** |

### City Comparison — TY2025 certified, non-homestead

| City (school district) | Combined | $300K/yr | $300K/mo |
|---|---|---|---|
| **Temple** (Temple ISD) | **2.3877%** | $7,163.03 | $596.92 |
| **Killeen** (Killeen ISD) | **2.0284%** | $6,085.29 | $507.11 |
| **Belton** (Belton ISD) | **2.0068%** | $6,020.49 | $501.71 |
| **Harker Heights** (Killeen ISD) | **1.8327%** | $5,498.19 | $458.18 |

**The stacks are NOT the same entities. Never hand-assemble a city's rate.**
Temple pays Temple College (0.2017) + Health & Bioscience (0.0139). Killeen and Harker Heights
pay Central Texas College (0.090) instead. **Belton pays no junior college district at all.**
Killeen also carries WCID #6 (0.0243). ESD #1 applies to **none** of them.

**Within-city variants (real — disclose them):**

| Variant | Rate | Incidence in parcel sampling |
|---|---|---|
| Temple + Elm Creek Watershed (+0.0228) | 2.410477 | 2 of 14 in-city Temple parcels (east Temple, 76501) |
| Temple + Belton ISD instead of Temple ISD | 2.399877 | confirmed, 8501 Iowa Ave 76502 |
| Belton + WCID #6 (+0.0243) | 2.031130 | ~32% of in-city Belton parcels |
| Killeen **without** WCID #6 (−0.0243) | 2.004130 | ~31% of in-city Killeen parcels |
| Harker Heights + WCID #6 (+0.0243) | 1.857030 | ~25–40% [VERIFY — samples disagree] |

**Safe phrasing:** Temple "about 2.39%" · Killeen "about 2.0%" · Belton "about 2.01%" ·
Harker Heights "about 1.83% to 1.86%" — always with "verify the exact address."

A **"Temple, TX" mailing address does not mean inside city limits and does not mean Temple ISD.**
Bell CAD counts 47,787 City of Temple accounts but only 32,059 Temple ISD accounts.

### Investor vs Homeowner — $300,000 home, TY2025

| City | Investor (no exemption) | Homeowner (homestead) | Homestead is worth |
|---|---|---|---|
| Temple | $7,163.03 / 2.3877% | $5,029.99 / 1.6767% | **$2,133.04/yr** |
| Killeen | $6,085.29 / 2.0284% | $4,856.37 / 1.6188% [VERIFY] | $1,228.92/yr |
| Belton | $6,020.49 / 2.0068% | $4,411.33 / 1.4704% | $1,609.16/yr |
| Harker Heights | $5,498.19 / 1.8327% | $4,269.27 / 1.4231% | $1,228.92/yr |

**WORKING NUMBERS FOR INVESTOR UNDERWRITING**
- **Temple: 2.39% of assessed value — $23.88 per $1,000 — $7,163/yr per $300K — $597/mo**
- Killeen 2.03% · Belton 2.01% · Harker Heights 1.83%

1. Out-of-state buy-and-hold investors **never** get the homestead exemption. The no-exemption
   number is the only correct one for a rental pro forma.
2. Assessed value drives the bill, not purchase price. The 10% homestead appraisal cap
   (Tax Code §23.23) is unavailable to investors and resets for a new owner-occupant.
3. **Bell CAD does NOT appraise below purchase price.** The Texas Comptroller's 2025 Ratio Study
   puts Bell CAD's median level of appraisal on single-family at **1.00** (2,046 ratios, COD 7.04).
   Underwrite at full market value. *(Retires the old "typically appraises below purchase price" line.)*

### Exemptions
- School district homestead: **$140,000** (NOT $100,000 — the old figure in this file was stale)
- Over-65 / disabled: additional $60,000 + school tax ceiling
- City of Temple and Temple College: greater of 20% or $5,000
- Bell County, Road District, Health & Bioscience, Clearwater: **no homestead exemption**

### MUD / PID — the real Temple trap is a PID, not a MUD

**No MUD taxes any property inside Temple city limits.** Zero of 14 sampled in-city parcels carried one.
All three Bell County MUDs are outside city limits and small: MUD #1 (0.783, ~534 acres near
FM 1670/Lampasas River, 1,687 accounts), MUD #2 (0.950, outside Killeen, 426 accounts),
River Farm MUD #1 (1.000, Belton 76513, 3 accounts).

**Chapter 372 Public Improvement District assessments — including North Point PID in north Temple —
are assessments collected by the city, not ad valorem taxes.** They appear nowhere on the Bell CAD
rate chart and nowhere in the 2.39%. A "2.39%" quote can understate a new-construction buyer's real
obligation by roughly **$1,000–$4,000/yr**. [VERIFY — no complete Temple PID list obtained]

### Tax calendar
| Date | Event |
|---|---|
| January 1 | Valuation date; exemption eligibility set |
| January 31 | Prior-year taxes due |
| February 1 | Delinquent — 6% penalty + 1% interest; 12% penalty July 1 |
| April 1 | Appraisal notices mailed (§25.19) |
| **May 15** | **ARB protest deadline, or 30 days after the notice is mailed, whichever is later (§41.44)** |
| July 25 | CAD certifies the appraisal roll |
| Aug–Sep 30 | Taxing units adopt rates (§26.05) |
| October | Tax statements mailed |

### TY2026 — rates HAVE moved; chart not yet published

| Entity | TY2025 | TY2026 | Status |
|---|---|---|---|
| Temple ISD | 1.137200 | **1.061900** | CONFIRMED — adopted Sept 14 2026; lowest in 15+ years |
| City of Temple | 0.699900 | **0.750000** | CONFIRMED — adopted Aug 27 2026 |
| Bell County | 0.312800 | **0.299500** | CONFIRMED — adopted Aug 24 2026, 3-1 |
| Bell County Road | 0.019900 | **0.046800** | CONFIRMED — county total 0.3463 |
| Temple College | 0.201700 | 0.249800 | [VERIFY — proposed only, no adoption record] |
| Health & Bioscience | 0.013947 | 0.013947 | [VERIFY — held flat, no 2026 rate published] |
| Clearwater UWCD | 0.002230 | 0.002216 | [VERIFY — single source] |
| **TY2026 Temple combined** | | **≈ 2.4242** | **[VERIFY — do not publish as certified]** |

**HARD BLOCK: do not publish a TY2026 combined rate until the Bell CAD 2026 chart posts
or Temple College's adopted rate is confirmed.**

### Content rules for this section
- **Never say "the FY____ rate."** Fiscal years differ by entity — the City of Temple's "FY2026"
  rate IS the 2025 tax-year rate, while Temple ISD's "2026-27" rate is tax year 2026. This is
  exactly how the old numbers rotted. Always say **"the 2025 tax-year rate."**
- Anchor to the bill, not the budget: "the rate on the bill you get this October."
- **Never mix years inside one combined rate.** A stack is all-2025 or all-2026.
- Never say **2.25%** or **2.1–2.3%** for Temple. Both are wrong.
- Never say "Killeen is the lowest of the three major cities" — **false**. Harker Heights is lowest
  overall (1.83%); Belton is lowest of Temple/Belton/Killeen (2.01%).
- Never say "a MUD could add 1% in Temple" — say **PID**.
- Evergreen phrasing (no year lock): "right around two and a half percent — about $600 a month
  per $300,000 without a homestead exemption. Your exact rate depends on the address. Look up the
  parcel at bellcad.org."

### Provenance
```
Rates:          Tax year 2025 (certified)
Verified:       2026-09-19
Primary source: https://bellcad.org/wp-content/uploads/2025/09/2025-Tax-Rate-Chart.pdf
Local copy:     data/2025-Tax-Rate-Chart.pdf
Parcel source:  https://esearchgsa.bellcad.org/Property/View/<prop_id>  (no captcha)
                https://bell.countytaxrates.com  (state TNT database)
NEXT RE-CHECK:  2026-10-05 — Bell CAD 2026 chart expected within 1-3 weeks of 2026-09-19
ANNUAL TRIGGER: September 1 (NOT October 1 — rates are adopted in AUGUST)
```

**Content audit owed:** any pro forma, DOTW cash-flow table, GMB post, blog or video that used
2.25% or 2.1–2.3% for Temple **understates taxes by ~$413/yr per $300K**. Search and correct.

---

## ASSESSED VALUES (From Bell County CAD — 106K Properties)

| City | Properties | Median Assessed | Mean Assessed |
|------|-----------|----------------|---------------|
| Temple | 26,102 | **$253,579** | $269,396 |
| Belton | 12,961 | **$296,605** | $345,974 |
| Killeen | 35,742 | **$230,750** | $248,097 |
| Harker Heights | 8,254 | **$304,590** | $311,670 |

Total Bell County residential properties in dataset: 83,059

---

## MILITARY / FORT HOOD

- BAH E-5 w/dependents: **$1,695/mo**
- BAH E-6 w/dependents: **$1,920/mo**
- BAH E-7 w/dependents: **$2,070/mo**
- BAH O-3 w/dependents: **$2,340/mo**
- BAH O-5 w/dependents: **$2,748/mo**
- Source: DoD / DTMO Official 2026 BAH Rates (MHA: TX286)
- Fort Hood total personnel: **59,695** (38,642 active-duty/reserve + 21,053 civilian — 2023 census, latest published)
- Source: Texas Comptroller, "Fort Hood Economic Impact" Report
- Gate commute: Temple (76502) to North Gate (Clear Creek): **38 min, 36.4 miles** (via I-14 W / US-190 W)

---

## BSW MEDICAL

- BSW Temple campus total employees: **8,884** (Source: Temple EDC Major Employers List)
- PGY-1 resident salary: **$70,993/yr**
- PGY-2 salary: **$73,123/yr**
- PGY-3 salary: **$75,500/yr**
- Source: BSW GME 2025-2026 Stipend and Benefits Schedule
- BSW Level 1 Trauma Center: Yes
- Trauma surgeon 15-min OR mandate: Yes
- Match Day: Third Friday of March (March 20, 2026)
- Residency start date: Late June / early July
- Physician loan partner: Extraco Bank (0% down — verify still current)

### BSW Commute Times (from BSW Temple Medical Center, 2401 S 31st St)
| Neighborhood | Miles | Drive Time |
|-------------|-------|-----------|
| Canyon Creek | 1.2 mi | **3 min** |
| Prairie Ridge | 2.8 mi | **4 min** |
| Legacy Ranch | 3.1 mi | **5 min** |
| Wyndham Hill | 3.4 mi | **6 min** |
| Lake Pointe | 7.0 mi | **14 min** |
| Bella Terra | 3.9 mi | **8 min** |
| Dawson Ranch (Belton) | 9.2 mi | **15 min** |

---

## POPULATION / GROWTH

- Temple population: **96,267** (Vintage 2024 Census estimate — latest official)
- Bell County population: **399,578** (Vintage 2024 Census estimate — latest official)
- Temple projected annual growth rate: **3.38%** (Source: World Population Review 2026)
- Bell County projected 2030 population: **427,090** (6.8% increase from 2024 — Source: Texas Demographic Center)
- DO NOT USE the 5,101-unit housing deficit stat — debunked (data scraping error)

---

## KEY EMPLOYERS

- Baylor Scott & White (8,800+)
- Fort Hood (largest active-duty armored post)
- McLane Company (HQ in Temple)
- Wilsonart International
- META data center ($800M — verify status)
- Rowan data center ($700M — verify status)
- SeAH Steel ($110M — verify status)

---

## SCHOOL DISTRICTS

| District | TEA Score | Grade | Notes |
|----------|----------|-------|-------|
| Temple ISD | 77 | **C** | |
| Belton ISD | 80 | **B** | Higher rated, drives premium pricing |
| Killeen ISD | 74 | **C** | Largest district in Bell County |
| Academy ISD | [NEEDS UPDATE] | | Small, highly rated |
| Salado ISD | [NEEDS UPDATE] | | Small, highly rated |

Source: TEA 2025 A-F Accountability Ratings (released August 2025)

---

## DISTANCES / COMMUTES

| From → To | Miles | Drive Time | Route |
|-----------|-------|-----------|-------|
| Temple → Austin | 67.8 mi | **1hr 6min** | I-35 S |
| Temple → Waco | 34.6 mi | **36 min** | I-35 N |
| Temple → Dallas | 128.6 mi | **2hr 2min** | I-35 N & I-35E N |
| Temple → Fort Worth | 119.7 mi | **1hr 53min** | I-35 N & I-35W N |
| Temple → San Antonio | ~130 mi | ~2hr | I-35 S |
| Temple → Fort Hood North Gate | 36.4 mi | **38 min** | I-14 W / US-190 W |

---

## COMPLIANCE / LEGAL DISCLOSURES

- **Texas SB 17 (Foreign Ownership):** Texas law restricts real estate ownership by entities associated with designated foreign nations (China, Iran, North Korea, Russia). All investor content should note: "All acquisitions must verify compliance with Texas SB 17 restrictions regarding foreign ownership."
- **TRAIGA (Texas Responsible AI Governance Act):** AI disclosure required when visitors interact with AI tools (applies to Temple Concierge chatbot)
- **Foundation Risk Disclosure:** Temple and Belton properties sit on expansive clay soil — foundation movement risk. Include in investor memos and relevant neighborhood content.
- **Tax Volatility Disclosure:** Bell CAD reassessments have recently outpaced state averages (commercial +9.9%, residential +3.6% in 2025). Flag for investor content.

---

## CONTENT RULES (Reminders for Claude)

- Never use "turnkey" — say "buy-and-hold investors"
- Never use "Fort Cavazos" — always "Fort Hood" (the base was renamed back in 2025)
- Never use "hidden gem," "charming community," "dream home," "white glove," "nestled"
- Never hardcode interest rates in evergreen content
- Never cite the 5,101-unit housing deficit (debunked)
- Foundation issues: only mention on pages for Western Hills, River Oaks, or the dedicated foundation page
- Tax rates: use the verified combined rates in the PROPERTY TAX section. Temple is 2.39%,
  NOT 2.25% and NOT 2.1-2.3%. Never hand-assemble a city rate from individual line items —
  the entity stacks differ by city and by address.
- Rent data: always specify ZIP and bedroom count — "Temple rents" is too vague
- All numbers should be specific — no "approximately" unless the underlying data is truly uncertain

---

## DATA SOURCES

| Data | Source | Refresh Frequency |
|------|--------|-------------------|
| Active/sold listings | MLS (CTXMLS) | Monthly |
| Rental listings | MLS (CTXMLS) | Monthly |
| Assessed values | Bell County CAD | Annually (Jan) |
| Tax rates | Bell County CAD Tax Rate Chart | Annually (Sep/Oct) |
| BAH rates | militarybenefits.info / DoD | Annually (Jan) |
| BSW salaries | AAMC / BSW posting | Annually |
| Population | US Census Bureau | Annually |
| School ratings | TEA | Annually (Aug) |
