# Council Reason-Run Lineage — Temple Investor Buy Boxes video

**Date:** 2026-06-13 · **Domain:** content · **Mode:** convergent · **Judges:** 5 · **Iterations:** 3 (conv=2)
**Result:** Converged in 2 rounds. Synthesis (AB) won Round 1 **5–0**, Round 2 **4–1** → 2 consecutive wins.

## Round-by-round
| Round | A | B | AB | Winner | Note |
|---|---|---|---|---|---|
| 1 | 0 | 0 | **5** | AB | Critic verdict: "SHIP WITH FIXES — nails the honest frame." Synthesis swept. |
| 2 | 0 | 1 | **4** | AB | AB repeats → converged. |

## Pipeline (per round, cold-start context-isolated agents)
Author-A → adversarial Critic (candidate+facts only) → Author-B (task+A+critique) → Synthesizer (task+A+B) → 5 blind judges (randomized X/Y/Z labels, per-round permutation). Then a derive-assets agent produced talking-points/thumbnail/description/shot-list from the winner.

## Top frame-corrections the loop locked in (what a one-pass draft would have shipped wrong)
1. **Honest-leverage spine enforced** — every claim reconciled to "negative/breakeven at 25% down; only the self-managed MTR is positive." Killed any implicit "Temple cash flows" hype.
2. **Morgan's Point precision** — Belton-addressed lake community, NOT Lake Pointe; appreciation play with the friendliest rent ratio in its tier, never a cash-flow play at leverage.
3. **Turnkey rarity quantified** — only 6 truly turnkey 3-2s ≤$180K in a full year; framed patience as the strategy.
4. **Entity declaration placed after the hook** (not first 15s); zero banned words; investor lane held.

## POST-CONVERGENCE correction (rental data arrived mid-run)
Taylor added `market-monitor/rental-data-bell.csv` (432 Temple lease comps) AFTER the council launched on operator-estimated rents. Applied a precision fact-correction pass + reconciliation:
- Provenance flipped: LTR rents now **MLS-verified** (was "MLS has zero rent data"). Exceptions flagged: MTR = Furnished Finder; Morgan's Point = thin-comp estimate.
- New insight added: **the rehab IS the rent lever** — as-is hospital 3-2 leases $1,395 (−$222/mo) vs renovated $1,650 (breakeven). $30K rehab = ~$255/mo swing.
- Rents corrected to MLS medians: hospital as-is $1,395 / reno $1,650; Canyon Creek $1,595; duplex $1,300/side (EXACT MLS match, 81 records); 76502 $1,500; West Temple $1,650.
- All-in / rent / rent-to-price / CF reconciled across script + talking-points + description + shot-list (verified consistent).

## Cross-lab
Codex (OpenAI, codex-cli 0.128.0) ran a final adversarial critique on the corrected script — see CODEX-CRITIQUE.md.

## Raw council artifacts
`_council-raw/` — pre-correction converged script, original assets, lineage.json.
