# Lineage — Round-by-Round Trace

## Round 1 — Cold start

**Author-A produces Candidate A** (cold context, task only)
- Word count: ~2,800
- Stand-out: complete deliverables in all 8 required categories; voice + lane compliance maintained
- Weakness profile (per Critic): 2 FATAL + 7 MAJOR + 3 MINOR

**Critic attacks A**
- FATAL #1: Hook at 0:15 promises "60-second decision," direct answer doesn't arrive until 1:00 (45s identity block bleeds retention)
- FATAL #2: Walkthrough demo narrates three deflections but writes only ONE verbatim rebuttal — viewer cannot memorize under social pressure
- MAJOR (7): lender section structural pitch asymmetry; 87% County View headline sample-size dishonest; Title #3 "Lost $40M to Temple Builders" misframing; no mid-roll CTAs; residency-to-closing timing math missing; walkthrough demo narrated not visually cued; CTA path circular (description says "pinned in comments," pinned comment says "in description")
- MINOR (3): Title #1 vague; Stark Law in pinned comment lacks setup; "same as any other sale" overstates the parallel
- VERDICT: hook+deflection FATAL gaps mean the video fails on core retention promise and core deliverable

**Author-B addresses critique**
- Word count: ~3,200
- Restructured: direct answer in first 25s, identity at 0:25-1:00, three verbatim deflection scripts, cut markers throughout script, mid-roll CTAs at 2:30 and 5:45, three lender CATEGORIES (parallel structure), residency-to-closing timing math added, thumbnail #3 changed to Parks at Westfield (defensible 29-sample anchor), CTA path repaired

**Synthesizer produces AB**
- Word count: ~3,400
- Take from A: dense authority block (BP Featured, $27M, 76502 Power Zip), rhetorically sharper "you can repeat that" close on Stark Law, more complete on-camera identity statement
- Take from B: direct-answer-first structure, three verbatim deflection scripts, cut markers, mid-roll CTAs, parallel lender categories, defensible Title #3, residency timing math, repaired CTA path

**Round 1 Vote (label map X=AB, Y=A, Z=B):**

| Judge | Persona | Winner | Decoded |
|---|---|---|---|
| 1 | Retention Engineer | X | AB |
| 2 | Contrarian | X | AB |
| 3 | BSW Resident Viewer | X | AB |
| 4 | Real Estate Analyst | X | AB |
| 5 | Scout | X | AB |

**Tally:** AB 5 / A 0 / B 0 → **AB wins (consecutive_wins = 1)**

Scout surfaced four remaining gaps for Round 2 attack surface:
- Toured-without-1502 recovery script
- Builder-registration handcuff trap
- Earnest money structure for new construction
- Virtual-tour vs in-person-tour distinction

---

## Round 2 — Incumbent = AB

**Author-A' produces Candidate A'** (incumbent = AB, cold context)
- Word count: ~3,600, runtime ~9:40
- Improvements over AB: integrated registration handcuff (4:30) + recovery script (4:55) + earnest money callout (5:55-6:00); tightened lender section; added Short #4 (registration handcuff)
- Title #3 changed (regression): replaced "55% Walked Into..." with "145 BSW-Adjacent Buyers Walked Into Temple Builds Alone"

**Critic attacks A'**
- 0 FATAL + 4 MAJOR + 4 MINOR
- MAJOR #1: Runtime ceiling ~9:40 puts video at long-tail-explainer threshold
- MAJOR #2: Earnest money tack-on creates anxiety without resolution
- MAJOR #3: Title #3 regression — "BSW-Adjacent" jargon weaker than "55% subdivision specificity"
- MAJOR #4: Recovery script under-builds the post-30-day case
- MINOR (4): procuring-cause not named; "minute eight" timestamp drift; registration framing too paranoid; mid-roll #1 timing shaved

**Author-B' addresses critique**
- Word count: ~3,800, runtime ~9:05
- Cuts earnest money tack-on (defers to Calendly)
- Restores AB Title #3 ("55% of Buyers Walked Into This Temple Subdivision Alone")
- Names "procuring cause" as the legal term for the registration handcuff
- Extends recovery script with post-30-day legal/compliance vs sales-side posture
- Softens registration framing
- Moves "minute eight" promise to "the last third of this video"
- Tightens lender section ~25s

**Synthesizer produces AB'**
- Word count: ~3,900, runtime ~9:10
- Takes all of B's structural improvements
- Adds one rhetorical compression: closing callback "Sixty-second move. Sign the 1502 before you tour. That's all of it. Get represented before the model home, not after." — creates hook-to-close structural symmetry on the "60-second move" anchor

**Round 2 Vote (label map X=B', Y=AB', Z=A'):**

| Judge | Persona | Winner | Decoded |
|---|---|---|---|
| 1 | Retention Engineer | Y | AB' |
| 2 | Contrarian | Y | AB' |
| 3 | BSW Resident Viewer | Y | AB' |
| 4 | Real Estate Analyst | Y | AB' |
| 5 | Scout | Y | AB' |

**Tally:** AB' 5 / B' 0 / A' 0 → **AB' wins (consecutive_wins = 2 → CONVERGED)**

---

## Convergence summary

| Round | Winner | Vote | Cons. Wins | Stop? |
|---|---|---|---|---|
| 1 | AB | 5-0-0 | 1 | No |
| 2 | AB' | 5-0-0 | 2 | **Yes** |

**Lineage chain:** A → AB → AB' (final ship candidate)

## Critique themes across rounds

1. Hook-to-payoff timing (R1 FATAL → fixed in AB)
2. Verbatim vs narrated deflection scripts (R1 FATAL → fixed in AB)
3. Defensible data anchors (R1 MAJOR → fixed in AB via Parks at Westfield)
4. Parallel lender categories (R1 MAJOR → fixed in AB)
5. Cut markers in script for editor (R1 MAJOR → fixed in AB)
6. Mid-roll CTAs at 2:30 and 5:45 (R1 MAJOR → fixed in AB)
7. Residency-to-closing timing math (R1 MAJOR → fixed in AB)
8. Toured-without-1502 recovery (R1 Scout → fixed in AB')
9. Registration handcuff + procuring-cause naming (R1 Scout → fixed in AB')
10. Runtime under long-tail penalty (R2 MAJOR → fixed in AB')
11. Title #3 single-subdivision specificity (R2 MAJOR → fixed in AB')
12. Hook-to-close structural symmetry (R2 marginal → added in AB')

## Reason composite score

```
quality_delta       = (3900 - 2800) / 2800 = 0.39, capped at 1.0 = 0.39
rounds_survived     = 2
judge_consensus     = 1.0 (final round)
critic_fatals_addr  = 2 (both R1 FATAL fixed and didn't recur)
convergence_achieved = true
no_oscillation      = true

reason_score = 0.39 * 30 + 2 * 5 + 1.0 * 20 + 2 * 15 + 10 + 5
             = 11.7 + 10 + 20 + 30 + 10 + 5
             = 86.7
```
