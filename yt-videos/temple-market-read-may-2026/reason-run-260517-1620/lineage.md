# Lineage — Temple TX May 2026 Market Read Council Run

Full decision trail. What changed at each step and why.

---

## Pre-Round 0: Reconnaissance

| Check | Source | Outcome |
|---|---|---|
| MLS data freshness | `~/market-monitor/05-14-2026-mls-templebelton.csv` | 3 days old (within 7-day window) ✓ |
| Anti-duplication | grep over `~/claude-social-media-manager/yt-videos/` | No prior market-read video. References only. ✓ |
| Existing project folder | `ls ~/claude-social-media-manager/yt-videos/temple-market-read-may-2026/` | Did not exist; created |
| Voice precedent | `bsw-residents-temple-new-construction/script.md`, `temple-caution-areas/COUNCIL-REPORT.md` | Investor-analyst voice + identity block pattern lifted |
| Brain query (Phase 0) | mem-search corpus | No prior Taylor takes on monthly market reads. New territory. |

---

## Round 1

### Candidate A (cold-start)
**Author posture:** Analyst-first single-pass. No critique input. Baseline for adversarial attack.

**Structure chosen:** Hook → Identity → 4 sections (price cuts, DOM, inventory mix, who buys/waits) → Honest negatives → Close

**Strengths in A:**
- Hits all the required data points
- Identity block delivered at compliant timing
- Lane discipline holds throughout
- No banned words

**Weaknesses A shipped that critic caught:**
- Hook landed on abstract percentage, not viewer's physical experience
- "Back to normal" tone alienated rate-burdened buyers
- "Rates may drop in 2027" violated own no-forecast rule
- Unsourced Lennar incentive claim
- Frame-inverted median price (used misleading number first, debunked it last)
- Zero named neighborhoods
- Buyer advice without consequences

### Critic R1
**Posture:** Outsider voice. Attack from Anthropic-blind angles.

**Output:** 3 FATAL + 4 MAJOR + 6 MINOR weaknesses. Verdict: REVISE.

**Most valuable catches:**
- FATAL 1: Hook should anchor in viewer's physical experience
- FATAL 3: Rate forecast violated own rule
- MAJOR 2: Median-price frame inversion
- MAJOR 3: Zero named neighborhoods is a 60-second add for huge utility gain

### Candidate B (independent, post-Critic)
**Author posture:** Story-first. Three-changes narrative arc instead of four-sections list.

**Structural differences from A:**
- Hook anchored in "every other house you tour" — viewer's physical experience
- Three-changes narrative (sellers blink, you have time, builders compete) — narrative arc
- Named neighborhoods baked in as Section 4, not absent
- "Buyer move + consequence" rule applied throughout
- All rate forecasts removed
- Series anchor at 0:35
- Single split-screen graphic locked as the one creative element

**Critic feedback addressed in B:** All 3 FATAL + all 4 MAJOR ✓

---

## Round 2

### Synthesis AB
**Method:** B as base (95%), with 5 surgical patches from A and from critic MINOR feedback.

**Patches applied:**
1. (None substantial from A — B was the structural winner)
2. Critic MINOR: Replace "stay through the end" generic tease with specific tease
3. Critic MINOR: Add templetxhomes.net dashboard close
4. Critic MAJOR 2: Compute $300K-$500K band median for the relevant audience
5. Inverse-fail check: every leverage claim paired with honest negative

### 5 Judges vote
| Judge | Vote | Key critique |
|---|---|---|
| Retention Engineer | SHIP | Preview June topic in close |
| Contrarian | SHIP | "Other half are going to" is a forecast — fix |
| Viewer | SHIP | Define DTI, PCS, VA loan inline |
| Analyst | SHIP | Verify $375K band median (placeholder; needs MLS re-pull) |
| Scout | SHIP | Add 76502 active count; anchor monthly series |

**Result: 5-0 SHIP, with 8 surgical patches and 1 verification flag**

---

## Round 3

### Verification before AB'
**Action:** Pulled $300K-$500K band median from MLS CSV.
**Result:** Actual = $348,000 (not $375K placeholder). Updated script.

