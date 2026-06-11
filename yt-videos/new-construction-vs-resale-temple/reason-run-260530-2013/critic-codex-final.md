**FATAL WEAKNESSES (must fix or kill):**
1. `"Banned-word landmine: MLS public remarks contain "stunning"/"perfect" ..."` and `"Banned-word sweep (clean): no dream / dream home, charming... stunning, gorgeous"` — Your own notes fail the “anywhere” banned-vocab gate. A scanner does not care that it is meta commentary. — Rewrite: `Banned vocabulary checked against governance list; clean across VO, on-screen copy, thumbnails, CTA, and production notes. Do not quote MLS adjective copy in this package.`

2. `"new-construction pull median $294,340/DOM104 (brief $294,900/106)"` and `"median $294,340 / DOM 104 / n=381"` — Fatal number drift. The locked public truth is `$294,900 / DOM 106 / n=461`. Alternate validation numbers do not belong in a shoot package. — Rewrite: `All public and production-facing new-construction stats use: median $294,900, $174/sqft, DOM 106, n=461. Keep alternate audit pulls out of the creative package.`

3. `"Over a 30-year hold..."` and `"you're ready to budget for CapEx like roof and HVAC"` — Buyer-lane leak. “Hold” and “CapEx” are investor/asset language in a video that explicitly cannot sound investor-framed. — Rewrite: `Over a 30-year mortgage term...` and `budget for major repairs like roof, HVAC, plumbing, and foundation work.`

**MAJOR WEAKNESSES (fix to ship cleanly):**
1. `"A lot of Temple's newer subdivisions sit inside a MUD or a PID..."` followed by `"Bell County MUD Number One covers the Three Creeks... out by Belton"` — A Temple local can screenshot this and say, “Three Creeks is Belton.” Real Bell County proof is not the same as proving “a lot of Temple.” — Rewrite: `Some newer Bell County / Temple-area developments may carry district taxes or assessments. Three Creeks near Belton is a public-record example. Do not assume either way on a Temple address; verify the exact parcel in writing.`

2. `"A resale in an established Temple neighborhood usually has none of it."` — Too broad. Some resale can still be in a district; some newer resale definitely can be. — Rewrite: `Many older established resales may not carry that extra district assessment, but verify the exact address before you compare payments.`

3. `"builders here are buying mortgage rates down to around 3.5%, some all the way to 2.99%"` — Rate-ad compliance risk. No terms, APR, qualification, expiration, lender tie, or “as of May 30” qualifier in the spoken line. — Rewrite: `As of the May 30 builder-incentive feed, selected homes advertised buydown offers around 3.5%, with some 2.99% offers, subject to lender terms, buyer qualification, fees, and change.`

4. `"it costs you nothing... the builder pays the buyer's agent out of their budget either way. Walking in alone doesn't save you a dollar"` — Too absolute for 2026 commission/representation compliance. — Rewrite: `In many builder deals, if your agent is registered before you tour, the builder has already budgeted buyer-agent compensation, so it typically costs you nothing out of pocket. Confirm it in writing.`

5. `"A builder holding a finished home for three-plus months is paying interest, taxes, and insurance..."` — DOM does not prove every home was finished and carried for 106 days. MLS DOM can include construction/listing timing. — Rewrite: `When a finished spec home sits on the MLS, the builder may be carrying interest, taxes, and insurance, and that can create negotiating pressure.`

6. `"Budget three to eight thousand a year for that — it's a line item, not a maybe."` — Unsupported by the supplied ground truth and too universal for resale. — Rewrite: `Budget for repairs based on inspection, age, and condition; roof, HVAC, plumbing, and foundation risk are property-specific.`

7. `"Sellers right now hand out fewer concessions than a builder chasing year-end inventory."` — “Year-end” is wrong or stale if this publishes mid-2026. — Rewrite: `Sellers often offer fewer visible incentives than builders trying to clear finished inventory.`

8. `"before you fall for a floor plan"`, `"model home runs you"`, `"leashed to the builder's in-house lender"` — The copy claims neutrality, but the diction is anti-builder. — Rewrite with neutral analyst language: `before you choose a floor plan`, `before the model-home process frames the decision`, `tied to the builder's preferred lender`.

**MINOR WEAKNESSES (polish):**
1. `Title: "New vs Resale in Temple TX: The 46-Day Gap"` plus hook `"about a month and a half longer"` — The title and hook pre-pay the Section 4 reveal. — Rewrite the Section 4 payoff as `why the 46-day gap changes your negotiation strategy`, not “here’s the number.”

2. `"left, a new build on bare sod, zero trees; right, a tree-lined resale street"` — Thumbnail bakes in an anti-new-construction bias. — Rewrite: `new-build street with young landscaping vs established resale street`.

3. `"This is the 76502 Power Zip"` — Insider brand phrase may not mean anything to relocators. — Rewrite: `76502 is one of the main Temple ZIP codes where I track this resale inventory closely.`

**DOMAIN CHECKS:**
1. Entity timing — PASS. Hook has no entity; body Section 1 starts: `"I'm Taylor Dasch with EG Realty..."`.

2. Banned vocab — FAIL. Notes contain banned terms in `"Banned-word landmine..."` and `"Banned-word sweep (clean)..."`.

3. Lane leak — FAIL. `"30-year hold"` and `"CapEx"` are investor-lane terms.

4. Number drift — FAIL. `"median $294,340 / DOM 104 / n=381"` conflicts with locked `$294,900 / DOM 106 / n=461`. The hook’s “month and a half” is accurate for 46 days.

5. Position consistency — PASS with rewrite risk. MUD/PID warning is specific; model-home agent line is present; physician-loan warning is present. The “costs you nothing” wording needs qualification.

6. Fairness balance — FAIL. Scar count is roughly symmetric, but language is not: “trap,” “fall for,” “runs you,” and “leashed” tilt anti-builder.

7. Temple-specific proof — FAIL as written. It names real districts and builders, but the strongest MUD example is Three Creeks near Belton, which weakens the Temple-specific claim.

8. Forward-looking/compliance risk — FAIL. Rate offers, “year-end inventory,” “costs you nothing,” and “rate resets around Year 4” need qualifiers.

9. Retention honesty — FAIL. Pairing A and the hook front-load the 46-day reveal; Section 4 needs to pay off leverage mechanics, not pretend the number is still hidden.

10. Decision usefulness — PASS. The Section 6 matrix gives real self-selection gates, but it should be simplified and stripped of jargon.

**VERDICT:** The most damaging flaw is that the package loudly claims verification discipline while leaving screenshot-ready proof of drift, banned vocabulary, and overclaimed local specificity inside the artifact.
