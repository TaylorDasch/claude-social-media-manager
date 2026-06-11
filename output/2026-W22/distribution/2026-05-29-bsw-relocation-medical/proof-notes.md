# Proof Notes — BSW Medical Relocation Cluster

Status: DRAFT. Evidence backbone for every claim in `platform-drafts.md`. If a claim is not in Section A, B, or C (structural) below, it does not ship externally.

Confidence levels (per `governance/FACT-HANDLING.md`): VERIFIED · DATED · ESTIMATED · CONTESTED · DO-NOT-USE.

---

## Section A — VERIFIED, use freely (with date)

| # | Public-safe wording | Source | Date | Conf |
| --- | --- | --- | --- | --- |
| A1 | Temple's median sale price is about $274,000, with homes taking a median of ~72 days to sell | market-monitor `closed-temple-belton-0-365.csv` (closed sales, trailing ~12 mo), n=1,481 | file 2026-05-24 | VERIFIED |
| A2 | A recent MLS pull puts the Temple median near $280,000 and median days-on-market around 68 | market-monitor `may-23-market-data.csv`, n=1,261 | 2026-05-23 | VERIFIED |
| A3 | In the $250K–$450K band (where most relocating staff buy), the Temple median is ~$300,000 and median days-on-market ~81 | market-monitor `closed-temple-belton-0-365.csv`, n=779 | 2026-05-24 | VERIFIED |
| A4 | The Match Day page is the highest-CTR BSW page on the site (5.12% CTR, position 8.9) | Google Search Console, sc-domain:templetxhomes.net, window 2026-02-28→2026-05-28 | pulled 2026-05-28 | VERIFIED |
| A5 | The BSW childcare guide page draws real search demand (593 impressions, position 9.8) | GSC, same window | pulled 2026-05-28 | VERIFIED |
| A6 | The physician-mortgage page gets 1,137 impressions but sits at position 55.6 (a ranking problem, not a demand problem) | GSC, same window | pulled 2026-05-28 | VERIFIED |

Read for copy: ~72 days on market and a balanced market means relocating buyers have negotiating room and time for inspections — no bidding-war pressure. This is the honest, current, defensible market line.

---

## Section B — PAGE-PUBLISHED, use with attribution + verify note

Cite as "as published on templetxhomes.net, [date]" and carry a `[verify before external use]` flag where noted. These come from Taylor's own pages; they are usable for context but are secondary sources.

| # | Public-safe wording | Source page | Date | Verify? |
| --- | --- | --- | --- | --- |
| B1 | Match Day 2026 was March 20, 2026 (NRMP) | Match Day page (schema Event) + relocation page | 2026-03-09/19 | Settled (schema-backed). Note: physician page says "March 17" — that page is wrong |
| B2 | BSW GME orientation is June 22, 2026 (Mayborn Auditorium); nurse residency orientation June 15, 2026 | Match Day page (schema Event); relocation page | 2026-03-09 | Verify against current BSW GME calendar |
| B3 | The window from Match Day to orientation is about 94 days; residents arrive late May to mid-June | Match Day + relocation pages | 2026-03 | Settled |
| B4 | BSW Temple is the only Level I Trauma Center between Dallas and Austin | relocation page (states "verified active through Sept 2026") | 2026-03 | Verify (low risk) |
| B5 | BSW Temple is one of Bell County's largest employers (page states ~8,884 staff) | relocation page | 2026-03 | Verify vs BSW; Gate 9 180-day window |
| B6 | A physician loan can close using only a signed BSW employment contract, up to ~90 days before the start date | physician + relocation + roadmap pages (consistent) | 2026-03 | Category fact; do NOT promise eligibility |
| B7 | Some physician loan programs offer 0% down and no PMI, and count student loans at the IDR payment rather than the full balance; terms vary by lender | physician page (Extraco, BMO, First Horizon, First Financial, Texell CU named) | 2026-03 | Describe category only; "verify with lender" |
| B8 | Physician loan rates typically run ~0.125%–0.50% above conventional — the page itself says conventional sometimes wins for attendings with cash | physician page Taylor's Take | 2026-03 | Honest tradeoff; keep |
| B9 | Most physician loan programs require a primary residence (not investment) and a ~700 minimum credit score | physician page | 2026-03 | Category fact |
| B10 | "I've completed 15+ sight-unseen transactions for BSW relocators" and do video walkthroughs covering HVAC age, foundation, daytime-sleep bedroom orientation, and noise | Match Day page | 2026-03 | Taylor confirm count before posting |
| B11 | BSW main campus is at 2401 S 31st St, Temple | commute + relocation pages | 2026-03 | Settled |
| B12 | Living 5 minutes from BSW can still mean a 12–20 minute door-to-department time once parking and shuttles are counted | commute page | 2026-03 | Strong, distinctive — keep |
| B13 | West Adams / Outer Loop construction adds roughly 10–15 minutes to some BSW commutes through late 2026 | commute page | 2026-03 | Verify TxDOT timeline |
| B14 | A Temple mailing address does not guarantee Temple ISD zoning; some "Temple" homes are Belton or Academy ISD — verify by address at Bell CAD | commute + roadmap pages | 2026-03 | Settled, important for fair-housing-safe framing |
| B15 | Bell County property taxes are high relative to no-income-tax expectations — budget roughly 2%+ of value annually; file the homestead exemption immediately after closing (it is not automatic) | all three pages (rate quoted 1.68%–2.5% — see D3) | 2026-03 | Use "roughly 2%+"; do not cite a single contested rate |

---

## Section C — ESTIMATES / RESEARCH-DOC ONLY (childcare)

