# TEMPLE TX DATA VAULT — Single Source of Truth
## Every content skill pulls from this file. Prevents number drift across videos, pages, and social.
## Last verified: 2026-03-21
## Next review due: 2026-05-01
## UPDATE PROTOCOL: Review monthly on the 1st. Flag any data point older than 90 days.
## SECTION FRESHNESS:
##   Market Data (MLS): 2026-03-17 — next refresh due 2026-04-17
##   Property Tax (CAD): 2025 rates — next refresh due 2026-10-01
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

## PROPERTY TAX (From Bell County CAD — 2025 Tax Rates, per $100 Valuation)

### Tax Rates by Jurisdiction
| Entity | Code | Rate per $100 |
|--------|------|--------------|
| Bell County | CB | 0.3128 |
| Temple City | TTE | 0.6999 |
| Belton City | TBE | 0.5225 |
| Killeen City | TKI | 0.7014 |
| Harker Heights City | THH | 0.5300 |
| Temple ISD | STEM | 1.1372 |
| Belton ISD | SBEL | 1.1494 |
| Killeen ISD | SKIL | 0.8778 |
| Academy ISD | SACA | 1.1489 |
| Salado ISD | SSAL | 1.1669 |
| ESD1 | ESD1 | 0.1000 |

### Combined Effective Tax Rates (County + City + ISD + ESD1)
| Location | Total Rate | Effective % | Annual Tax on $280K | Monthly |
|----------|-----------|-------------|--------------------:|--------:|
| **Temple (Temple ISD)** | 2.2499 | **2.25%** | $6,300 | $525 |
| **Belton (Belton ISD)** | 2.0847 | **2.08%** | $5,837 | $487 |
| **Killeen (Killeen ISD)** | 1.9920 | **1.99%** | $5,578 | $465 |
| **Harker Heights (Killeen ISD)** | 1.8206 | **1.82%** | $5,098 | $425 |

### Tax Rules for Content
- Homestead exemption: $100K off school taxes (state) + local exemptions vary
- Protest deadline: May 15 or 30 days after notice (whichever is later)
- Bell County CAD typically appraises below purchase price
- **DO NOT hardcode specific tax rates in evergreen content** — reference "approximately 2.1–2.3%" for Temple
- For investor pro formas, use 2.25% for Temple (Temple ISD) as working number
- Belton is slightly lower (2.08%) — worth noting in comparison content
- Killeen is lowest of the three major cities (1.99%)

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
- Never use "Fort Hood" — always "Fort Hood"
- Never use "hidden gem," "charming community," "dream home," "white glove," "nestled"
- Never hardcode interest rates in evergreen content
- Never cite the 5,101-unit housing deficit (debunked)
- Foundation issues: only mention on pages for Western Hills, River Oaks, or the dedicated foundation page
- Tax rates: reference the combined effective rates in this file, not individual line items
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
