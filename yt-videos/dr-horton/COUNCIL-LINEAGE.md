# D.R. Horton Video — Council Lineage & Decision Trail

Run: `reason-run-260723-1705/` · Config: content domain, convergent mode, 5 blind judges (Retention Engineer, Contrarian, Viewer, Analyst, Scout), convergence 2, Codex cross-lab critic default-on. Started by Fable 5; finished by Opus 4.8 (Fable hit a credit limit mid-Round-2; the run was resumed from file state, not restarted).

## Post-council edit (2026-07-24)
After convergence, Taylor decided to **remove the lawsuit entirely from the shipped video** ("I don't want to say it, I don't honestly care about it, and I don't think D.R. Horton is blatantly doing anything bad"). The G17 graphic + Robinson paragraph were deleted; check 4 keeps only the plain year-two escrow-budgeting advice. The Robinson references below are the accurate record of what the council decided *at the time* (the Santiago→Robinson correction was the right call then) — they are NOT in the final video. The live companion page was cleaned of litigation content the same day.

## Outcome
**Converged.** The synthesis candidate (AB) won Round 1 **5-0** and Round 2 **3-2** → 2 consecutive wins = convergence. A targeted reconciliation merge resolved the 3-2 split, then a Codex cross-lab final gate hardened the ship version. Winner → `VIDEO-PACKAGE.md` + component files.

## Round 1 (5-0 → AB)
- Author-A cold draft (1,641 spoken words) → **Codex cross-lab critic**: 11 FATAL / 18 MAJOR / 6 MINOR.
- **Decisive catch (Codex, then orchestrator-verified live via web search):** the draft called the escrow lawsuit "the pending Santiago class action." **Santiago was voluntarily dismissed 12/04/25 and refiled as the broader *Robinson v. D.R. Horton* (D. Nev.).** All later candidates use Robinson, attributed to court filings as allegations.
- Orchestrator adjudication (`orchestrator-verified-facts-r1.md`) settled which critic points to adopt vs which fought locked decisions; task ground truth patched with the per-community MLS breakdown.
- Author-B (compliance-hardened) + Synthesizer (AB) built. Blind judges (labels X=B, Y=AB, Z=A): **AB 5, A 0, B 0.** Candidate A was disqualified by all five on "pending Santiago" + PMMS-without-caveat + the −3.7% overclaim ("the data says it works"). AB won on loop discipline, the BBB "A+/1.07 at once" chip in the first 15s, the persona-named CTA, and the cleanest comparability framing.

## Round 2 (3-2 → AB, convergence reached)
- Author-A improved the incumbent (r2-candidate-A) → **Codex R2 critic**: 9 FATAL / 15 MAJOR / 5 MINOR.
- Orchestrator adjudication (`orchestrator-verified-facts-r2.md`): **overrode** 3 critic points that fought locked decisions — kept the **3/5 verdict** (+ a disclosed-criteria sentence), kept the **interview insert in this video** (with buyer-facing Red-Tag questions + corrected runtime math), kept the **persona-named CTA**. **Adopted** 19 accuracy fixes, incl. killing the market-wide "cheapest new construction" superlative — which also removed a **cross-video contradiction**: the channel's Stylecraft video already calls South Pointe ($225,900) "the cheapest new-construction entry in the county."
- Blind judges (labels X=AB, Y=B, Z=A): **AB 3 (Contrarian, Analyst, Scout), A 2 (Retention Engineer, Viewer), B 0.**
- The 2 dissents were informative, not noise: A won on two retention levers that don't conflict with compliance — a caveat-free 0:08 hook, and speaking the all-in monthly payment ($2,808 FHA / $2,735 VA) aloud instead of on a graphic. A carried 3 compliance-fatal overreaches its own voters didn't defend (market-wide "cheapest," "best deals die Sept 30 every year" forecast, an internal-pricing interview question). B carried 2 factual errors (Mesa Ridge + Homestead mislabeled "Final Opportunities") — AB was confirmed clean on that by the Analyst.

## Reconciliation merge (resolves the 3-2 split)
`merge-brief-r3.md` → `r3-candidate-FINAL.md`: base = converged AB, **RESTORE** A's two retention levers (move the review caveat off the spoken hook onto graphic G14a so the 0:08 open lands clean; SPEAK the all-in PITI, date-stamped), **KEEP KILLED** A's three overreaches, **VERIFY** Final Opportunities = Mesa Ridge + Three Creeks only.

## Codex final gate (the 6th-judge tiebreak) → ship version
`critic-codex-r3.md`: REVISE, 5 FATAL / 12 MAJOR / 4 MINOR. Triaged in `ship-fixlist-r3.md`:
- **Adopted (legit hardening):** identity lands ≥0:15; **Red Tag "may not be combinable — confirm in writing"** (real fine-print catch); review causality tightened with the BBB 654/741 service-repair denominator; "actives" → "active/pending"; all-in-payment definition precise; taxable-value wording fixed; BBB reframed as the national/corporate profile (not accredited, ~264-review denominator); warranty submission per the delivered booklet; title #4 de-collided to "85 Local Records"; Short S1 retitled to the national BBB profile; the "Best Deals Die Sept 30" packaging line killed; MINOR polish (BSW CTA softened, "different methodologies," "most in the sample").
- **Publish-gates (Taylor-fill placeholders, not defects):** completed IABS 1-2 URL, CPN URL, dated Stylecraft review URL, a real on-screen Pecan Creek sample address. Listed in the PUBLISH-GATE block.
- **Verified-and-rejected (Codex FATAL-4 hallucination):** Codex claimed a "fresh fetch" showed the live page serving stale March-2026 content, the expired 0.99% promo as current, and an investor section with 1%-rule analysis. **Orchestrator fetched the live page and disproved it** — page reads "Updated: July 2026," carries 4.99% (28×), the 0.99% hits are CSS noise, and there is no investor-analysis section (cap-rate / 1%-rule / cash-flow all zero; the "investor" hits are Taylor's footer tagline + schema). The one real kernel: the live PAGE still says "pending Santiago" and should be updated to Robinson (page edit for Taylor, not a video change). Verifying before acting prevented a false "your deploy failed" alarm.

## Honest limits
- The 5 judges + critics are rigor-disciplined model outputs; the Codex critic is the one genuine cross-lab (OpenAI) voice. Treat 5-0/3-2 as "no internal contradictions survived," not "humans agreed."
- Every ⚠️ VOLATILE number in `sources-rate-claim.md` (rates, MLS, review counts, docket status, Stylecraft's competing offer) must be re-pulled the morning of filming — they drift.

## File map
`task-block.md` (brief + ground truth) · `orchestrator-verified-facts-r1/r2.md` (adjudications) · `critic-codex-r1/r2/r3.md` (cross-lab critiques) · `r1-/r2-/r3-candidate-*.md` (all drafts) · `merge-brief-r3.md` · `ship-fixlist-r3.md` · `r3-candidate-SHIP.md` (winner) · `reason-lineage.jsonl` (machine trace).
