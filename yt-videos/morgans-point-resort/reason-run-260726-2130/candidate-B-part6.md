# 16. COMPLIANCE REVIEW + PHRASING CORRECTIONS

## 16a. Hard-rule audit — all 14 rules from TASK.md

| # | Rule | Status | Where handled |
|---|---|---|---|
| 1 | No invented MLS stats, testimonials, reviews, awards, top-agent claims | ✅ | Every figure traces to the ground-truth tables. Zero testimonials, awards, rankings anywhere in the package. |
| 2 | Date-stamp all market numbers July 20, 2026 | ✅ | Spoken in the hook; footer on all 15 graphics; in the description, pinned comment, all 5 Shorts, and inside each quotable passage. Editor rule: no footer = doesn't ship. |
| 3 | No "safe," "family-friendly," "good schools," demographic steering, protected-class language | ✅ | None present. School content is a district-of-record statement plus a verify instruction. The "who this is for" beat (B9) is framed on transaction speed, home age, and errand distance — never on people. |
| 4 | Schools phrasing exact | ✅ | "All 29 MLS records show Belton ISD — verify your exact address with Belton ISD" appears in B8, G-13, G-14, description, pinned comment, and a quotable passage. |
| 5 | HOA not universal | ✅ | Always "27 of 29 records show None, 2 show Mandatory — verify per property." Never "no HOA here." |
| 6 | No lake access / water rights / dock promises | ✅ | B8 is built on it; G-13 line 1 and G-14 name both verification bodies; Short 5 is entirely this; pinned comment item 1; description verify block; dedicated quotable passage. **The CTA was rewritten specifically to stop violating this** (§10). |
| 7 | No unmeasured drive times | ✅ | Shot G4 requires a measured clock with departure hour visible. No measurement → no number ships. No drive-time figure appears anywhere in the package. |
| 8 | No implication Taylor served | ✅ | No military reference of any kind. |
| 9 | No dollar-volume or transaction-count credentials on camera | ✅ | None on camera and none in the description. Only credential used: "agent with EG Realty in Temple." |
| 10 | Distinguish confirmed / snapshot / observation / opinion | ✅ | Four-state chip, upper-left, ~14 state changes. Every labeled claim is *also* labeled out loud in the sentence carrying it — the chip is redundancy, not the mechanism. G-8 is an explicit OPINION card. |
| 11 | "Agent," never "broker" | ✅ | Zero instances of "broker" in viewer-facing copy. Only appearance is the TREC form's legal title, "Information About Brokerage Services," which cannot be reworded. |
| 12 | Water proximity is observation, never MLS-verified | ✅ | Stated on camera at B8; shots D3/G3 flagged as shoot dependencies with graphics-only fallbacks (§8f); the CTA labels Taylor's read as his read and routes to verification. |
| 13 | Buyer/relocator lane only | ✅ | Zero rent, cap rate, cash flow, ROI, appreciation forecast, or short-term-rental content. B7 is framed as *what to offer*, never *what this returns*. **Note:** the live page has STR/DSCR/rent content — that stays on the page, out of the video. |
| 14 | Entity declaration early but NOT in first 15 seconds | ✅ | Hook B1 (0:00–0:16) carries no name, brokerage, or credential. Declaration lands at 0:16, opening B2. Description opens with it. |

## 16b. Banned-words check

Scanned: dream home · dream · charming · nestled · turnkey · white glove · hidden gem · perfect neighborhood
· exclusive · sneak peek · insider · my expertise · paradise · oasis · stunning · gorgeous · safe ·
family-friendly · good schools.

**Result: zero occurrences in any viewer-facing copy** — hook, all ten beats, all 15 graphics, title and 8
alternates, thumbnail text, CTA, description, chapters, pinned comment, all 5 Shorts, all quotable passages.
Verified by mechanical grep across every candidate file, not by eye.

Also avoided as adjacent risk though not on the list: "luxury," "must-see," "won't last," "priced to sell,"
"motivated seller," "up-and-coming," "great investment," and the entire security/protection word family.

## 16c. Risky phrasing → shipped phrasing

