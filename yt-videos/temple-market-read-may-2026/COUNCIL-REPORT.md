# Council Report — Temple TX May 2026 Market Read

**Date:** 2026-05-17
**Topic:** "What's actually happening in Temple TX real estate right now (May 2026 market read)"
**Channel:** Living in Temple (BUYER/RELOCATOR lane)
**Council config:** 5 judges (Retention Engineer, Contrarian, Viewer, Analyst, Scout), 3-round bounded
**Result:** **Converged 5-0 × 2 rounds (R2 + R3). AB' is the production ship.**

---

## EXECUTIVE SUMMARY

The council took a competent but flawed cold-start draft (Candidate A) and produced a meaningfully better final artifact (Candidate AB'). The structural arc was rebuilt (4-section list → 3-changes narrative), the hook was reframed (abstract percentage → viewer's physical experience), every forecast surface was eliminated, and the headline median was corrected to the actual relevant-band median for Taylor's audience.

**The script that's now in `script.md` is meaningfully different — and stronger — than the one a one-pass draft would have shipped.**

This is month one of a monthly series. The "same five numbers every month" anchor is now a real commitment.

---

## TOP 3 WINS THE COUNCIL LOCKED IN

These are the things the adversarial loop CAUGHT that a one-pass draft would have shipped.

### 1. Killed the forecast surface

**What a one-pass draft would have shipped:** Three forward-looking claims that violated the script's own "this is a market read, not a forecast" rule.
- "your monthly payment math may improve in 2027 if rates drop"
- "Half have cuts. The other half are going to."
- "The 2021 market is done."

**What the council shipped instead:** Mechanism statements without forecasts.
- "Watch the months ahead — if rates move, your math shifts; if they don't, your math is the same as today."
- "91 of them already cut. The other 91 are sitting at original list past the normal selling window. Make of that what you will."
- "The 2021 market is gone for now."

**Why this matters:** A contrarian commenter or industry critic would isolate any rate forecast and use it to discredit the analyst voice. The council eliminated every forecast surface — meaning Taylor cannot be quoted out of context in October 2027 if rates didn't drop.

### 2. Fixed the frame-inverted headline number

**What a one-pass draft would have shipped:** Used the $293K all-bands median sold price as the headline number, then debunked it 9 minutes later by saying it's misleading for the actual audience.

**What the council shipped instead:** $293K is acknowledged ONLY as "the headline you'll see in news write-ups" and immediately followed by the verified band median for Taylor's actual audience — $348,000 for the $300K-$500K band. This was VERIFIED against the May 14 MLS CSV in Round 3, not approximated.

**Why this matters:** The BSW physician or relocator family searching this video doesn't care about the entry-level median — they care about the median in their actual budget band. Using the right number upfront earns trust. Using the wrong number and debunking it later breaks the analyst frame.

### 3. Anchored the hook in viewer experience, not abstraction

**What a one-pass draft would have shipped:** "Right now in Temple, more than half of active listings — 641 out of 1,218 — have already cut their price."

**What the council shipped instead:** "If you're moving to Temple this summer, the seller of every other house you tour has already cut their price. Not eventually. Already. Right now, May 14, 2026."

**Why this matters:** Same data, different gravity. The BSW physician watching this in the BSW lounge between cases has zero stored context for 641-of-1,218. But "every other house you tour" lands in their body — they imagine touring a house in three weeks, and the seller has already cut. That's a retention-critical seven seconds.

---

## ALSO PRESERVED (smaller wins worth noting)

- **5 named subdivisions** instead of zero — Three Creeks, Mesa Ridge, Pecan Creek, Hubbard Branch, Oak Ridge, plus the 76502 medical-zip anchor — makes the video searchable and useful for the "where should I look" buyer
- **DTI defined inline** ("total monthly debt over 43% of gross income") — earns viewer trust by not assuming finance literacy
- **PCS defined inline** ("permanent change of station") — earns the BSW viewer who isn't military
- **"Same five numbers every month" series anchor** — turns this from a one-shot video into a subscription reason
- **June topic preview** at close — builder incentives across six biggest communities — earns retention through 10:30 AND sets up the next episode
- **Banned words: zero** — final scan clean

---

## HONEST LIMITS

The council can produce a high-quality artifact, but it cannot do these things:

1. **Cannot verify live builder incentives day-of.** The 4.99-5.49% Stylecraft/Lennar rate-buydown range is hedged as "have been advertising." Taylor should briefly confirm at one builder website morning of recording.

