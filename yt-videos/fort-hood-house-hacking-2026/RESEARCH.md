# Research and Evidence Lock

**Research date:** 2026-07-19  
**Geography:** Killeen, Copperas Cove, Harker Heights, Temple, and the Fort Hood corridor  
**Public standard:** every number must retain its source date and denominator

## Executive finding

The recovered ChatGPT sidebar draft had the right category but the wrong final scope. It proposed a Temple-only guide, a new-construction duplex example, and FHA/VA/conventional math. Channel, market, and competitor evidence points to a stronger concept: test four film-day-verified **property examples** through the same owner-occupancy, financing, monthly-cost, rent, property-condition, and PCS-exit screen. These examples teach four failure modes; they are not a fair city ranking.

The content gap is not “nobody has discussed house hacking.” Local creators have toured duplexes and older videos have discussed VA multifamily. The gap is a current, official-rule-checked, MLS-backed **decision test** that shows why a property that looks good online may not be owner-occupancy-ready.

## Recovered ChatGPT sidebar draft

- Sidebar title: `House Hacking Opportunity`.
- Recovered chat: https://chatgpt.com/c/6a5d341f-506c-83ea-a1e1-2a1d51b84a3e
- Original direction: a Temple-only 18–21-minute guide centered on FHA/VA/conventional financing, a new-construction duplex example, a calculator/checklist, and the title concept `Buy a Temple Duplex With 5% Down? The Honest 2026 Math`.
- What remains useful: the honest-math premise, owner-occupied financing, and an address-level deal screen.
- What changed: the final plan uses four property failure modes, reaches a real case by 0:35, avoids changing builder incentives, and does not pretend Temple alone represents the Fort Hood house-hacking opportunity.

## Existing Taylor coverage and duplicate check

- No dedicated house-hacking guide was found in the current public catalogs or Studio audit.
- Closest public overlap: `Temple TX Under $100K – Zoned 2-Family + New Slab = High ROI!` (`mNw9NMFxNV8`), a property-level investor video whose description mentions live-one/rent-one.
- A prior internal idea, “House Hacking in Killeen with a VA Loan — The Actual Math,” was never published.
- The existing Temple multifamily production bible uses house hacking only as a closing reframe.
- Duplicate risk: **low for a dedicated guide; medium if this becomes another generic four-city or new-duplex tour.**

## Competitive gap

### Current local competitor