| Rejected | Shipped | Why |
|---|---|---|
| "You're only seeing 4 of the 15 listings" | "Eleven of the fifteen have their city field set to Belton. If your search keys on the town's name, ask where those eleven went." | The export proves the **MLS field value**, not what any portal does with it. Portals ingest, geocode and filter differently, and they change. Never assert a third party's behavior as fact. |
| "Zillow hides these listings" | *cut entirely* | Same reason, plus it names a company in an accusation. |
| "Agents are hiding listings under Belton" | "That's not anybody doing anything wrong. It's how the records got typed." | Accusation → observable pattern. Removes any implication of intent about identifiable agents. |
| "There's barely anything for sale here" | "The floor you see is $315,000. The floor that exists is $205,000." | The original mechanism was **backwards** — the filtered buyer concludes *too expensive*, not *too thin*, and crosses the town off. Getting this wrong inverts the entire point of the video. |
| "Asking $330K, selling $220K — that's your negotiating room" | "Asking, per square foot: $188. Sold, per square foot: $175. Gap: 6.9%." | The 33% gap is a **size artifact** — active homes are 32% larger. Presenting it as leverage overstates by ~5x and a sharp viewer catches it. |
| "$330K → $273K → $232K → $220K, the market is falling" | *graphic cut entirely* | Three of those four are **asking** prices. Under-contract and pending homes have no sale price until closing. Four different cohorts, three different meanings of "price." |
| "These lakefront homes…" | "There is no waterfront field in this data. Zero of twenty-nine." | The export has no water field of any kind. |
| "Most homes here have no HOA" | "Twenty-seven of twenty-nine records show None, two show Mandatory — verify per property." | A count, not a rule about the city. |
| "It's 15 minutes to groceries" | "Put the address in your phone and drive it at the hour you'd actually drive it." | No unmeasured drive times. Becomes a number only if measured on the shoot with the departure hour supered. |
| "These 1970s houses have roof and foundation problems" | "You're pricing roof age, foundation history, electrical panel, plumbing material, HVAC age. I'm not telling you any specific home here has any of those issues." | Prevents a defect claim about identifiable properties. Reframes as a budgeting instruction. |
| "That $869,000 listing is overpriced" | "It's been on the market 193 days." | Never render a verdict on an identifiable seller's pricing. State the record; let the viewer conclude. This is the clip a competing agent would screenshot. |
| "Nearly half the sellers are capitulating" | "Seven of fifteen have cut. The middle cut is under five percent. That's sellers testing, not sellers desperate." | Four of the seven cuts are under 5%. The 47% headline implies a capitulation the magnitudes don't support. |
| "In this window" | "The seven homes that closed between May 18 and July 16, 2026" | The window was never defined. It's ~60 days and n=7 — say both. |
| "15 homes for sale" | "15 active listings" | The 29 rows include 1 Coming Soon at $299,900. |
| Original CTA: "separate the true water-tier lots from the pretenders" | See §10a | Promised a data sort the video just proved impossible from this data. |

## 16d. ⚠️ OPEN — MLS display and licensing. NOT cleared.

**This is not a pass. It is an unresolved question that must be answered before upload.**

The package puts identifiable listing-level data on screen for properties Taylor does not represent:
G-5 (six listings with street name and price), G-TIER (all 15 by $/sqft), G-11 (seven closed sales with
close price and original list), G-12 (seven price-cut histories), and §8's shot list references. The
supporting tables carry street name, square footage, year built, list price, DOM, and original list price.

Unanswered:
1. Do **CTXMLS rules** permit public display of listing-level data — including **original list price and
   price-cut history**, which are often more restricted than current list price — in video content?
2. Is **listing-office / listing-agent attribution** required on screen for each displayed listing, and does
   the aggregate/statistical presentation here change that?
3. Do the **closed sale prices** carry a separate display restriction? Texas is a non-disclosure state, and
   close price is MLS-participant data, not public record.
4. Does IDX display policy apply to non-IDX video content at all?

