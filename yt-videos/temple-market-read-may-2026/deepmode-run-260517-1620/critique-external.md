# Phase 6 — External Check (Gemini Hostile-Critic Pass)

**Model:** gemini-3-pro-preview
**Temperature:** 0.6
**Input:** v2.md (full deepmode v2)
**System prompt:** Hostile critic from a different lab. Imagine you're a skeptical BSW resident, a military spouse who's seen 100 realtor videos, or a Round Rock relocator burned by sales-y content. Return 3 biggest blind spots + 1 thing done surprisingly well. Under 600 words. No preamble.

---

## Gemini's Raw Critique (verbatim)

### Blind Spot 1: Medical Match Day is in March; mid-May is terrifyingly late.

You are targeting BSW residents with a video dated May 14th, telling them the "June Match" pool goes tight and to get pre-approved today. Match Day is the third week of March. By mid-May, 90% of incoming PGY-1s have already bought or signed leases because orientation starts in mid-June. To a BSW resident, you sound completely out of touch with the actual Graduate Medical Education timeline.
- **Section:** 4:00–5:30 — "BSW resident or fellow... arriving for June start... pre-approval letter in hand before any model home."
- **1-Sentence Fix:** Acknowledge they are late to the Match cycle and pivot the strategy to targeting homes that just fell out of escrow, or advise them on securing short-term rentals while shopping the July inventory dip.

### Blind Spot 2: Contradictory, dangerous timeline math for Military PCS.

You tell military families they have a hard late-July deadline for school enrollment, warn them that VA appraisals take 10-14 days longer, but then tell them their "offer timeline can be slower" and to "let a listing sit." If a PCS buyer waits for a listing to age 40 days in June, then endures a 45-day VA close, their kids are starting school in a La Quinta.
- **Section:** 5:30–6:30 — "The fifty-three percent price-drop pool works in your favor... because your offer timeline can be slower. You can let a listing sit..."
- **1-Sentence Fix:** Change the advice to aggressively target *already* aged inventory right now, rather than waiting for fresh listings to age, ensuring they clear the 45-day VA closing window before August 1st.

### Blind Spot 3: The "Anti-Sales" persona masks a blatant bait-and-switch funnel.

You spend 10 minutes posturing as an objective, data-first analyst who hates cliché realtor spam, but then you gate the only truly actionable data (the zip-code specific pull) behind a mandatory 20-minute Calendly sales call. A burned Round Rock relocator sees right through this; holding the data hostage until they agree to a phone call completely undercuts the "information, not advice" high ground you just built.
- **Section:** 9:45–10:30 — "Calendly for a twenty-minute call — I'll send you a dated MLS pull, zip-code-and-price-band filtered... before we get on the call."
- **1-Sentence Fix:** Offer the zip-code filtered MLS pull as an automated email download, making the 20-minute phone call an optional next step rather than the toll bridge to get the data.

### What the script does well

The physical laptop rotation at 0:00 showing the two raw MLS tabs. It is a brilliant, low-tech pattern interrupt that instantly proves to a skeptical viewer that you are operating inside the actual database, establishing immediate authority over every other agent reading off a polished corporate slide deck.

---

## My Decision On Each (Protocol Phase 7: Selectively Incorporate)

### Blind Spot 1 (Match Day timing): ACCEPT WITH MODIFICATION

**Gemini's frame:** "90% of incoming PGY-1s have already bought or signed leases by mid-May."

**Disagreement:** The "90%" claim is overstated. Taylor's bsw-residents flagship (May 14, council-run, on the same channel) explicitly targets the May-June BSW shopping window. That production decision was made with audience research. The "fellows + late deciders + dual-physician households + spouses still negotiating timing" cohort is real and shopping in mid-May.

**Acceptance:** Gemini's underlying catch is valid — the script should NOT assume every BSW viewer is in the ideal-cycle bucket. Some fraction watched the video AFTER missing the optimal window. The script needs to acknowledge that timing reality openly.

**Fix:** Reframe BSW section to address the audience as it actually is at filming — "PGY-1s who haven't locked housing yet, fellows transferring between programs, dual-physician households still negotiating which job takes the relocation lead, and spouses who need the buy-or-rent answer this week." Don't pretend everyone is on the ideal Match cycle. Also add: "If you DID lock housing in March or April and you're watching this in May, the next-30-days section is more relevant to you than the BSW-cohort section." Calls out the audience reality.

### Blind Spot 2 (Military PCS timeline math): ACCEPT FULLY

**Gemini's frame:** Telling PCS buyers to "let listings sit and age" contradicts the school-year deadline + VA-close padding I already told them about.

**Acceptance:** Full accept. This is an internal logical contradiction in my script. The honest play for a May 2026 PCS buyer with an August 1 school-year deadline is to target ALREADY-AGED inventory NOW, not wait for fresh listings to age. The script implied a luxury of timeline budget that the PCS calendar does not provide.

**Fix:** Rewrite the military PCS section to:
1. Lead with the calendar math (back-solve from August 1: VA close ~45 days = under contract by mid-June)
2. Action = target listings already past 40 days TODAY, not wait
3. Aged-inventory leverage is a NOW play, not a future play
4. Keep the +10-14 days VA close padding warning (correct as-is)

### Blind Spot 3 (Data-gate / bait-and-switch perception): ACCEPT WITH MODIFICATION

**Gemini's frame:** Gating filtered MLS pull behind Calendly call contradicts the anti-sales analyst posture.

**Acceptance:** Catch is real. The video positions itself as anti-sales and then makes the actionable data conditional on a sales call. That IS a credibility leak for a high-information viewer.

**Modification:** Full automated email delivery isn't a system Taylor has built yet — it would require a Hermes script to actually run the filtered MLS pull and email it. I'm not building that as part of this deepmode run. But the fix can be lighter-weight:

Add TWO paths in the CTA:
1. **Free path (no call):** Email Taylor at [address] with your zip code + price band. Taylor sends the filtered MLS pull as a one-off Gmail draft within 48 hours. No call required, no follow-up sequence.
2. **Optional path (call):** Calendly 20-min if you want to talk about what's in the pull, with the pull sent ahead of time.

This preserves the lead-gen pathway (Calendly opt-in remains) while removing the gate perception. Honest counter: the email path requires Taylor to actually do the manual MLS pull and respond inside 48 hours. Need to commit to that response window or remove the offer.

### What Gemini Liked: VALIDATION

Confirms the ONE creative element choice (two-snapshot laptop reveal) is doing the work it was designed to do. Phase 1 anchor decision validated. No change needed there.

---

## Phase 6 Tally

- Total Gemini critiques: 3 blind spots + 1 positive callout
- Accepted in full: 1 (Blind Spot 2)
- Accepted with modification: 2 (Blind Spots 1 and 3)
- Rejected: 0
- Validated: 1 (laptop reveal pattern)

Protocol Phase 7 red-flag check: Did I accept 100%? No (accepted 2 with modification). Did I reject 100%? No. Pattern looks healthy — picked up the real catches while documenting where I disagreed with framing.

Going into Phase 7 — Final v3 + Closeout.
