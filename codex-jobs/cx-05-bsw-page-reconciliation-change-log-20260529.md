# CX-05 BSW Page Reconciliation Change Log

Completed: 2026-05-29 00:15 CDT  
Site: https://templetxhomes.net  
Mission: `/Users/taylordasch_1/claude-social-media-manager/codex-jobs/cx-05-bsw-page-reconciliation.md`

## Rollback

- Pre-change backup: `/Users/taylordasch_1/claude-social-media-manager/codex-jobs/agentfire-backups/cx-05-20260528-223946/prechange-backup.json`
- Backup includes REST edit data and AgentFire `afe_values` for post/page IDs `2271`, `2223`, `3131`, `2230`, `2817`, and `3200`.
- AgentFire revisions remain available in WordPress/AgentFire for page-level rollback.
- Redirect Manager rollback rows:
  - ID `88`: `/best-neighborhoods-baylor-scott-white-temple-tx/`
  - ID `89`: `/best-neighborhoods-baylor-scott-white/`
  - New row added for `/best-neighborhoods-bsw/`

## Publish Status

- Group A was saved/published live after the bounded edit pass.
- Group B physician mortgage page was also saved/published live after Taylor's explicit follow-up approval: "go ahead and publish the physician loan page i looked at it".

## A1 - Match Day Page

Page: `/match-day-2026-bsw-housing-timeline/`  
Post ID: `2271`  
Status: published live

| Field | Before | After |
| --- | --- | --- |
| Canonical | Checked for split canonical | Canonical verified to self: `/match-day-2026-bsw-housing-timeline/` |
| Body median stat | `$255K` | `~$274K` |
| Body median comparison | `Temple median home: $255K vs Austin $525K+` | `Temple median home: ~$274K (median, MLS May 2026) vs Austin $525K+` |
| Body buy label | `Buy ($255K, 0% Down)` | `Buy (~$274K, 0% Down)` |
| Body training-length language | `3+ year categorical residency` | `4-7 year residency or fellowship-to-attending path` |
| Body rent-vs-buy rule | `Buying makes more sense for a 3+ year program or a household likely to stay in Central Texas.` | `Buying usually makes more sense for a 4-7 year program or a household likely to stay in Central Texas. A 3-year program is a genuine toss-up; run the numbers against your cash reserve and exit plan.` |
| Body rule-of-thumb | `if your program is 3+ years, buy. If it's a preliminary year, rent the cheapest apartment you can tolerate and save your cash.` | `if your program is 1-2 years, rent. If it is 3 years, run the numbers carefully. If it is 4-7 years or a fellowship-to-attending path, buying usually wins.` |
| FAQ buy answer | `Yes, if your training program is 3+ years. Temple's median home price is $255K.` | `Often, if your training program is 4-7 years. A 3-year program is a toss-up, and a 1-2 year prelim usually points to renting. Temple's median home price is ~$274K (median, MLS May 2026).` |
| Exit-cost line | `$15,000-$23,000 in exit costs on a $255K home` | `$15,000-$23,000+ in exit costs on a ~$274K home` |
| Hold-period line | `Only profitable if you've owned 3+ years.` | `Usually strongest if you have owned 4+ years; a 3-year hold is a toss-up.` |
| Prelim line | `Rent if your training program is under 3 years. Period.` | `Rent for 1-2 year prelims; treat 3-year programs as a toss-up.` |
| Physician loan sentence | `Physician loans let you close with 0% down using only your signed BSW contract.` | Linked `Physician mortgage loans` anchor to `/physician-mortgage-loans-central-texas/` and softened eligibility to lender terms. |
| Monthly payment sentence | `A physician loan at 0% down, 6.5% rate on a $255K home runs approximately $2,100/month` | `A physician loan at 0% down, using a May 2026 rate estimate on a ~$274K home, runs approximately $2,100+/month` |
| Property-tax FAQ | `Bell County's effective rate is 2.18%. On a $300K home, that's $6,540/year ($545/month) in your escrow payment.` | `A rough planning number is about 2% of value, but the actual bill varies by parcel, district, exemptions, and appraisal. Verify the address at Bell CAD before you trust a calculator.` |
| Property-tax detail | `Bell County's effective property tax rate averages 2.18%... On a $255K home, expect $5,559/year...` | `Use roughly 2% of assessed value as a planning number, then verify the parcel at Bell CAD because city, ISD, county, college district, exemptions, and appraisal all change the bill.` |
| GME count | `31 GME programs` | `30+ accredited programs` |
| Internal link | `https://templetxhomes.net/best-neighborhoods-bsw/` | `https://templetxhomes.net/neighborhoods-near-bsw-by-commute/` |