**Resolution paths, cheapest first:** (a) email the CTXMLS/TBBOR compliance contact and get the answer in
writing — do this now, it's free and it's a one-time answer that unblocks every future data video; (b) ship
the graphics **de-identified** — bucketed $/sqft ranges and counts with no street names — which costs
specificity but removes the question entirely; (c) ship as-is only after (a) comes back clean.

**Recommendation: do (a), and prepare (b) as the fallback so the publish date doesn't depend on the answer.**
Note that the aggregate claims that carry this video — the 4/11 split, the $110,000 gap, the vintage
inversion, the 6.9% $/sqft gap — **all survive de-identification intact**. Only G-5's street names and
G-11's per-sale rows would need to change. The video does not depend on this being resolved favorably.

## 16e. Pre-publish gate — all eight before upload

1. **Re-pull MPR rows from CTXMLS on the publish date.** If any headline figure moved materially, re-cut the
   affected graphic or super `Data as of July 20, 2026 — re-verify current listings`.
2. **CTXMLS display question answered in writing** (§16d), or graphics swapped to the de-identified version.
3. Every data graphic carries the `CTXMLS · July 20, 2026` footer.
4. Every closed-side graphic carries `n=7` and `May 18 – July 16, 2026`.
5. Real TREC IABS + Consumer Protection Notice links pasted into the description — the placeholder must not
   ship. (Both are already live on templetxhomes.net and can be copied from there.)
6. The drive-time beat carries a measured number with departure hour supered, or carries no number at all.
7. Corrected transcript uploaded — not auto-captions. Every quotable passage must survive verbatim, because
   the transcript is what AI answer engines actually retrieve.
8. **FAA/B4UFLY airspace confirmed for the shoot date** before any drone launch (Fort Cavazos R-6302 sits
   west of Belton Lake).

## 16f. Page-side dependencies — the video is not shippable alone

Three items on `templetxhomes.net/morgans-point-resort/` conflict with this video. Full detail in
`../PAGE-AUDIT-2026-07-27.md`.

| Item | Severity | Why it blocks |
|---|---|---|
| Page publicly prints a local filesystem path (`/Users/taylordasch_1/market-monitor/...`) — twice | **P1** | Sits inside the page's own credibility sentence. Fix regardless of this video. |
| FAQ answers "Is Morgan's Point Resort safe?" with a crime + population characterization | **P1** | Fair-housing exposure, and "safe" is on Taylor's own banned list. Live now. |
| Page runs May 14 data (12 active, $249,500 median sold, 62 DOM); video runs July 20 data (15 active, $220,000 median close, 93 DOM) | **P2** | The video drives traffic to a page that contradicts it. Refresh the page or scope each block by cohort and date. |
| Page asserts water-tier $/sqft medians with no visible source | **P2** | The video's honesty moment is "there is no water field in this data." The page must not contradict it. |

## 16g. Inverse-fail rubric — self-check

| Failure mode | Why this package doesn't trip it |
|---|---|
| "Just a drone tour with numbers read over it" | The city-field price split, the 35-year vintage split, the two-subdivision reveal, and the $/sqft ladder all require having read the export. None can be produced by flying a drone. Both drone-dependent shots have graphics-only fallbacks that are arguably stronger. |
| Buyer burned on an implied water claim | Disclaimed on camera at B8 before any water language is used; chip-labeled; dedicated Short; pinned-comment item; description block; quotable passage; two named verification bodies. **The CTA was rewritten to stop promising it.** |
| A number fails same-day recheck or lacks its date | Every figure traces to the ground-truth tables; date spoken in the hook, footered on all 15 graphics, embedded inside every quotable passage. Gate 1 forces a re-pull. |
| Repeats the page instead of demonstrating it | The page has none of this. The city-field split, the vintage inversion, the $/sqft tier ladder, and the corrected leverage math are all new from the July 20 pull. §16f has the page rebuilt around them. |
| Reads as investor content | Zero rent, cap rate, cash flow, or return language. B7 is framed as what to offer, never what to earn. |
| Leans on the $330K median after calling it misleading | The median appears twice: once being dismantled (G-3, against the $497,500 name-carrying median), once in G-10 being explicitly rejected as a leverage metric in favor of $/sqft. Never a standalone anchor. |
