# Buyer Value: A Resource and Service People Would Save
## The Year-Two Test for Temple and Belton buyers, with a bounded decision-note consultation

**For:** Taylor Dasch, EG Realty · **Prepared:** October 1, 2026 · **Status:** drafts and analysis only. Nothing published, sent, enrolled, changed in the CRM or spent. · **Pilot start requested:** Monday, October 5, 2026, inside the 90-day buyer program.

---

## 0. What was inspected, and what was not

**Private input:** the assignment, the October 1 owner direction (TD-IMPLEMENT-20261001-v1), and Business Evidence v3 with all 29 closing rows and 22 appointment rows. No CRM, analytics, computer, email, calendar, Lofty, Lanes or ledger file was read. No connector was used.

**Public inspection of templetxhomes.net, October 1, 2026 (curl, sitemap and page text):**

| What | Finding | Why it matters here |
|---|---|---|
| Platform | WordPress 7.1.2 with All in One SEO 5.0.1.1; 215 URLs in the page sitemap; sitemap regenerated October 1, 2026 | The site is WordPress, not AgentFire. Taylor's stored preferences still say AgentFire. Treat the CMS as WordPress until Taylor confirms. |
| `/first-time-home-buyers/` | Reviewed September 30, 2026. Eleven sections including an **ungated two-scenario monthly cost worksheet** (current rental vs. proposed purchase), a cash-to-close table, assistance program table (TSAHC, TDHCA, SETH), loan comparison, new-build vs. resale questions, and its own inquiry form with a "comfortable monthly payment" band | Already strong. Do not rebuild. The Year-Two Test below extends it (two purchases, year one vs. year two) and links back to it for rent-vs-buy and cash-to-close. |
| `/how-much-house-can-you-afford-temple-tx/` | Updated May 29, 2026. 28/36 calculator using a 2.25% tax rate and a 6.5% example rate | Budget-ceiling step. The example rate is stale against the October 1 Freddie Mac average (7.28%). Flag, not rebuild. |
| `/temple-tx-property-taxes/` | Reviewed September 23, 2026. Per-entity parcel worksheet with eight named 2025 parcel examples; already uses the $140,000 school exemption and Temple's 20% local option | This is the tax engine. The Year-Two Test tells the reader to fill its tax lines from this page. |
| `/mud-vs-pid-taxes-temple-belton-tx/` | Data verified March 2026. Three Bell County MUDs (0.783% to 1.0%), PID vs. MUD mechanics, neighborhood lookup | Reused as the district check. |
| `/bell-county-builder-incentives/` | Source observed September 30, 2026. 58 incentive packages in the MLS export, 69% tied to a preferred lender, 45% with a stated price cut, and **no builder-verified current offer** published | Reused for the incentive step and the "verify in writing" rule. |
| `/new-construction-vs-resale-temple-tx/` | June 18, 2026 closed-sale pull: new $290,950 median vs. resale $265,000; new-build days on market 133 vs. 56 | Topic page. Links to the Year-Two Test as the decision tool. |
| `/temple-vs-belton/` | Sources observed September 2 to 25, 2026. Twelve-month medians $269,700 Temple vs. $320,848 Belton; 2025 tax on a $300,000 homestead about $5,030 (Temple) vs. about $4,411 (Belton) | Relocation comparison already exists. Reused. |
| `/temple-tx-market-update/2026-08/` | CTXMLS export August 19, 2026: Temple median sold $261,545; 633 actives; 4.6 months of supply; median closed days on market 53; close-to-original-list 96.4%; 56% of actives had a price cut | Current local context for the resource. |
| `/rent-vs-buy-bsw-resident-temple-tx/` | Reviewed September 23, 2026. Monthly cash-flow and exit-cost framing for a three-year stay | The "stay-length" logic already exists for one audience. The Year-Two Test generalizes it. |
| `/buyers/` | Updated July 2026. States a "$100K homestead exemption" | **Stale**: the school exemption is $140,000 (Tax Code 11.13(b); Proposition 13, November 4, 2025). One-line fix. |
| `/contact/` | Form posts to `https://ai-real-estate-toolkit-production.up.railway.app/fub-lead`; hidden fields `source=contact`, `campaign=contact-form`, `lane=general`, `lead_tags=Contact`, `tags=General,Contact`; a request-type select (`asset_name`), builder-visit fields, a **current agent relationship** select, a TCPA consent checkbox, redirect to `/thank-you/` | The intake route and attribution hooks already exist. The endpoint name says "fub-lead" while the evidence says Lofty is the CRM and FUB-era integrations were dropped. Where submissions actually land is unverified. |
| `/thank-you/` | States it "does not verify that a request was saved"; links neighborhoods, moving guide, investor hub, two PDFs | Receipt page exists; needs one added link. |
| Footer | IABS link, TREC license 0775435, "EG Realty" rendered at the required size | Brokerage identification present. The IABS form itself should be the January 2026 version. Verify. |

**Public primary sources retrieved October 1, 2026:** Bell CAD 2025 Tax Rate Table (PDF); Texas Comptroller exemptions and protests pages; TREC article on 2026 buyer-representation changes (Occupations Code 1101.562 and 1101.563); Freddie Mac PMMS (October 1, 2026 release); Realtor.com Killeen-Temple series via FRED (August 2026); TDI homeowners market overview; KDH News and KWTX reports on TEA's August 14, 2026 ratings; Fannie Mae, HUD and VA concession rules as summarized by lender sources. Full list in section 13.

