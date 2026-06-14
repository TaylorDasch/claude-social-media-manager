# Council Lineage — Sellers "Builders Are Your Competition" Video
**Run date:** 2026-06-13 · **Engine:** adversarial workflow (3 frames → 2 critics → 1 synthesis → 5 judges) · **Cross-lab:** Codex (GPT-5.4) used as one critic · **Convergence:** judges avg **89/100**, 0 blockers, 0 Fair-Housing fails, 0 overpromise fails, 0 banned words.

## Ground truth (verified before drafting)
- **market-monitor MCP, june-13-market-data.csv:** Temple median list $279K, median DOM 71 (n=1,713); Belton median list $330K, median DOM 71 (n=706).
- **Builder incentive feed (generated 2026-06-13, Belton source):** 32 active incentive packages detected; verified deep cuts — Sandor/Pecan Meadow −$79K (95 DOM); 5818 Hamlet −$50.1K +$5K credit (82 DOM); 5712 Red Fish −$56K (145 DOM); 815 Liberty Park (Nirmaan) −$5.9K +$10K credit (135 DOM); specs at 250–400 DOM; preferred-lender requirements common.
- **new-construction-mls-data.csv (May 19):** 1,123 Bell County new-construction listings, median DOM 77; Temple = 381 (most in region).
- **Locked from published May "New vs Resale" pillar:** new $294,900 vs resale $260,000; $174 vs $149/sqft; DOM 106 vs 60 (46-day gap); MUD/PID $2–5K/yr ≈ +$267/mo ≈ $96K/30yr (Bell County MUD No.1 @ Three Creeks).
- **Existing-content audit:** /sellers/ page is live (pricing/process/compliance focus, no builder-competition angle); buyer "new vs resale" video already exists — this video flips to the SELLER seat to avoid duplication.

## Frames generated (3 distinct angles)
1. **Hidden-Tax Moat** — permanent district cost vs. temporary discount (MUD/PID lead).
2. **32-Incentive Reality Check** — read the live board, position against it (data lead).
3. **Out-Position, Don't Out-Discount** — 3 levers a spec home can't match (seller-playbook lead). ← **chosen spine.**

## Critic verdict (Codex cross-lab + Claude contrarian)
- **Winning blend:** Frame 3 spine + Frame 2's live-board hook + Frame 1's one knockout MUD line & caveat discipline.
- Key frame errors caught & corrected: "moat/permanent" too absolute → made conditional; "can't match" overbroad → "levers many resale homes have that a spec's incentive doesn't address"; outcome-coded "winning/losing move" → "costlier approach"; three-dataset collision (June feed / May new-con / locked May analysis) → labeled separately so DOM 60/106 never collides with today's 71.

## Judge scoreboard
| Judge | Score | Verdict | FH | Overpromise | Verified data |
|---|---|---|---|---|---|
| Retention Engineer | 88 | ship | ✅ | ✅ | ✅ |
| Contrarian / Skeptic | 88 | ship | ✅ | ✅ | ✅ |
| Temple Seller (viewer) | 89 | ship | ✅ | ✅ | ✅ |
| Compliance & Data Analyst | 91 | ship | ✅ | ✅ | ✅ |
| SEO / Distribution Scout | 88 | ship | ✅ | ✅ | ✅ |

## Must-fixes applied to the final package
- **[Compliance, top catch]** "~17% premium" now tied ONLY to the per-sqft pair ($174 vs $149 = 16.8%); median pair ($294,900 vs $260,000 ≈ 13%) carries no % on screen. Prevented a verifiably-wrong stat.
- **[Compliance]** Count reframed "detected / showing on the board" (signals, not verified contracts) + date-stamped spoken & on-screen. Lever 2 RESPA hedge added ("may or may not beat the buydown — the buyer's call").
- **[Retention]** Hook A reordered so the seller callout lands by ~sec 3; Lever 3 opens with a re-hook (relocation-timeline strength) before the caveat; honest-negative trimmed (cut duplicate "71 days"); playbook $/sqft VO simplified (graphic carries the figures); CTA tightened to ~40s.
- **[Viewer]** Temple-anchor line added (~1:00, "381 new-construction listings"); "I check your district status in the free review" surfaced inside Lever 1; plain-English anchor tying the 60-day figure to "not a promise yours hits it."
- **[Contrarian]** Soft "mature trees / sqft per dollar" → "finished yard the buyer doesn't pay to add"; "rational value" → "different total-cost package, not a cheaper house"; thumbnail card de-identified ("▼ $79K"); 5 hooks differentiated into genuinely distinct angles (added Temple-381 hook E); DOM chips given identical source labels.
- **[SEO]** YouTube title swapped to keyword-front-loaded "Selling a Home in Temple TX? Builders Are Your Competition" (curiosity line → thumbnail/H1); VideoObject `@id` linkage to site agent entity + thumbnailUrl array; thumbnail chip made market-neutral ("Bell County: 32 builder discounts"); $79K superlative softened to "one of the deepest."

## Honest limits
- Single-Anthropic-model judges + one Codex cross-lab voice; treat scores as "no internal contradictions," not human consensus.
- Builder-incentive count, the four example cuts, and today's medians/DOM **drift** — re-pull day-of-filming (see VIDEO-PACKAGE.md §8). Locked May figures are quoted, not re-derived.
- New-construction inventory (381 Temple) is a mid-May figure; refresh or label as such.

## Files
- `VIDEO-PACKAGE.md` — master, all 8 deliverables, corrected.
- `videoobject-schema.json` — drop-in JSON-LD.
- Raw council output: `/private/tmp/.../tasks/wsai5jo0u.output` (frames, critiques, judge JSON).