Skipped exact target:

- `Match Day is March 17, 2026.` was not found on this page. Final verification found no `March 17` instance on the live page.

## A2 - Redirect Consolidation

Status: published live

| Redirect Manager Row | Before | After |
| --- | --- | --- |
| ID `88` | `/best-neighborhoods-baylor-scott-white-temple-tx/` -> `/best-neighborhoods-bsw/` | `/best-neighborhoods-baylor-scott-white-temple-tx/` -> `/neighborhoods-near-bsw-by-commute/` |
| ID `89` | `/best-neighborhoods-baylor-scott-white/` -> `/best-neighborhoods-bsw/` | `/best-neighborhoods-baylor-scott-white/` -> `/neighborhoods-near-bsw-by-commute/` |
| New row | No direct redirect for `/best-neighborhoods-bsw/` found | `/best-neighborhoods-bsw/` -> `/neighborhoods-near-bsw-by-commute/` |

## A3 - BSW Relocation Hub

Page: `/baylor-scott-white-relocation/`  
Post ID: `2223`  
Status: published live

| Field | Before | After |
| --- | --- | --- |
| Meta title | Empty Yoast title field | `Baylor Scott & White Temple Relocation Guide (2026)` |
| Meta description | `BSW Temple housing guide: best neighborhoods by commute, physician loans (0% down), schools, costs. From a $30M+ agent who's housed dozens of BSW staff.` | `Relocating to Temple, TX for Baylor Scott & White? Neighborhoods by commute, the buying timeline, and honest tradeoffs from agent Taylor Dasch, EG Realty.` |
| Body physician link | `how physician loans work` | Linked `physician mortgage loans` anchor to `/physician-mortgage-loans-central-texas/` |
| Glance median | `~$250K` | `~$274K` |
| Body median | `Median home prices sit around $250,000` | `Median home prices sit around ~$274,000 (MLS May 2026)` |
| Body median | `Median home price: ~$250,000 (Q1 2026)` | `Median home price: ~$274,000 (MLS May 2026)` |
| Body median | `median home price around $250,000` | `median home price around ~$274,000 (MLS May 2026)` |
| Body median comparison | `Temple's median home price is $250,000-$300,000...` | `Temple's median home price is about ~$274,000 (MLS May 2026)...` |
| Property tax | `property taxes run 2.2% to 2.5% in Bell County` | `use roughly 2% of value as a planning number in Bell County` |
| Property-tax bullet | `Property tax rate: 2.2-2.5% (Bell County)` | `Property tax: roughly 2% of value (verify your parcel at Bell CAD)` |
| Banned wording | `turn-key` | `move-in ready` |
| Loan copy | `Physician mortgage loans are available locally with 0% down and no PMI` | `Some physician mortgage lenders offer 0% down and no PMI options` |
| Loan copy | `Physician loans: 0% down, no PMI (Extraco, Regions)` | `Physician loan options: some lenders offer 0% down/no PMI (verify terms)` |
| Loan copy | `Physician mortgage loans exclude student debt from DTI calculations and offer 0% down with no PMI.` | `Some physician mortgage programs may exclude student debt from DTI calculations and offer 0% down/no PMI options.` |
| Loan copy | `Physician mortgage loans offer 0-5% down payment with no PMI, and exclude student loans from debt-to-income calculations.` | `Some physician mortgage loans offer 0-5% down payment with no PMI and may treat student loans differently in debt-to-income calculations.` |
| Internal links | `https://templetxhomes.net/best-neighborhoods-bsw/` | `https://templetxhomes.net/neighborhoods-near-bsw-by-commute/` |