**Not inspectable, and therefore conditional:** where the contact form actually writes (Lofty, the appointment ledger, email only); the current IABS version on the site; Bell County's 2026 adopted tax rates (not yet posted on Bell CAD's rate page on October 1); any builder's current written incentive; Bell County's average homeowners premium (TDI's county map requires interaction); whether the site's two PDFs on the thank-you page are current.

---

## 1. The one decision this offer resolves

**Decision:** *"Of the two homes I am actually considering, which one can my household still carry in year two and year three, and should I buy either one now rather than rent or wait?"*

**Why this decision and not a relocation guide.** A relocation guide answers "what is Temple like." The site already has 40-plus neighborhood and comparison pages that do that well. The question that costs people money is narrower and comes later: the moment they are choosing between two specific addresses, often a new build with an incentive and a resale without one, or a Temple address and a Belton address, or a purchase and one more lease. Four Bell County mechanics make the year-one payment a poor guide to the real payment:

1. **The land-only tax year on new construction.** Bell CAD values property as of January 1. A home that was a slab or a lot on January 1 is taxed that year on the land or partial improvement. The following January it is valued as a finished home, the escrow analysis catches up, and the payment steps up (TSAHC consumer guidance; Texas Comptroller appraisal rules).
2. **Homestead timing.** The $140,000 school exemption and Temple's 20% local option are large, but they apply to the buyer's taxable value only once the buyer qualifies and files (Form 50-114). A seller's prior exemption or a new build's lot bill tells the buyer nothing about their own bill.
3. **Temporary buydowns.** In the September 30 MLS snapshot, 69% of active Bell County incentive packages were tied to a preferred lender, and 2-1 and 3-2-1 buydowns are routine on standing inventory. A 2-1 buydown raises principal and interest in month 13 and again in month 25.
4. **District charges.** Bell County MUD rates ran 0.783% to 1.0% in 2025; a PID is a fixed assessment. Neither shows in the list price.

A buyer who adds those four rows for two addresses, side by side, has made the consequential decision with their own eyes. That is worth saving and sharing. It is useful to people who never call Taylor, and it is exactly the preparation that makes a 30-minute consultation productive.

**Honest comparison with how people already get this done.** None of this disparages anyone; it describes what each source is built to do.

| Source | What it does well | What it does not do |
|---|---|---|
| Portals (Zillow, Realtor.com, Redfin) | Inventory, photos, list price, a generic payment estimate | Payment estimates use a flat tax percentage, no homestead, no land-only year, no district assessment, no buydown schedule. One address at a time. |
| Builders and their preferred lenders | Accurate on their own home: price, included features, incentive, year-one payment | The sheet is for year one, for their home, with their lender. It will not show the resale across town or year three. Incentive conditions change monthly; the September 30 board shows no builder-verified current offer. |
| Lenders (Loan Estimate) | Legally standardized cost disclosure for one property and one loan | A Loan Estimate is for one address. Its tax line is an estimate the lender was given; on new construction it is often the lot bill. It does not compare two homes or test renting. |
| Agents generally | Showings, negotiation, contract, local judgment | Many do not quantify year two. Agents may also not show homes under Texas law without a written agreement (Occupations Code 1101.563, effective January 1, 2026), so a resource that works *before* that agreement has real value to the consumer. |
| This resource | Two addresses, three years, every Bell County line, plus a renting row and a stay-length test; works with no form | It does not replace the Loan Estimate, the parcel record, an insurance quote or an inspection. It tells the reader exactly which document to get for each line. |

**No exclusive expertise is claimed.** The rates come from Bell CAD. The homestead rule comes from the Comptroller. The agreement rule comes from TREC. The resource's value is the assembly, the local examples, and the honesty about what is unknown.

---

## 2. What to leave unchanged, and the three stale lines to fix

**Leave unchanged:** the first-time-buyer page and its worksheet; the property-tax parcel worksheet; the MUD/PID page; the builder incentive board; the Temple-vs-Belton comparison; the neighborhood comparison; the market update; the rent-vs-buy page for BSW residents; the contact form's structure, consent language and agent-relationship question; the thank-you page's "does not verify a save" honesty. These are already better than most brokerage sites and they are dated and sourced.

**Fix with one line each, at the next scheduled edit (not a new project):**

- `/buyers/` "with a $100K homestead exemption" → "$140,000 school homestead exemption (2025 tax year onward)".
- `/how-much-house-can-you-afford-temple-tx/` example rate "~6.5%" → point the reader to the current weekly Freddie Mac average and date it; do not hardcode. The 7.28% figure below is dated October 1, 2026 and will be wrong within a week.
- `/buyers/` "Seller concession frequency exceeds 90%" → add the source and date or remove; the August market update's measurable figure is "56% of active listings had taken at least one price cut," which is a different statistic.

---

## 3. The public resource (ready-to-review page text)

> **Page working title:** The Year-Two Test: Compare Two Temple or Belton Homes on What You Will Actually Pay
> **Proposed URL:** `/year-two-test/` (one page, not a landing page; or, as a zero-new-page fallback, section VIII-B of `/first-time-home-buyers/`)
> **Meta title (under 60):** Year-Two Test: Real Payment for Temple & Belton Homes
> **Meta description (under 155):** Compare two Temple or Belton homes on year-one, year-two and year-three cost, with Bell County taxes, homestead timing, buydowns and district charges. No form needed.

---

### The Year-Two Test: Compare Two Temple or Belton Homes on What You Will Actually Pay

*Taylor Dasch with EG Realty · Temple, TX · Prepared October 1, 2026 · Rates and figures carry their own dates below. Nothing on this page is a loan offer, a tax bill or an appraisal.*

**Should you compare homes on the year-one payment?** No. In Bell County the year-one payment is often the lowest payment you will ever make on a home, and the year-three payment is the one you live with. This page gives you a six-line test to run on any two homes you are weighing, including a new build against a resale, a Temple address against a Belton address, or a purchase against one more year of renting. You can finish it with documents you can get for free. You do not need to send me anything to use it.

**What you need before you start (about an hour of collecting):**

- For each home: the listing sheet, the Bell CAD parcel record (search by address at bellcad.org), and, for a new build, the builder's written incentive sheet with its expiration date and lender condition.
- A written lender scenario for each home, same loan type and same lock assumption, showing principal and interest at the note rate and at each buydown step if there is one. Ask for the payment *after* the buydown ends.
- One address-specific homeowners insurance quote per home. For anything near a creek or lake, ask whether flood coverage is required.
- Your own number: the monthly housing amount you can carry comfortably after your other obligations. Write it down before you look at the homes. A lender's approval is a ceiling, not a target.

#### Step 1. Write your comfortable monthly number at the top

Not the maximum you qualify for. The amount that still leaves room for savings, a car repair and a deductible. If you need help finding it, the 28/36 calculator on this site walks through it. Everything below is compared to this one number.

#### Step 2. Principal and interest, three years out

Ask each lender for principal and interest at the full note rate, then at each year's buydown rate if the builder or seller is funding one. A 2-1 buydown means year one is two points below the note rate, year two is one point below, year three is the note rate. Write all three years.

*Reference point, dated:* Freddie Mac's national average 30-year fixed rate was 7.28% for the week released October 1, 2026 (15-year: 6.60%). Your quote will differ. Use your quote.

#### Step 3. Property tax, the way Bell County actually bills it

This is the line most estimates get wrong. Do it per taxing entity, not with one percentage.

1. Find the parcel's taxing entities on the Bell CAD record. A Temple mailing address can sit in Belton ISD or Academy ISD; a Belton address can be outside the city. The entities decide the bill, not the city name.
2. Use the 2025 adopted rates below (Bell CAD 2025 Tax Rate Table). Bell County's 2026 rates are adopted each fall; check the Bell CAD rate chart for the newer table before relying on these.
3. Apply the exemptions you will actually hold. The school district must exempt $140,000 of a residence homestead's value (Texas Tax Code 11.13(b), approved by voters November 4, 2025). Temple City and Temple College each also exempt 20% of value for a homestead (minimum $5,000). Belton City and Bell County list no general homestead percentage in the 2025 table. Over-65 and disabled owners have additional amounts.
4. For a **new build**, write two tax lines: year one on the value as of the January 1 before you close (often land or partial construction; ask the builder what the lot was assessed at), and year two on the finished home with your homestead applied. Your escrow will reset to the second number.
5. For a **resale**, write the finished-home value with your homestead applied for both years. The seller's old bill is not your bill: their exemptions and their appraisal cap do not transfer to you. After your first full year with a homestead, your appraised value increase is capped at 10% per year.
6. Add any **MUD or PID** line separately. In 2025, Bell County MUD No. 1 was 0.783% and MUD No. 2 was 0.950%. A PID is a fixed annual assessment; ask the title company for the payoff. If the parcel is in either, Texas law requires a separate notice before you sign.

**2025 adopted tax rates, per $100 of taxable value (Bell CAD 2025 Tax Rate Table):**

| Entity | Rate | Homestead note in the 2025 table |
|---|---|---|
| Bell County | 0.3128 | No general homestead %; over-65 and disabled amounts |
| City of Temple | 0.6999 | 20% local option, $5,000 minimum |
| City of Belton | 0.5225 | No general homestead %; over-65/disabled $10,000 |
| Temple ISD | 1.1372 | $140,000 school exemption; over-65/disabled $60,000 |
| Belton ISD | 1.1494 | $140,000 school exemption; over-65/disabled $60,000 |
| Salado ISD | 1.1669 | $140,000; over-65/disabled $60,000 |
| Temple College | 0.2017 | 20% local option, $5,000 minimum |
| Temple Health & Bioscience District | 0.013947 | Applies to some Temple parcels |
| Bell County ESD No. 1 | 0.1000 | Unincorporated areas; check the parcel |
| Bell County MUD No. 1 | 0.7830 | Parcel-specific |
| Bell County MUD No. 2 | 0.9500 | Parcel-specific |

Academy ISD's 2025 rate did not print on the retrieved table; use the Bell CAD parcel estimate for Academy ISD addresses.

*Worked line, hypothetical:* a finished Temple home appraised at $310,000 inside the city, in Temple ISD, Temple College and the Bioscience District, with a general homestead, pays about **$5,182 a year, or $432 a month**: school $1,933 on $170,000 taxable; city $1,736 on $248,000; college $500 on $248,000; county $970 and bioscience $43 on the full $310,000. Without the homestead the same parcel would owe about $7,333 ($611 a month). Those are the two numbers a new-build buyer must not confuse with the year-one lot bill.

#### Step 4. Insurance, mortgage insurance, HOA and upkeep

- **Homeowners insurance:** use the written quote. For scale only, the Texas Department of Insurance reports a preliminary 2025 statewide average premium of $3,489 for homeowners policies; Bell County's own average is on TDI's county map. Your quote depends on the roof, construction year and deductible. A 2% wind/hail deductible on $300,000 of dwelling coverage is $6,000 out of pocket per claim.
- **Mortgage insurance:** required on most loans under 20% down; ask the lender for the monthly amount and when it can be removed. VA loans do not carry it.
- **HOA:** dues and any special assessment, from the resale certificate or the builder's HOA disclosure.
- **Upkeep reserve:** write something honest. A new build with a warranty is not zero. An older roof, HVAC and water heater are predictable costs with dates.

#### Step 5. The renting row

Put your current or likely rent, renters insurance and any utilities you would not pay as an owner in a third column. In August 2026, Temple's median sale price was $260,000 across 100 observed MLS closings and Belton's was $313,000 across 56 (CTXMLS exports, September 29 and 30, 2026). Renting a year is a legitimate answer when the purchase columns clear your number only in year one.

#### Step 6. The stay-length test

Ask one question of each purchase column: *if I had to sell at 36 months, what price would cover my payoff and selling costs?* Your lender can give the loan balance at month 36; selling costs vary and are negotiable, so test a range rather than a single percentage. If the answer is "I need the home to be worth more than I paid," and your job or orders could move you inside three years, that is a reason to prefer the renting row or the home that costs less to leave. Temple's 56% price-cut share and 53-day median time to sell in the August 2026 update are a reminder that sellers do not always control their timing.

#### The test, as a table you can copy

| Line | Home A | Home B | Renting |
|---|---|---|---|
| Address, listing date, lender, quote date | | | Lease terms, renewal date |
| Price / loan amount / down payment | | | |
| Principal & interest, year 1 | | | Rent, year 1 |
| Principal & interest, year 2 | | | Likely rent, year 2 |
| Principal & interest, year 3 (note rate) | | | |
| Property tax, year 1 (per entity, your exemptions) | | | Included |
| Property tax, year 2 (finished value, homestead) | | | |
| MUD / PID | | | |
| Homeowners (or renters) insurance ÷ 12 | | | |
| Mortgage insurance | | | |
| HOA | | | |
| Upkeep reserve | | | |
| **Total, year 1** | | | |
| **Total, year 2** | | | |
| **Total, year 3** | | | |
| Cash needed at closing (after confirmed credits) | | | Deposit |
| Price needed to exit at 36 months | | | Lease-break cost |
| Clears my comfortable number in year 3? | yes / no | yes / no | yes / no |

Fill the cash-to-close row with the first-time-buyer page's cash table and the lender's Loan Estimate; fill the tax rows with the property-tax page's parcel worksheet; check districts on the MUD/PID page; check current incentives on the builder board.

#### A fully synthetic example (invented inputs, real 2025 rates)

A household with a $2,600 comfortable number compares a $315,000 new build in Temple (5% down, builder-funded 2-1 buydown on a 7.28% note through a preferred lender, $8,000 closing credit, lot assessed at $60,000 on January 1) with a $299,000 resale in Belton built in 2016 (5% down, 7.28% fixed, $6,000 seller credit toward closing) and with renewing a $1,850 lease.

| Line | Temple new build | Belton resale | Renting |
|---|---|---|---|
| Principal & interest, year 1 | $1,658 (5.28%) | $1,944 | $1,850 |
| Principal & interest, year 2 | $1,848 (6.28%) | $1,944 | ~$1,900 |
| Principal & interest, year 3 | $2,048 (7.28%) | $1,944 | |
| Property tax, year 1 | $118 (lot only) | $360 (homestead) | included |
| Property tax, year 2 | $432 (homestead) | $360 | |
| Mortgage insurance | $125 | $118 | |
| Insurance ÷ 12 | $200 | $233 | $20 |
| HOA | $45 | $0 | |
| Upkeep reserve | $100 | $250 | |
| **Total, year 1** | **$2,246** | **$2,906** | **$1,870** |
| **Total, year 2** | **$2,750** | **$2,906** | ~$1,920 |
| **Total, year 3** | **$2,949** | **$2,906** | |
| Cash at closing after credits | ~$17,250 | ~$17,950 | deposit |
| Clears $2,600 in year 3? | No | No | Yes |

The new build "wins" year one by $660 a month and is under the household's number. By year three it has stepped up $703 a month, with $390 of that from the buydown ending and $314 from the tax reset, and both homes are about $300 to $350 over the number. On the same assumptions, a Temple home near **$275,000** carries about $2,609 in year three, and a Belton resale near **$265,000** carries about $2,615. The honest readings are: shop a lower band, bring 20% down (which drops the Temple home to about $2,510 in year three), negotiate a permanent rate buydown or price cut instead of a temporary one, or rent another year. Buying the $315,000 home because year one fits is the mistake this test exists to catch.

Every input above is invented for arithmetic. Insurance, HOA, upkeep, lot value, credits and the 36-month selling cost are placeholders. The tax rates are Bell CAD's adopted 2025 rates; the national rate is Freddie Mac's October 1, 2026 average. None of it is a quote.

#### The downside of this test

It makes some homes look worse than a builder's or portal's sheet, and it can talk you out of a purchase you wanted. It also depends on documents other people control: the lender's written scenario, the insurer's quote, the appraisal district's value. If any of those is missing, the test is incomplete and says so. It does not forecast appreciation, rent growth or rates, and it does not tell you whether a neighborhood suits you. It is a cost test, not a life test.

#### If you want a second set of eyes

Run the test first, as far as you can. Then, if it would help, send me the two addresses and your three-year totals through the contact page and pick "Year-Two Test review." I will reply personally within one business day, usually with two or three questions, and offer a 30-minute call. After the call you get a one-page written decision note for your two addresses. That is the whole offer: no obligation, no agreement needed for the conversation, and if the right answer is "rent another year" the note will say so. Texas law requires a written agreement before I can show you a home or present an offer for you (Occupations Code 1101.563, effective January 1, 2026); we would discuss that only if you decide you want to see one of the homes.

Taylor Dasch · EG Realty · 254-718-4249 · dealswithdasch@gmail.com · Information About Brokerage Services and the TREC Consumer Protection Notice are linked in the footer.

---

*End of public resource text.*

---

## 4. The bounded personalized next step

### 4a. The intake worksheet (seven fields, on the existing contact form)

The existing contact form already collects name, email, phone, a request type, a move date, a budget, a builder-contact status and the current agent relationship. For the Year-Two Test review, the `asset_name` select gets one more option and the optional builder fields are relabeled when it is chosen. No new form.

| Field | Why it is asked | Rule |
|---|---|---|
| Request type: "Year-Two Test review (two addresses)" | Sets the exact asset for attribution and routes the reply template | Required |
| The two addresses (or one address plus "renting") | The note is about these two and nothing else | Required; two maximum |
| Your comfortable monthly number | Separates the buyer's own budget from any lender ceiling | Required; a range is fine |
| Year-three totals you got, if you ran the test | Shows what is already done and where it stalled | Optional |
| Move timing | Fixed date vs. flexible changes the advice | Required (already on form) |
| Financing status: not started / talked to a lender / written pre-approval / cash | Self-reported; the note will say "lender to confirm" | Required |
| Current agent relationship | Already on the form; protects existing representation | Required (already on form) |

Consent language and the TCPA checkbox stay exactly as they are. A download of the page or a prior CRM record is not permission to call; only the submitted form with the checked box is.

### 4b. The one-page Decision Note template

```
DECISION NOTE  ·  Year-Two Test review
Prepared for: [first name]  ·  Prepared by: Taylor Dasch, EG Realty  ·  Date: [date]
Addresses reviewed: A) [address, listing date]   B) [address, listing date]   C) Renting at $[rent]
Your comfortable number: $[X]/month (your figure, not a lender ceiling)

WHAT YOU GAVE ME / WHAT I CHECKED
- Lender scenario(s): [received / not received] from [lender], dated [date]; payment after buydown [shown / not shown]
- Bell CAD parcel records: A) entities [list], 2025 value $[ ]  B) entities [list], 2025 value $[ ]
- District check: A) [MUD/PID/none, source]  B) [MUD/PID/none, source]
- Insurance quotes: [received / placeholder used]
- Incentive sheet: A) [builder, dated, lender condition, expiration] B) [seller credit stated on MLS: yes/no]

THE TEST (monthly)                      A            B            Renting
Year 1 total                            $            $            $
Year 2 total                            $            $            $
Year 3 total                            $            $            —
Cash at closing after confirmed credits $            $            deposit $
Price needed to exit at 36 months       $            $            lease-break $
Clears your number in year 3?           yes/no       yes/no       yes/no

WHAT CHANGES THE ANSWER (ranked)
1. [the single input with the largest effect, who confirms it, by when]
2. [second]
3. [third]

MY READ (judgment, not a quote)
[Three to five sentences in plain words: which column fits, which does not, and why; where renting or waiting is the better fit, say so.]

WHAT YOU WOULD VERIFY NEXT, WHOEVER YOU WORK WITH
- Lender: [specific items]  - Insurer: [item]  - Bell CAD / title: [item]  - Builder or seller: [item in writing]

IF YOU WANT TO SEE EITHER HOME
Texas requires a written agreement before I can show a home or present an offer for you. The agreement states the services, the end date, whether it is exclusive, and the compensation, which is not set by law and is fully negotiable. We can talk through it on a call; there is no obligation from this note.

Taylor Dasch · EG Realty · 254-718-4249 · dealswithdasch@gmail.com
This note organizes your own figures and public records. It is not a loan estimate, appraisal, tax bill, inspection or legal advice. Figures dated as shown.
```

### 4c. A clearly synthetic sample note

```
DECISION NOTE  ·  Year-Two Test review   [SYNTHETIC EXAMPLE: invented household, invented homes]
Prepared for: Jordan  ·  Prepared by: Taylor Dasch, EG Realty  ·  Date: October 1, 2026
Addresses reviewed: A) new build, Temple 76502, listed 09/18/2026   B) 2016 resale, Belton 76513, listed 08/30/2026   C) Renew lease at $1,850
Your comfortable number: $2,600/month

WHAT YOU GAVE ME / WHAT I CHECKED
- Lender scenario: received from the builder's preferred lender for A only, dated 09/26/2026; shows year-1 payment, does not show year 3. No scenario for B yet.
- Bell CAD: A) Bell County, City of Temple, Temple ISD, Temple College, Bioscience District; 2025 value $60,000 (lot).  B) Bell County, City of Belton, Belton ISD; 2025 value $291,000 with the seller's homestead.
- District check: A) no MUD or PID on the parcel record; builder to confirm in writing.  B) none.
- Insurance: placeholders ($2,400 and $2,800 a year) until your quotes arrive.
- Incentive: A) 2-1 buydown plus $8,000 credit, requires preferred lender, expires 10/31/2026.  B) MLS shows seller concession field "yes"; $6,000 assumed.

THE TEST (monthly)                      A            B            Renting
Year 1 total                            $2,246       $2,906       $1,870
Year 2 total                            $2,750       $2,906       ~$1,920
Year 3 total                            $2,949       $2,906       —
Cash at closing after confirmed credits ~$17,250     ~$17,950     deposit ~$1,850
Price needed to exit at 36 months       ~$315,000    ~$299,000    lease-break: 2 months' rent
Clears your number in year 3?           No           No           Yes

WHAT CHANGES THE ANSWER (ranked)
1. Down payment. At 20% down, A carries about $2,510 in year 3 and clears your number. You confirm what cash you want to keep after closing.
2. Permanent vs. temporary buydown on A. Ask the builder in writing whether the same dollars can buy the note rate down permanently or cut the price. Lender to show year-3 payment either way.
3. B's actual insurance quote (2016 roof) and a written seller credit. Insurer and listing agent.

MY READ
Neither home fits your number by year three at 5% down; A only looks like it fits because of year one. At this price band the renting column is the honest default for 2026 unless the down payment changes. If you want to buy in the next six months, the band that fits your number on the same assumptions is roughly $265,000 to $275,000, which is right at Temple's August 2026 median of $260,000, so the inventory exists. I would not let the October 31 incentive deadline make this decision for you.

WHAT YOU WOULD VERIFY NEXT, WHOEVER YOU WORK WITH
- Lender: year-3 payment for A; a scenario for B; mortgage insurance removal terms.  - Insurer: both quotes with deductible in dollars.
- Bell CAD / title: A's finished-home estimate; any PID payoff on either.  - Builder: incentive, lot value and HOA in writing.

IF YOU WANT TO SEE EITHER HOME
Texas requires a written agreement before I can show a home or present an offer for you. It states the services, end date, exclusivity and compensation, which is not set by law and is fully negotiable. No obligation from this note.
```

### 4d. The initial reply (Taylor sends manually; drafted, not auto-sent)

> Hi [first name], Taylor Dasch with EG Realty. Thanks for sending the two addresses. I pulled both parcel records tonight; before I write anything up, two quick questions: (1) does the lender scenario you have show the payment after the buydown ends, and (2) is the move date fixed or flexible? If a 30-minute call would help, reply with two times that work this week and I'll send a link. Either way you'll get a one-page note on the two addresses. If you're already working with another agent, tell me and I'll keep this to the public numbers out of respect for that.

Rules: within one business day; no attachment on the first reply; no agreement mentioned unless they ask to see a home; nothing added to a newsletter.

### 4e. The 30-minute conversational agenda

1. **Their number and their timing (5 min).** "What's the payment you'd be comfortable with even if nothing goes right the first year?" "What happens if the move date slips?"
2. **The two columns, year three first (10 min).** Read the year-three totals out loud. Ask what surprised them. Then back up to how each line was built.
3. **The three inputs that move the answer (8 min).** Down payment, incentive structure, the missing quote. Who confirms each and by when.
4. **Taylor's read, with the downside (5 min).** Including "rent another year" when that is the read.
5. **Next step, their choice (2 min).** "Do you want the note and nothing else, or do you want to see one of these? If you want to see one, I'll send the agreement to read first; it says what I do, when it ends, and what I'd be paid, which is negotiable."

Preparation limit: 20 minutes by the assistant or Codex (parcel records, rate stack, draft table) plus 10 minutes of Taylor review before the call. Recap limit: the assistant drafts the note from Taylor's call notes in 20 minutes; Taylor edits and sends in 15. **Hard caps:** two addresses; one note; no second note, no custom comps, no showings and no builder calls before a written agreement.

### 4f. Optional two-message follow-through (permission- and timing-dependent)

- **Message 1, two days after the note, only if they said a lender or quote was pending:** "Did the [lender/insurer] get you the [item]? If the number moved, send it over and I'll update the row. No rush."
- **Message 2, at their own stated date (lease decision, incentive expiry, orders), not on a schedule:** "You mentioned [date] was the decision point. Still the plan? If anything changed on your end I'm glad to re-run the two columns."

No third touch unless they reply. If they said they were working with another agent, no follow-through at all beyond the note they asked for.

### 4g. What belongs after engagement

Everything property-specific and representational: showings and live virtual tours; a written comparable-sales review; offer and concession strategy; builder negotiation on incentive structure; inspection and repair negotiation; coordinating lender, title, insurer and appraisal; a third or fourth address. All of it starts after the written agreement, which is also when compensation is set in writing.

---

## 5. Three use cases, one resource

| Case | How the Year-Two Test applies | What not to do |
|---|---|---|
| **Relocating for any reason** (BSW, Fort Hood, McLane, Wilsonart, remote, family) | Column A and B are often a Temple and a Belton address; the parcel step catches the ISD and city-limits surprises the Temple-vs-Belton page documents. The stay-length test carries the most weight when the job or orders are time-limited. Military and medical pages remain as examples and link here; they are not gates. | Do not build a separate military or medical version. The BAH and physician-loan pages already exist; they feed the lender line. |
| **Local first purchase** | Usually one purchase column and one renting column, sometimes two purchases in different bands. Step 1 (their number) and the renting row do most of the work. Down-payment assistance flows through the first-time-buyer page's assistance table into the cash-at-closing row. | Do not prescribe buying. In the synthetic example the renting column wins at the stated number. Say so when it does. |
| **New build vs. resale** | The core case: the land-only year, the buydown schedule, the incentive conditions, the district line and the HOA all land in the same table. The builder board supplies the incentive; the parcel step supplies the finished-home value. | Do not treat the builder's year-one sheet as the comparison. Do not let an incentive deadline substitute for a decision. |

**Two distinctions the resource makes explicit, in every case:**

- **Self-reported budget vs. lender qualification.** Step 1 is the buyer's number. The lender's written scenario is a separate document. The note labels every lender figure "lender to confirm."
- **Negotiable compensation vs. any assumed standard.** The resource says, in the consumer's language, that broker compensation is not set by law and is fully negotiable, and that the written agreement states the amount or rate. No percentage is quoted anywhere on the page or in the note. Seller or builder credits are shown as credits toward the buyer's costs, not as a standard the buyer should expect.

---

## 6. Investor boundary: the existing brief intake, unchanged in spirit

Per the October 1 direction, no acquisition time or new resources go to attracting investors. Existing investor pages stay up. Repeat clients and selectively qualified inbound investors continue to be served through a brief that must be complete before any custom analysis or travel.

**Brief intake (text for the existing contact form's "Investor" request type or a reply template):**

> Thanks for reaching out about investing in Bell County. Before I run numbers or set up property time, I ask every investor for the same short brief, so the analysis is worth both our time:
> 1. **Criteria you would actually buy on:** property type, price band, minimum cash flow or return test, condition you will accept, and location limits.
> 2. **Funds or financing:** proof of funds or a lender pre-approval for the band above (a screenshot is fine; I do not need account numbers).
> 3. **Comparables:** are you willing to underwrite from current Bell County comparable sales and rents? Temple's August 2026 median sale was $260,000 and the market update showed 56% of active listings with a price cut, so there is room to negotiate; there is not a hidden tier of homes at half of value.
> 4. **Timeline and decision-maker:** when you would close and who signs.
> 5. **Prior experience:** first property or tenth; self-managed or managed.
> With that, I can tell you quickly whether I am the right fit. Looking for a discount is fine and expected; I just need the criteria to be something a Bell County listing can satisfy.

**Rules:** a deep-discount objective is never by itself disqualifying. An incomplete brief gets the brief again, politely, not a custom report. No bespoke spreadsheet, tour or travel before the brief is complete and the comparables condition is accepted. Existing obligations and repeat clients are outside this gate.

---

## 7. Evidence and legal review

| Item | What the resource does | Source, date | Open question for broker / lender / CPA |
|---|---|---|---|
| Dates and geographies | Every figure carries a date; rates are "2025 adopted," market figures are "August 2026"; cohort stated (CTXMLS Residential, MLS city field) | Bell CAD 2025 table; templetxhomes.net market pages | None |
| Property tax | Per-entity rates; $140,000 school exemption; 20% Temple/Temple College local option; 10% homestead cap after first full homestead year; protest deadline May 15 or 30 days after notice | Bell CAD; Comptroller exemptions and protests pages | **Verify** Bell County 2026 adopted rates when posted; **verify** Academy ISD rate |
| New-build first-year tax | Described as land or partial value as of January 1, then finished value | TSAHC consumer guidance; Comptroller | Lender: which value supports the initial escrow |
| Insurance | Statewide 2025 preliminary average $3,489 for scale only; quote required | TDI market overview | **Verify** Bell County average on TDI map before quoting a county figure |
| Financing | Freddie Mac 7.28%/6.60% dated October 1, 2026; payment after buydown required | Freddie Mac PMMS | Lender confirms every figure; nothing on the page is an offer |
| Concessions | Credits shown as credits; caps are lender/program rules: FHA 6%, VA 4% beyond normal costs, conventional 3/6/9% by down payment | HUD, VA, Fannie Mae as summarized by lender sources | Lender confirms the cap for the actual loan |
| Fair housing | No characterization of neighborhoods by who lives there, no "good/bad schools" judgments; TEA ratings cited as a dated data point (Temple ISD B/81 and Belton ISD B/80, released August 14, 2026) with the address-lookup instruction; no crime adjectives | TEA; HUD fair housing rules | Broker review of the page text |
| Brokerage identification | Name, brokerage, phone, email on page and note; footer IABS and CPN links; advertising includes "EG Realty" | TREC advertising rules (brokerage name required as of January 2026) | **Verify** the footer IABS is the January 1, 2026 version |
| Agency disclosure and agreements | Written agreement before showing or presenting an offer; contents listed; non-representation agreements limited to 14 days and non-exclusive; compensation stated and "not set by law and fully negotiable" | TREC article on 1101.562/1101.563 | Broker: which agreement forms EG Realty uses; when IABS is delivered in this flow (first substantive contact = the first reply) |
| Existing representation | Asked on the form; honored in the reply | Existing contact form | None |
| Seller's disclosure, MUD/PID notices, builder warranty | Named as documents to obtain | Texas Property Code 5.008; Water Code 49.452 notice; Property Code 5.014 PID notice | Title company confirms notices |
| Permission | Only the TCPA-checked form submission authorizes contact; no newsletter enrollment; no use of old CRM rows | Existing form consent text | None |
| Deductibility of MUD vs. PID | Mentioned on the existing MUD/PID page, not repeated here | | CPA question for the buyer; not advice |
| Confidentiality | The synthetic example is labeled; no client data; the note goes only to the person who requested it | | None |

---

## 8. Service economics and time

| Work | Reusable or personalized | Who | Time | Quality check |
|---|---|---|---|---|
| Year-Two Test page | Reusable; once, then dated updates | Assistant/Codex drafts from this document; Taylor reviews every number; broker reviews compliance text | Build 3 to 4 hours; Taylor review 60 min; broker review 30 min | Rate table matches Bell CAD PDF; arithmetic re-run; banned-word scan; dates present |
| Link placements on six existing pages | Reusable | Codex | 30 min | Links resolve; anchor text consistent |
| Contact form option + hidden tags + thank-you link | Reusable | Codex | 45 min plus the acceptance tests below | Test submission reaches the destination with exact asset recorded |
| Reply, agenda, note templates | Reusable | This document; Taylor edits voice once | 30 min | Taylor's words, not the template's |
| Per household: prep | Personalized | Assistant/Codex | 20 min | Parcel entities and values copied from Bell CAD, not typed from memory |
| Per household: call | Personalized | Taylor | 30 min | Agenda followed; next step stated |
| Per household: note | Personalized | Assistant drafts 20 min; Taylor edits 15 min | 35 min | Every lender figure marked "lender to confirm"; note sent by Taylor |
| **Taylor time per household** | | | **about 55 minutes** | |
| Displaced work | | | One hour of the 3:30 to 4:15 window plus 10 minutes, per household | The owner direction says selective outbound is supplemental; this is inbound conversion work |

**Escalation that is justified:** when a household has run the test, had the call and received the note, and asks to see a home. That is when the agreement is presented and full service begins. **Escalation that is not justified:** a second note, custom comps or builder calls for someone who has not signed; a note for someone who sent one address and no number (they get the public page and the two questions instead).

**The commercial mechanism, stated without a dollar claim:** better-prepared first consultations should raise the share of consultations that become written agreements (the Signed field in the appointment ledger, metric 5 in the strategy documents), which the ledger can measure in 30 to 60 days, and funded closings follow 60 to 150 days later. The owner-reported experience that inquiries rose after the pillar-video shift is a hypothesis; this offer is the conversion step for whatever inquiries arrive, not a traffic program.

**Production help saves net time only if** the assistant's prep removes Taylor's parcel lookups and table-building. If Taylor finds himself re-checking every cell, the prep is not saving time and should stop; the test then runs as a Taylor-only 45-minute flow with no note until the agreement.

**Cost and cash, separately:** zero incremental spend. No plugin, form tool, scheduler or ad is required. Codex time is the implementation cost. No capital, no borrowing, no enrollment.

---

## 9. Implementation in the existing route: three steps, each with an approval gate

**Step 1. Publish the Year-Two Test and connect it.** One WordPress page at `/year-two-test/` built from section 3, or, if Taylor prefers no new URL, as section VIII-B of the first-time-buyer page. Add a one-line link from `/first-time-home-buyers/`, `/new-construction-vs-resale-temple-tx/`, `/temple-tx-property-taxes/`, `/mud-vs-pid-taxes-temple-belton-tx/`, `/bell-county-builder-incentives/` and `/temple-vs-belton/`. Fix the three stale lines in section 2 while editing. **Gate:** Taylor approves every number against this document's sources; broker approves the compliance sentences. Nothing is published before both.

**Step 2. Give the contact route the exact asset.** Add "Year-Two Test review (two addresses)" to the existing `asset_name` select; when selected, show the existing optional fields relabeled as "Two addresses," "Your comfortable monthly number," "Year-3 totals if you ran the test"; set hidden `lead_tags` to `YearTwoTest` and `campaign` to `year-two-test`. Add the Year-Two Test to the thank-you page's resource list. **Gate:** the acceptance tests below pass on a test submission, and Taylor confirms where submissions land.

**Step 3. Stand up the reply-to-note workflow with no sends.** Save the reply, agenda and note templates where Taylor actually drafts (Gmail drafts via create_draft, or Lofty templates if that is what he uses). Each inquiry gets an appointment-ledger row with the existing August 15 fields: source `website`, exact asset `/year-two-test/`, source-evidence locator = the form submission reference, and the three qualification flags left `unknown` until confirmed on the call. **Gate:** Taylor approves the templates in his own words; the ledger write is read back before it counts.

**Contact-path acceptance tests (run once, record results):**

1. Submit the form with the new request type from a test identity. Expected: HTTP success, redirect to `/thank-you/` with a reference shown.
2. Confirm the submission is visible at the destination within 10 minutes and name the destination (Lofty record, email, ledger row). If the `fub-lead` endpoint goes nowhere Taylor uses, that is a blocker to fix before launch, not after.
3. Confirm the record carries `lead_tags=YearTwoTest`, the two addresses and the comfortable number, and that the TCPA checkbox state is stored.
4. Confirm the thank-you page link opens the Year-Two Test without a form.
5. Confirm a duplicate submission (same email, same day) does not create a second household; it updates the first.
6. Confirm Taylor receives a notification he will actually see.

**Customer effort:** seven fields, two of them already required today; no account, no download gate, no scheduler. **Handoff ownership:** the website owner (Codex task) owns steps 1 and 2; Taylor owns every reply and every note; the assistant owns prep and drafts; nobody auto-sends.

**Origin vs. assist attribution (uses the ledger's existing rule):** *origin* is the first recorded touch the household names in the reply or on the call (a specific video, a search, a referral); *assist* is the Year-Two Test page when it appears in the path but was not the first touch. The exact asset field records `/year-two-test/` only when the household says that is how they found Taylor; otherwise it records the origin asset and the page is logged as the assist. Never infer either.

---

## 10. Codex preparation handoff

**Objective:** implement steps 1 and 2 above on the WordPress site and prepare step 3's templates, with no publication until Taylor's approval and no changes to CRM data.

**Inputs supplied:** this document (section 3 text, section 4 templates, section 7 table); Bell CAD 2025 Tax Rate Table PDF (bellcad.org/wp-content/uploads/2025/09/2025-Tax-Rate-Chart.pdf); the existing page URLs named in section 2.

**Tasks:**

1. Create a draft page `/year-two-test/` from section 3, matching the site's existing section styling (the first-time-buyer page is the pattern). Render the copyable table as an HTML table with a "copy table" button; optionally add a client-side calculator that computes the three yearly totals from entered lines using the 2025 rate table, with every rate shown as an editable field and a visible "2025 adopted rates; check Bell CAD for 2026" notice. No external service, no storage of entries, no form inside the calculator.
2. Add the six inbound links in section 9, step 1, as single sentences placed after each page's most relevant section.
3. Apply the three one-line fixes in section 2.
4. Contact form: add the select option and hidden-field behavior in section 9, step 2; relabel optional fields conditionally; keep the consent checkbox and all existing options untouched.
5. Thank-you page: add the Year-Two Test to the "while you're here" list.
6. Write a test script that performs acceptance tests 1 to 6 against a staging copy or with a clearly marked test identity, and prints a pass/fail table. Do not run it against production without Taylor present.
7. Save the reply, agenda and Decision Note templates as plain-text files in the project under `templates/year-two-test/`, with Taylor's contact block and the compliance sentence verbatim.
8. Produce a review packet: diff of each page, the rendered draft page URL, and a table of every number on the page with its source and date.

**Done means:** the draft page renders with no placeholder text; the arithmetic in the synthetic example re-computes to the figures in section 3 within one dollar; the test script passes or names the exact failing step; nothing is published; no CRM write occurred.

**Out of scope:** a new CRM, a scheduler, a newsletter sequence, any investor page change, any automatic reply.

---

## 11. Before-use verification list

- [ ] Bell CAD 2025 rates on the page match the PDF line by line, including Temple College 0.2017 and the Bioscience District 0.013947.
- [ ] Bell CAD's rate page checked for a 2026 Tax Rate Table; if present, the page updates and the "2025" labels change.
- [ ] Academy ISD 2025 rate obtained from a Bell CAD parcel estimate and added.
- [ ] Freddie Mac figure re-dated to the current week before publishing; the page says "check the current weekly average."
- [ ] TDI Bell County average premium read from the county map and dated, or the county sentence removed.
- [ ] Synthetic example re-computed by Codex; every input labeled invented.
- [ ] Footer IABS confirmed as the January 1, 2026 version; CPN link resolves.
- [ ] Broker review of: the agreement sentence, the "fully negotiable" sentence, the fair-housing-neutral school and area language, and the absence of any compensation percentage.
- [ ] The `fub-lead` endpoint's destination confirmed by Taylor; if it does not reach Lofty or the ledger, fixed before launch.
- [ ] Acceptance tests 1 to 6 passed with a test identity and the results saved.
- [ ] The three stale lines in section 2 fixed.
- [ ] Templates read aloud by Taylor once and edited into his own voice.
- [ ] The appointment ledger accepts a row with exact asset `/year-two-test/` and the three flags `unknown`.
- [ ] Banned-word scan of the page text passed (none of the Quality Gate 1 terms appear).
- [ ] The CMS confirmed as WordPress by Taylor; the stored "AgentFire" preference corrected or explained.

---

## 12. Owner decisions (three)

1. **Approve the decision and the placement.** The Year-Two Test as the buyer value offer, as one page at `/year-two-test/` (recommended), or as a section of the first-time-buyer page (no new URL).
2. **Approve the bounds of the free personalized step.** Two addresses, one 30-minute call, one one-page note; no second note, comps, showings or builder calls before a written agreement; the renting answer stated when it is the honest read.
3. **Go or no-go on the October 3 to 4 Codex build,** conditional on the contact-form destination check in section 9 passing first.

---

## 13. Sources (retrieved October 1, 2026)

- Bell CAD, 2025 Tax Rate Table: https://bellcad.org/wp-content/uploads/2025/09/2025-Tax-Rate-Chart.pdf ; adopted rates page: https://bellcad.org/?p=966
- Texas Comptroller, Property Tax Exemptions (residence homestead, $140,000 school exemption, 20% local option, Form 50-114): https://comptroller.texas.gov/taxes/property-tax/exemptions/
- Texas Comptroller, Property Tax Protests (May 15 or 30 days after notice): https://comptroller.texas.gov/taxes/property-tax/protests/
- Texas Legislature, S.B. 4 (89R) bill analysis, $140,000 homestead exemption and Proposition 13: https://capitol.texas.gov/tlodocs/89R/analysis/html/SB00004F.htm
- TREC, "What Changes in 2026 About Buyer/Tenant Representation in Texas" (Occupations Code 1101.562 and 1101.563): https://www.trec.texas.gov/article/what-changes-2026-about-buyertenant-representation-texas
- Freddie Mac, Primary Mortgage Market Survey, October 1, 2026 release (30-year 7.28%, 15-year 6.60%): https://www.freddiemac.com/pmms
- Realtor.com housing inventory for Killeen-Temple, TX via FRED, August 2026 (median listing price $284,000; median days on market 72; 2,446 active listings): https://fred.stlouisfed.org/series/MEDLISPRI28660
- Texas Department of Insurance, Texas Homeowners Insurance Market Overview (2025 preliminary statewide average $3,489; 2024 $3,291): https://www.tdi.texas.gov/general/texas-homeowners-insurance-market-overview.html
- TSAHC, "Tips to Avoid Property Tax Surprises on Newly Built Homes": https://www.tsahc.org/blog/post/tips-to-avoid-property-tax-surprises-on-newly-built-homes
- KDH News, Temple ISD and Belton ISD both rated B in 2026 A-F release (August 14, 2026): https://kdhnews.com/news/region/report-cards-temple-isd-belton-isd-both-designated-b-districts-with-release-of-a-f/article_1112a7f0-5eb7-5d25-88a3-7cfd98c6a2da.html ; TEA 2026 statewide summary: https://tea.texas.gov/school-and-district-leaders/accountability/academic-accountability/performance-reporting/2026-a-f-statewide-summary.pdf
- Seller concession caps by loan type (FHA 6%, VA 4%, conventional 3/6/9%), lender summary: https://www.lower.com/mortgages/seller-concessions-by-loan-type
- Ownwell, Texas 20% non-homestead appraisal cap expiration (Tax Code 23.231, through tax year 2026): https://www.ownwell.com/blog/texas-20-percent-appraisal-cap-expiration-2027
- templetxhomes.net pages inspected: /first-time-home-buyers/, /how-much-house-can-you-afford-temple-tx/, /temple-tx-property-taxes/, /mud-vs-pid-taxes-temple-belton-tx/, /bell-county-builder-incentives/, /new-construction-vs-resale-temple-tx/, /temple-vs-belton/, /temple-tx-market-update/2026-08/, /rent-vs-buy-bsw-resident-temple-tx/, /relocation-guide/neighborhood-comparison/, /buyers/, /contact/, /thank-you/, /page-sitemap.xml