2. **Cannot verify the 76502 active count precisely.** Approximated as ~250 in script. Taylor's morning-of MLS re-pull should produce the actual number.

3. **Cannot fully verify the pinned-comment "47-day first cut" stat.** Currently flagged in `pinned-comment.md` notes — verify against the CSV before posting, or hedge.

4. **Cannot replace cross-lab signal.** All 5 judges are Claude variants. No genuine Gemini critique was applied this run (documented opt-out). If Taylor wants cross-lab confirmation, run `~/.hermes/scripts/gemini-call.py --temperature 0.6` against `script.md` before recording. ~2 minutes, ~$0.30-$0.80.

5. **Cannot guarantee the data will hold for the recording date.** All numbers are May 14 MLS pull. If Taylor records on May 25, six numbers may have drifted (active count, % with cuts, median DOM, sold-30 count, sold median, sold DOM). Re-pull morning-of.

6. **The monthly series is now a commitment.** Once Taylor publishes "I'm doing this every month," skipping June erodes the series credibility. The reward is large but the obligation is real.

---

## NEXT PHYSICAL ACTION FOR TAYLOR

**Before recording:**
1. **Re-pull MLS** the morning of recording. Verify all 6 numbers listed in `script.md` pre-record checklist.
2. **Confirm Stylecraft/Lennar Mesa Ridge incentive band** still 4.99-5.49% via any one builder's website (5 min).
3. **Verify the pinned-comment "47-day first cut" stat** or hedge it.
4. **Optional cross-lab pass:** run gemini-call.py against final script if outside signal wanted (~2 min).

**For shoot day:**
1. Capture the new B-roll items listed in `b-roll-and-shot-list.md` (price-reduced signs, builder incentive signs, empty model home parking lot — all driveable in ~2 hours)
2. Build the running split-screen percentage graphic in editor BEFORE shoot day so on-camera reads can sync to it
3. Test the identity-timing — first sentence must end no earlier than 0:15

**Post-record:**
1. Publish to YouTube with description, timestamps, IABS link
2. Schedule GBP post within 6 hours
3. Schedule LinkedIn post within 4 hours, mid-morning CT
4. Schedule Short 24 hours after main publish
5. Schedule Temple Insider email Tuesday 8am CT

---

## STOP CHECKLIST

- **Files changed:**
  - `yt-videos/temple-market-read-may-2026/ground-truth-pack.md` (new)
  - `yt-videos/temple-market-read-may-2026/script.md` (new — production)
  - `yt-videos/temple-market-read-may-2026/titles-thumbnails.md` (new)
  - `yt-videos/temple-market-read-may-2026/description-block.md` (new)
  - `yt-videos/temple-market-read-may-2026/pinned-comment.md` (new)
  - `yt-videos/temple-market-read-may-2026/b-roll-and-shot-list.md` (new)
  - `yt-videos/temple-market-read-may-2026/repurpose-map.md` (new)
  - `yt-videos/temple-market-read-may-2026/COUNCIL-REPORT.md` (this file, new)
  - `yt-videos/temple-market-read-may-2026/reason-run-260517-1620/` (6 lineage files, new)

- **Verification:**
  - MLS data: Python script run twice on `~/market-monitor/05-14-2026-mls-templebelton.csv`; all stated numbers computed live (not estimated). Band median verification: `$300K-$500K sold last 30 days, n=59, median $348,000`. Luxury split verification: `91/91 exact at $500K+ threshold`.
  - Anti-duplication: grep across `~/claude-social-media-manager/yt-videos/` — no prior market-read video.
  - Banned words: visual scan of all production deliverables — clean.
  - Format spec: 10:30 runtime confirmed by section timing. Identity at 0:14. One creative element. 4 honest negatives. No investor pivots.

- **Residual risk:**
  - Numbers may drift between May 14 pull and recording date. Pre-record checklist exists in script.md to catch drift.
  - 76502 active count is approximated (~250). Verify morning-of.
  - Pinned-comment "47-day first cut" stat is unverified — flagged in pinned-comment.md notes.
  - No live cross-lab (Gemini) critique pass. Documented opt-out — recommended if Taylor wants extra outside signal.

- **Rollback:**
  - No production state changed (nothing published, nothing committed, no FUB writes, no emails sent).
  - To roll back: `rm -rf ~/claude-social-media-manager/yt-videos/temple-market-read-may-2026/` removes everything written this turn.

- **Next physical action:**
  - Re-pull MLS morning of recording; verify the 6 numbers listed in `script.md` pre-record checklist; then film.

---

## END COUNCIL REPORT