## A4 - Childcare Page

Page: `/bsw-temple-childcare-daycare-guide/`  
Post ID: `3131`  
Status: published live

| Field | Before | After |
| --- | --- | --- |
| Meta title | Empty Yoast title field | `BSW Temple Childcare: Shift Hours, Waitlists & Cost (2026)` |
| Meta description | `Daycare in Temple TX for BSW families -- center costs, nanny rates, FSA savings, and what to lock down 12 months before your start date.` | `Why medical families should start the Temple childcare search before housing: 6-6 daycare hours, waitlists, and shift-friendly options near BSW.` |
| On-site daycare claim | `BSW does not operate an on-site daycare. However, BSW provides a Dependent Care FSA through Optum Bank...` | `At the Temple campus, BSW does not run a dedicated on-site employee daycare (its on-site/Bright Horizons childcare is at the Fort Worth campus); BSW does offer childcare benefits system-wide -- confirm Temple specifics with HR.` |
| On-site daycare claim | `BSW does not operate an on-site daycare facility at the Temple campus...` | Same scoped Temple-campus/Bright Horizons/Fort Worth/HR confirmation language. |
| Waitlist copy | `Standard infant waitlists in Temple range from 3 to 15 months.` | `Estimated standard infant waitlists in Temple range from 3 to 15 months.` |
| Waitlist copy | `The infant care waitlist in Temple is 3-15 months at most centers` | `The estimated infant care waitlist in Temple is 3-15 months at most centers` |
| Internal links | `/best-neighborhoods-baylor-scott-white-temple-tx/` | `/neighborhoods-near-bsw-by-commute/` |

## B1 - Physician Mortgage Page

Page: `/physician-mortgage-loans-central-texas/`  
Post ID: `2230`  
Status: published live after Taylor approval