Source: `bsw-pages/Childcare Guide for Temple Medical Families.md` (footnoted research doc, figures labeled "2026 Est."). **Use the STRUCTURAL facts (C1–C5). Treat all dollar/waitlist numbers as estimates — mark `[estimate — verify]` and do not present as hard fact.**

| # | Public-safe wording | Conf | Handling |
| --- | --- | --- | --- |
| C1 | BSW Temple does not operate a dedicated on-site childcare center for employees | DATED (research doc) | Strong structural fact — verify with BSW HR before external use |
| C2 | Standard daycare hours of roughly 6 AM–6 PM don't line up with hospital shift schedules | VERIFIED (structural/logical) | Use freely |
| C3 | Infant childcare waitlists in the Temple/Austin region can run several months to over a year — long enough that a March match often can't clear a waitlist before a June/July start | ESTIMATED | Frame as "can run several months to a year+"; mark estimate |
| C4 | Cornerstone Learning Academy (109 S General Bruce Dr, Temple 76504) is the one named center listed with extended hours to 8 PM | DATED (research doc) | Verify by calling the center before naming it externally |
| C5 | Part-time infant care is hard to find — centers rarely "timeshare" an infant crib, so families often pay full-time rates | ESTIMATED | Use as structural reality |
| C6 | Temple infant care estimated ~$880–$1,000/mo vs Austin ~$1,400–$1,750/mo | ESTIMATED | Only with `[estimate — verify]`; prefer not to lead with dollars |

Behavioral insight for copy (defensible, not a number): **childcare is the relocation step medical families start last and should start first** — because the waitlist clock can outrun the match-to-start clock.

---

## Section D — CONTESTED, DO NOT cite externally until pages reconciled

These are real conflicts found across Taylor's own pages. They become site-fix tasks (see `seo-geo-aeo-amplification.md` + `quality-check.md`). **Do not put any of these numbers in a post.**

- **D1 — Median home price**: pages say $245,000 / $246,538 / $255K / $255–260K. → Use MLS instead (A1–A3: ~$274K). All pages are stale-low.
- **D2 — Match Day date**: March 20 (correct, schema/NRMP) vs March 17 (physician page — wrong).
- **D3 — Property-tax effective rate**: 1.68% vs 2.18% vs 2.2–2.5%. → Use "roughly 2%+" only (B15).
- **D4 — Rent vs buy**: physician page says buying wins for 3+ yr residencies (break-even ~2.5 yr); roadmap page says 3-yr residents should rent. **Opposite advice to the same person.** → Social uses the defensible synthesis (D-syn below).
- **D5 — GME program count**: "31 programs" vs "125+". (The 125 likely conflates the VA's 125 affiliation agreements.) → Avoid stating a count, or say "30+."
- **D6 — Bed count**: 636 / 640. → "~640-bed" is fine.
- **D7 — Cost of living**: "16.3% below" vs "-13%". → "well below the national average," no number.
- **D8 — Per-neighborhood price/commute/ISD**: Lake Pointe 15-18 vs 10-12 min; Wyndham Hill Academy vs Belton ISD; Bella Terra $305K vs $419K low end; Prairie Ridge, Hills of Westwood, Canyon Creek ranges all differ between pages. → Do not cite specific neighborhood prices/commutes externally; speak in role/zone generalities and point people to the page.
- **D9 — Track record**: "$28.5M+" (pages) vs "$30M+ / 100+ transactions / #28 of 2,013 Bell County agents" (CLAUDE.md). → Omit the dollar/deal figure from posts until reconciled.

**D-syn (the rent-vs-buy line we WILL use, honest + defensible):**
> Whether buying beats renting comes down to how long you'll be here. A 1–2 year prelim year? Renting almost always wins — selling costs eat any equity. A 3-year residency is the real toss-up where the math is close. A 4–7 year track or fellowship-to-attending path? Buying usually pulls ahead. Run your specific number before you decide.

---

## Section E — COMPLIANCE WORDING (loan / benefit / endorsement)

Bake these into every asset:

- **Loan claims** → describe the category, never promise the outcome.
  - SAY: "Some lenders offer physician loan programs with 0% down and no PMI, and many let residents qualify on a signed contract before their start date. Terms and eligibility vary by lender and your situation."
  - NEVER SAY: "You'll get 0% down," "You'll be approved," "You'll save $X," "You qualify."
- **Employment / relocation benefits** → "BSW relocation benefits vary by role, and residents and attendings are treated differently. Confirm your specific eligibility with the BSW GME office." Never state a resident gets a specific stipend.
- **BSW endorsement** → "I'm an independent real estate agent who helps people relocating for BSW. I'm not affiliated with or endorsed by Baylor Scott & White." Use the hospital only as employer/landmark.
- **Salary figures** (PGY-1 $70,993, attending $300K+) → page-published estimates; do NOT state as fact in social. If income is referenced, keep it general ("a resident stipend").

---

## Section F — NEVER PUBLISH (PII / off-limits)

- BSW GME director name + direct phone/email, Physician Well-Being staff names (appear on the relocation/childcare research) — internal contacts, not for social.
- Specific apartment-complex "avoid" call-outs by name (e.g., "Avoid Carmel Village") — defamation/fair-housing risk in social; keep neighborhood guidance structural (noise corridor, not "avoid X complex").
- Any client name or transaction address tied to the "15+ sight-unseen" claim.

---

## Entity block (drop-in, Gate 2 compliant)

> Taylor Dasch with EG Realty, a real estate agent in Temple, TX. Call or text 254-718-4249 · dealswithdasch@gmail.com · templetxhomes.net