Aundrea Dudik’s June 15, 2026 video, [Tour These BRAND NEW Construction Duplexes in Central Texas](https://youtu.be/9zSEk6Tsi6w), covers Copperas Cove and Temple new-construction duplexes. As checked July 19, it had 194 views and 9 likes. House hacking receives roughly 34 seconds and financing roughly 73 seconds. It does not apply one repeatable property/payment/risk screen across the corridor.

Her [companion article](https://www.livinginctx.com/blog/new-construction-homes-in-central-texas-under-400k-house-hacking-investment-opportunities) further occupies the “new duplexes under $400K” tour angle. Taylor should not copy that title, thumbnail, builder-logo treatment, or inventory-tour structure.

### Older local proof of interest

- [VA Loan MultiFamily House HACKS & SECRETS](https://youtu.be/J8KpQhdrQdU) — Stephen Harris, 2022; 7,137 views when checked.
- [Killeen TX is Perfect For House Hacking](https://youtu.be/pFETN93qymo) — 2023; 1,927 views when checked.
- [House Hack This Copperas Cove Duplex](https://youtu.be/VswxhggO1hI) — 2023; 493 views when checked.
- [VA Buyers Beware: Killeen 4-Plex](https://youtu.be/zJHCSEJf7MQ) — 2024; 1,363 views when checked.
- A 2026 national video, [7 Cities Where VA Loan House Hacking Actually Cash Flows in 2026](https://youtu.be/hNz0zx_oPdc), gives Killeen only a short segment rather than a local deep dive.

These are directional competitor observations, not proof that any strategy works today.

## MLS sales evidence

Primary source: `/Users/taylordasch_1/market-monitor/duplex-quadplex-bell-2026-06-29.csv`.

Method:

- Exact city match.
- `NumUnits` equal to 2, 3, or 4.
- Closed records use `ClosePrice` and span 2025-07-01 through 2026-06-25.
- Rows without `CloseDate` use `CurrentPrice`, but the file has no reliable status field; these are **not automatically active listings**.
- Price per unit is price divided by `NumUnits`.
- The verification pass found 443 qualifying sales-file rows across the analyzed filters and no exact duplicate transaction keys.
- One Killeen closed row has invalid `DOM = -9`; refresh work must exclude or explicitly document invalid DOM before recomputing DOM medians.

### Trailing-year closed 2–4-unit market

| City | Closed sales | Median close | Median close per unit | Median DOM |
|---|---:|---:|---:|---:|
| Killeen | 141 | $330,000 | $142,500 | 56 |
| Temple | 32 | $372,500 | $186,250 | 88.5 |
| Harker Heights | 27 | $341,000 | $158,500 | 106 |
| Copperas Cove | Not covered adequately by this export | — | — | — |

Public-use conclusion: in this dated Bell County export, Killeen had substantially more closed 2–4-unit transactions than Temple and Harker Heights. That supports a historical transaction-depth statement only; it does not establish current selection or make every Killeen property a better purchase.

### Records without a close date in the same snapshot

| City | Rows | Mix | Median current price | Median price per unit | Median DOM | Under $300K |
|---|---:|---|---:|---:|---:|---:|
| Killeen | 116 | 86 duplex, 2 triplex, 28 fourplex | $322,500 | $146,250 | 104.5 | 44 |
| Temple | 39 | 39 duplex | $359,000 | $179,500 | 90 | 12 |
| Harker Heights | 26 | 25 duplex, 1 fourplex | $382,000 | $191,000 | 48.5 | 3 |

**Public guardrail:** call these “records without a close date in the June 29 snapshot,” never “active inventory,” because pending/under-contract status is unavailable.

## Asking-rent evidence

Primary source: `/Users/taylordasch_1/market-monitor/july-13-rental-data.csv`.

Method:

- Exact city match.
- Blank `CloseDate`.
- Concatenated `PublicRemarks + AgentRemarks` explicitly contain duplex, triplex, fourplex, quadplex, multifamily, or multi-family language. No private remark is quoted publicly; only aggregates are used.
- Numeric current asking rent and exact bedroom count.
- These are asking rents, not executed leases, paired sales comps, or guaranteed future rent.

| City | Explicit multifamily rental rows | 2BR median ask | 3BR median ask |
|---|---:|---:|---:|
| Killeen | 47 | $900, n=15 | $1,250, n=32 |
| Temple | 20 | $1,295, n=3 | $1,400, n=13 |
| Harker Heights | 11 | $897.50, n=2 | $1,400, n=9 |
| Copperas Cove | 36 | $850, n=7 | $1,450, n=28 |

The 36 Copperas Cove rows are the strongest current reason to keep Cove in the video: the rental snapshot shows a meaningful multifamily-marketed unit pool. A dedicated Coryell County acquisition pull is still required before any sales-volume or median-purchase comparison.

Do not divide these citywide rent medians by citywide price medians on camera and call the result a return. The samples are unpaired and omit vacancy, taxes, insurance, repairs, utilities, management, financing, and concessions.

## Illustrative property candidates — not filming selections yet

Every address and lease statement below comes from a dated MLS export and must be reverified before use.

| City | Candidate | Teaching job | Required verification |
|---|---|---|---|
| Killeen | 4502 July; June 29 record at $299,999; two reported 3/2/1 units available | True duplex with an owner-unit path | Current status, vacancy, rent comps, legal units, taxes, insurance, access |
| Temple | 405 N 10th; June 29 record at $211,800; two reported 3/2 units, one vacant | Lower-price existing-duplex contrast | Current status, condition, leases, legal use, utilities, lender eligibility |
| Harker Heights | 301 Jeff Gordon; June 29 record at $315,000; remarks report both sides leased into 2027, while showing instructions refer to a vacant unit | Conflicting source fields must be resolved before any owner-occupancy verdict | Current leases, actual vacancy, possession timing, lender occupancy window, status |
| Copperas Cove | 705 & 709 Bluestem; July 19 market export at $250,000; two reported 3/2 homes, one leased | Two-home setup is not automatically a financeable duplex | Parcel(s), zoning/legal use, septic/utilities, leases, insurance, financing, status |

Backups:

- Killeen 1105 Leslie: fourplex; dated record says two occupied and two vacant.
- Temple 5222 & 5226 Davy Crockett: duplex; dated record says one side vacant.
- Harker Heights 225 Clore: dated record describes a new-construction 3/2/1 duplex on each side.
- Copperas Cove 310 W Avenue A: main house plus reported guest house; legal/financing status unknown.

## Official financing rules

### VA

The [VA purchase-loan page](https://www.va.gov/housing-assistance/home-loans/loan-types/purchase-loan/) permits eligible residential properties of up to four units when the borrower will occupy the property as a home. VA-backed loans are made by private lenders, so qualification, appraisal, entitlement, occupancy, and lender requirements still apply.

The [VA Lender’s Handbook](https://www.benefits.va.gov/WARMS/docs/admin26/m26-07/Lender_Handbook_VA_Pamphlet_Complete.pdf) supports considering prospective rent from other units under documented conditions. When projected rent is used to qualify, current guidance calls for six months of PITI reserves plus evidence of likely landlord success through prior experience or use of a property manager. A safe filmed summary is:

> Eligible VA borrowers may use a VA-backed purchase loan on a property with up to four units and live in one unit. If projected rent from other units is used to qualify, current VA guidance calls for six months of PITI reserves plus evidence of likely landlord success through prior experience or a property manager. The lender still determines the documented rent treatment, and borrower, property, appraisal, entitlement, and occupancy requirements apply.

Do not say every veteran gets a fourplex with zero down, that all proposed rent counts, or that VA universally requires exactly 12 months of occupancy.

### FHA

HUD’s [FHA 203(b) page](https://www.hud.gov/hud-partners/single-family-sfh203b) covers eligible owner-occupied one-to-four-unit properties with a minimum required investment as low as 3.5%.

The current [HUD Handbook 4000.1](https://www.hud.gov/sites/default/files/OCHCO/documents/40001-hsgh-Update-17.pdf) generally requires at least one borrower to occupy within 60 days and intend to continue occupancy for at least one year. Three- and four-unit properties must pass the self-sufficiency test, and three months of PITI reserves are required after closing. Do not apply the self-sufficiency test to duplexes.

HUD’s [Mortgagee Letter 2025-04](https://www.hud.gov/sites/default/files/OCHCO/documents/2025-04hsgml.pdf) allows existing boarder income only under limited documentation/history rules. Do not tell a first-time roommate house hacker that brand-new future roommate income automatically qualifies.

### Conventional

Fannie Mae’s [current Eligibility Matrix](https://singlefamily.fanniemae.com/media/document/pdf/eligibility-matrix-current) shows that some Desktop Underwriter-approved principal-residence 2–4-unit cases can reach 95% LTV. Manual underwriting, high-balance loans, lender overlays, and borrower/property eligibility can lower the maximum. Safe language:

> Some automated-underwriting conventional owner-occupied 2–4-unit loans may allow 5% down, but that is not universal; the lender has to approve both the borrower and the property.

### Rate benchmark

[Freddie Mac PMMS](https://www.freddiemac.com/pmms) reported a national average 30-year fixed rate of 6.55% on 2026-07-16. This is research context only—not a duplex, VA, FHA, conventional, borrower, or lender quote. The film must use a same-day address-specific scenario or clearly label an example as illustrative.

## Fort Hood and BAH context

The [official Fort Hood site](https://home.army.mil/hood/) identifies Killeen, Copperas Cove, Harker Heights, Belton, and Temple among surrounding communities. The [Army’s About page](https://home.army.mil/hood/about) says the installation is home to nearly 40,000 soldiers. Fort Hood is the current official name; the Army restored it in 2025.

The [official DoD BAH lookup](https://www.travel.dod.mil/Allowances/Basic-Allowance-for-Housing/BAH-Rate-Lookup/) returned the following for duty ZIP 76544, MHA TX286, when checked 2026-07-19:

- E-5 with dependents: $1,695 per month.
- E-5 without dependents: $1,530 per month.

BAH changes by duty-station ZIP, pay grade, and dependency status—not by which nearby city the member chooses. DoD states BAH is not designed to cover every housing expense. Never use BAH as a preapproval, payment ceiling, or cash-flow guarantee.

## Strategic conclusion

The video should be a **four-property stress test**, not a generic tutorial, city ranking, or new-construction inventory tour. Open with one verified property failure, distribute rules inside the cases, use Killeen’s historical closed count as context rather than current-inventory proof, and let each property reveal a different failure mode. The pass/fail count must emerge from refreshed evidence; it may not be selected to fit the title.

## Refresh triggers

- Re-run all MLS and rental figures if filming occurs after 2026-07-21.
- Recheck official loan sources on filming day if program guidance changes.
- Replace every candidate if its status, lease, price, or access changes.
- Use property-specific tax, insurance, utilities, and lender inputs.
- Keep the public description’s source dates even after refresh.