| Field | Before | After |
| --- | --- | --- |
| Meta title | Empty Yoast title field | `Physician Mortgage Loans in Central Texas \| Temple TX` |
| Meta description | `Physician mortgage loans in Central TX. Compare lenders, see real scenarios matching BSW salaries to Temple & Belton neighborhoods.` | `How physician mortgage loans work in Central Texas -- the 0%-down, no-PMI options some lenders offer doctors and residents. By Temple agent Taylor Dasch.` |
| Hero median | `$260K` | `~$274K` |
| Median comparison | `Temple median $255K vs Austin $525K+` | `Temple median ~$274K (MLS May 2026) vs Austin $525K+` |
| Savings median | `$255K` | `~$274K` |
| Median sentence | `where median home prices are $255K` | `where median home prices are around ~$274K (MLS May 2026)` |
| Median sentence | `With Temple's median home price at $255-$260K` | `With Temple's median home price at ~$274K (MLS May 2026)` |
| Median sentence | `At Temple's $255K median` | `At Temple's ~$274K (MLS May 2026) median` |
| Rate/payment sentence | `A $255K home with 0% down at 6.75%` | `A ~$274K home with 0% down using a May 2026 rate estimate` |
| Match Day date | `Match Day is March 17, 2026.` | `Match Day is March 20, 2026.` |
| Days-to-July line | `You have 106 days until July 1.` | `You have 103 days until July 1.` |
| Financing countdown | `That's 106 days to secure financing` | `That's 103 days to secure financing` |
| Timeline | `March 17 -- Day 0` | `March 20 -- Day 0` |
| Timeline | `March 20-25 -- Days 3-8` | `March 20-25 -- Days 0-5` |
| Timeline | `March 25 - April 5 -- Days 8-19` | `March 25 - April 5 -- Days 5-16` |
| Timeline | `April 5-May 10 -- Days 19-54` | `April 5-May 10 -- Days 16-51` |
| Timeline | `May 10-June 20 -- Days 54-95` | `May 10-June 20 -- Days 51-92` |
| Timeline | `June 25-30 -- Days 100-106` | `June 25-30 -- Days 97-102` |
| Rent-vs-buy | `The math favors buying in Temple for residencies of 3+ years.` | `The math usually favors buying in Temple for 4-7 year residencies or fellowship-to-attending paths. A 3-year program is a genuine toss-up; 1-2 year prelim paths usually point to renting.` |
| Eligibility copy | `Residents and fellows qualify using their signed employment contract, even before their start date.` | `Some residents and fellows may qualify using their signed employment contract before their start date.` |
| Eligibility copy | `can qualify for 0% down homeownership on a single resident stipend` | `may be able to qualify for 0% down homeownership on a single resident stipend, depending on lender terms` |
| Loan promise copy | `Physician mortgage loans are specialized products that let medical professionals buy homes with 0% down and no private mortgage insurance (PMI), saving $200-$350/month compared to conventional loans.` | `Physician mortgage loans are specialized products some lenders offer to qualifying medical professionals, sometimes with 0% down and no private mortgage insurance (PMI); terms, savings, and eligibility vary by lender and borrower profile.` |
| Loan promise copy | `BSW PGY-1 stipend ($70,993) qualifies for $250K-$300K at 0% down in Temple` | `A BSW PGY-1 stipend ($70,993) may qualify for $250K-$300K at 0% down in Temple, depending on lender terms` |
| Loan promise copy | `0% down, no PMI on purchases up to $1M at most lenders; up to $1.5M at 5% down` | `Some lenders offer 0% down/no PMI options on purchases up to program caps; verify max loan amounts directly` |
| Loan promise copy | `Residents qualify with signed contract 90 days before start date--no W-2 history required` | `Some residents may qualify with a signed contract before start date--verify documentation requirements with the lender` |
| PMI copy | `Physician loans eliminate this entirely.` | `Some physician loan products can eliminate this.` |
| Property tax | `Effective rate: ~2.18%. On a $300K home, that's $6,540/year ($545/month).` | `Use roughly 2% of assessed value as a planning number, then verify the parcel at Bell CAD because city, ISD, county, college district, exemptions, and appraisal all change the bill.` |
| Fair housing disclosure | Not present near the loan explainer | `Program terms, eligibility, loan availability, and savings vary by lender and borrower profile. Equal Housing Opportunity.` |

## Skipped/Adjusted Exact Targets

- Some exact strings in the mission were not found because the live AgentFire copy used close variants (`$250K`, `$255K`, `$260K`, or formatted timeline ranges). Equivalent live variants were updated where present and then rechecked.
- The Match Day page did not contain the exact `Match Day is March 17, 2026.` target; final live verification confirmed the bad date is absent there.
- Several retired-link exact variants were absent on specific pages. Final verification confirmed the relevant live pages point to the commute page where checked, and all three retired slugs now 301 to `/neighborhoods-near-bsw-by-commute/`.
- Encoding cleanup targets that were absent after the cleanup pass were skipped by design; final verification found no `mojibake` markers on the checked live pages.

## Verification

Live verification result: PASS

Checked pages:

- `/match-day-2026-bsw-housing-timeline/`
- `/baylor-scott-white-relocation/`
- `/bsw-temple-childcare-daycare-guide/`
- `/physician-mortgage-loans-central-texas/`

Checked redirects:

- `/best-neighborhoods-bsw/` -> 301 -> `/neighborhoods-near-bsw-by-commute/`
- `/best-neighborhoods-baylor-scott-white-temple-tx/` -> 301 -> `/neighborhoods-near-bsw-by-commute/`
- `/best-neighborhoods-baylor-scott-white/` -> 301 -> `/neighborhoods-near-bsw-by-commute/`

Final check passed for:

- Correct Match Day date on physician page.
- `$274K` median updates on all target pages.
- Hub and childcare Yoast title/meta updates.
- Physician page Yoast title/meta updates.
- Hub and Match Day links into the physician page.
- Retired BSW neighborhood slugs redirected to the commute page.
- Property-tax language reframed to roughly 2% and Bell CAD verification.
- Loan language softened to category-level terms with Equal Housing Opportunity near physician loan content.