**Other numbers verified:**
- $1.8M max cut: confirmed single-record max ✓
- 91/91 luxury split: exact (50% with cuts, 50% without) ✓
- 76502 active count: approximated as ~250 (needs Taylor's morning-of verification)

### Synthesis AB'
**Method:** Apply all 8 R2 surgical patches + 1 verified data update.

**Patches applied to AB → AB':**
1. Luxury "other half going to" → "Make of that what you will" (forecast eliminated)
2. "Sellers blink first" → "Sellers are the ones moving their numbers now" (softened claim)
3. "Is done" → "Is gone for now" (smaller forecast surface)
4. DTI defined inline ("total monthly debt over 43% of gross income")
5. PCS defined inline ("permanent change of station")
6. $375K → $348K (verified actual band median)
7. 76502 active count line added
8. "Same five numbers every month" series anchor added
9. June topic preview ("builder incentives across six biggest active communities")

### 5 Judges confirmation vote
| Judge | Vote |
|---|---|
| Retention Engineer | SHIP |
| Contrarian | SHIP |
| Viewer | SHIP |
| Analyst | SHIP |
| Scout | SHIP |

**Result: 5-0 SHIP**

---

## Convergence

| Round | Vote | Direction |
|---|---|---|
| R2 | 5-0 | SHIP |
| R3 | 5-0 | SHIP |

**Convergence rule satisfied: 2 consecutive same-direction votes.**
**Final artifact: AB' (synthesis-ab-prime-r3.md)**
**Production file: script.md (parent folder)**

---

## What was cut and why

### Cut in R1 → R2 (B chose different framings than A)
- Cut: "Stay through the end. The last two minutes are the part most videos skip." (generic retention cliché)
- Replaced: "Stay through the last two minutes — that's where I lay out who should wait, with the numbers. Most market videos chicken out on that one." (specific + earns retention)

### Cut in R2 → R3 (judge patches)
- Cut: "your monthly payment math may improve in 2027 if rates drop" (rate forecast)
- Replaced: "Watch the months ahead — if rates move, your math shifts; if they don't, your math is the same as today." (mechanism statement, no forecast)

- Cut: "Half have cuts. The other half are going to." (forecast)
- Replaced: "Half — 91 of them — already cut. The other 91 are sitting at original list past the normal selling window. Make of that what you will." (verified count + reader inference)

- Cut: "the relevant number is closer to $375K median in that band" (placeholder)
- Replaced: "the actual median in your band on May 14 was $348,000" (verified from CSV)

### Cut in R2 → R3 (scope discipline)
- **Cut from this episode:** Pending sales as leading indicator (Scout's missing-angle)
- **Rationale:** Adds 30-45 seconds, requires CSV column verification, would push runtime over 11:00 on episode 1
- **Logged for June read:** Build pending-sales tracking into the June episode

---

## Honest limits of this run

1. **Single-model simulation.** All 5 judges + Author + Critic + Synthesizer are Claude variants. No genuine cross-lab signal. Treat 5-0 vote as "no internal contradictions," not "5 independent minds agreed." Gemini cross-lab pass was opt-out for this run — recommend Taylor invoke gemini-call.py against final script before recording if cross-lab confirmation is wanted.

2. **One number is approximate.** 76502 active count (~250) was estimated, not directly computed. Taylor's morning-of MLS re-pull should verify and update.

3. **47-day "first cut" pinned-comment number is unverified.** Currently flagged in pinned-comment.md notes — Taylor must verify or hedge before posting.

4. **Stylecraft/Lennar incentive band (4.99-5.49%) is from recent observation, not live-pulled from builder sites.** Hedged as "have been advertising" in script. Morning-of recording, briefly confirm at any one builder's website.

5. **The "monthly series" promise is now a commitment.** AB' commits Taylor to a June read. If June doesn't ship, channel credibility erodes. Worth the trade-off (the series anchor was a 5-0 judge ask), but it's a real obligation.

---

## END LINEAGE
