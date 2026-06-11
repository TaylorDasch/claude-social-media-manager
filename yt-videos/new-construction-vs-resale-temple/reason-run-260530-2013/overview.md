# Council Run — New Construction vs. Resale in Temple TX (flagship YouTube)

**Date:** 2026-05-30 · **Skill:** /council → autoresearch:reason · **Domain:** content
**Config:** 5 blind judges (Retention-Engineer, Contrarian, Viewer-Proxy, Analyst, Scout), 3 iterations, convergence=2
**Result:** ✅ Converged on **Candidate B** after 3 rounds (a real convergence — B beat the synthesis in rounds 2 and 3).

## Vote trace
| Round | Winner | Votes (A / B / AB) | Incumbent after |
|---|---|---|---|
| 1 | AB | 0 / 1 / 4 | AB |
| 2 | B | 0 / 3 / 2 | B (flip) |
| 3 | B | 0 / 4 / 1 | B → converged |

## Top catches the adversarial loop locked in (what a one-pass draft would have shipped)

1. **A 404'd CTA funnel.** Round 1 caught that the working slug `/new-construction-vs-resale-temple-tx/` returns HTTP 404. The live page is `/new-construction-vs-resale/`. The wrong slug had been wired through the description, UTM, and pinned comment — every CTA would have dead-ended. Corrected everywhere.

2. **Fabricated incentive data (fed in by the brief).** The ground-truth pack claimed "Omega carrying $200K+ in spec-home price drops." Rounds 2–3 independently grepped the live builder-incentive feed (`generated_at` 2026-05-30 10:20) and found **no Omega and no $200K figure**. The claim was killed; Section 4 now names only the feed's actual active builders (Flintrock, Sandor, Hodges, Jerry Wright) and uses a closed-MLS *pattern* for price-drop proof rather than a fabricated dollar figure.

3. **Invented Temple-specificity → real public record.** The brief required "named MUD/PID districts." Early drafts either stayed generic (reads as outsider/AI voice) or risked inventing names. The winner sources **real, public-record districts** — Bell County MUD No. 1 (Three Creeks, near Belton), MUD No. 2, WCID #5 — spoken as local knowledge, never page-attributed.

## Secondary catches
- **Numbers-drift guard in the hook:** an early hook said the slower home sat "almost three and a half months longer" — overstating the 46-day gap. Locked to "a month and a half" so the Section-4 payoff doesn't crack.
- **Source-separation discipline:** builder *names* (page + MLS) vs *live buydowns* (feed) vs *price-drop proof* (closed MLS) are kept separate so no claim is mis-attributed on camera.
- **Page-consistency flag:** live page shows resale "~$265K / Updated April 2026"; video uses "$260,000 / May 2026." Resolved by labeling every card "Temple MLS, May 2026" + a recommended low-risk page edit to sync.
- **Retention honesty:** the "Leverage Flip" anti-sag move was tightened to pay ONE loop and open exactly ONE forward question (early drafts stacked a second cliffhanger + a "stay to the end" magnet tax).
- **Credibility discipline:** the 4 credentials are split across the runtime (never stacked on the retention peak).

## Files
- `council-winner.md` — the converged package (master)
- `script.md` — shoot-ready final (after Codex cross-lab gate)
- `thumbnail-brief.md` — 3 Pikzels-ready title/thumbnail pairings
- `codex-critic-prompt.txt` / `codex-critique.md` — cross-lab adversarial gate
- `lineage.md` — full round-by-round critic + judge trail

## Honest limits
- The "5 judges" are rigor-disciplined outputs from one model family — treat 4–1 as "no internal contradictions," not "4 humans agreed." Mitigated by the Codex (OpenAI) cross-lab gate on the winner.
- Stat claims should be re-pulled the morning of the shoot — MLS drifts.
- Specific-address MUD/PID status must be verified with the city/county before stating it on camera (the script's on-screen guardrail covers this).
