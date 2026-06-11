# Critic — Round 1

**Posture:** Outsider voice. Assume Taylor's most informed hostile commenter is reviewing this on r/TempleTX or in a BSW resident chat. Attack ruthlessly.

**Note on cross-lab signal:** Per council protocol, flagship work should default-on Gemini critic. This run uses Claude in "outsider voice" mode (documented opt-out — see overview.md). Mitigation: critic explicitly attacks from Anthropic-blind angles (industry jargon Claude likes, advice without consequences, banned-word patterns Claude has internalized).

---

## VERDICT: REVISE (do not ship as-is)

Candidate A is a competent first draft with three FATAL issues and four MAJOR ones. None require redoing the whole script. All are surgical fixes — but a one-pass author wouldn't catch them.

---

## FATAL WEAKNESSES (must fix or kill the video)

### FATAL 1 — The hook lands without weight on the actual viewer

**Line:** "Right now in Temple, more than half of active listings — 641 out of 1,218 — have already cut their price. That's the number that explains everything else happening in this market."

**Problem:** The BSW resident watching this in the BSW lounge between cases has zero stored context for what 641-of-1,218 means. A number that big needs an anchor that lands in the viewer's body — not just on the screen. The current hook is data-first but audience-blind. It's the kind of hook an analyst writes; not the kind a relocating buyer needs to hear at second 7.

**Proposed rewrite:**
> "If you're moving to Temple this summer, the seller of every other house you tour has already cut their price. Not eventually — already. Right now, May 14, 2026: 52.6% of active Temple listings have cut at least once. That's the market you're walking into."

This anchors the number in the viewer's physical experience (touring a house), then commits to the data. Same number, different gravity.

### FATAL 2 — "Back to normal" tone is wrong for the actual audience

**Line:** "We're back to a normal market — and by normal I mean the pre-2020 baseline, where a well-priced home takes about two months to sell and a mispriced home sits."

**Problem:** Historically true, emotionally wrong. The BSW physician carrying a 7% mortgage payment on a $400K house has no emotional access to "normal" — their normal IS the COVID-era market. Saying "back to normal" sounds like dismissal of their financial reality. The data is right; the framing alienates the exact viewer this video is for.

**Proposed rewrite:**
> "Median days on market is 65 to 75 right now. That's roughly double 2022. For a seller, that's painful. For a buyer at today's interest rate, it's the only leverage you have to work with. The market hasn't crashed — it's slowed down to a pace where you can actually negotiate. That's the trade."

### FATAL 3 — "Rates may drop in 2027" is forbidden speculation

**Line:** "your monthly payment math may improve in 2027 if rates drop, even if prices don't."

**Problem:** The script opens with "This is a market read, not a forecast." Then breaks that rule in the "who should wait" section. A contrarian judge or hostile commenter will isolate this clip ("Taylor predicts rate cuts in 2027") and Taylor has zero defense. Either delete the rate forecast OR replace with a market-mechanism statement that isn't forward-looking.

**Proposed rewrite:**
> "You have more flexibility. Watch the months ahead — if rates move, your math shifts. If they don't, your math is the same as today. Either way, the inventory is here, the price cuts are here, and waiting doesn't cost you scarcity."

---

## MAJOR WEAKNESSES (degrade the deliverable; should fix)

### MAJOR 1 — Lennar incentive claim is unsourced

**Line:** "A typical Lennar in Hubbard Branch right now is offering a 4.99% rate buydown for 24 months."

**Problem:** Specific enough to be checkable, but no source on-screen or in description. If Lennar's actual offer in May 2026 is different, Taylor looks like he made it up. Either pull the actual offer from `~/market-monitor/builder_incentives/` and quote it precisely, or hedge: "Builders in this band have been offering rate buydowns in the 4.99–5.49 range; check the specific community."

### MAJOR 2 — Honest negative undermines the headline

**Line (Section 4):** "'Median sold $293,000' sounds like an affordable market. It is — for the entry buyer. For the BSW hire and the typical relocator family looking at $350K to $475K, the relevant number is closer to $375K median in that band."

**Problem:** Correct content, wrong placement. If the headline median is misleading for the actual audience, why use it as the lead-in number? The video uses $293K twice early on and then debunks it at the end. That's a frame error — the lead-in should already be the relevant number, with $293K explained as the "what you'll see in headlines vs what you'll actually pay" pivot.

**Proposed rewrite:** Compute the median for the $300K–$500K band live and use IT as the headline, with the $293K all-bands median as the explanatory contrast.

### MAJOR 3 — Zero named neighborhoods

**Problem:** A viewer searching "Temple TX neighborhoods" or "where to buy in Temple" will not find this video helpful for their next click. The data has the top-12 active subdivisions (Three Creeks, Mesa Ridge, Pecan Creek, Hubbard Branch, etc.) and they don't appear in the script except for Hubbard Branch once. This is a 60-second add that doubles the video's utility for the BSW/military buyer.

**Proposed rewrite:** Insert a 60-second segment after Section 3: "Where these listings actually are. Three Creeks, Mesa Ridge, Pecan Creek are the three highest-volume active subdivisions right now — combined they're roughly 90 of the 1,218. If you've been scrolling Zillow, these are the names you've seen most. Here's the quick read on each: Three Creeks is mid-tier resale plus some new construction in the $325K–$425K band. Mesa Ridge is heavier new construction, similar price. Pecan Creek is older resale, slightly lower price point. None of those is a recommendation — it's where the inventory is."

### MAJOR 4 — Buyer advice without consequences

**Problem:** Every "buyer move" callout states a tactic without stating what happens when you do it.

- "Pull a property's price history" → no consequence stated
- "Walk if the seller hasn't cut" → no consequence stated
- "Get a real inspection" → no consequence stated

**Fix:** Each tactic gets one line of consequence. "Pull a property's price history. If you see one cut, expect more leverage in your counter — sellers who have already moved their number once will usually move again." That stickiness turns advice into a memorable rule.

---

## MINOR WEAKNESSES (polish)

### MINOR 1 — Generic retention cliché
**Line:** "Stay through the end. The last two minutes are the part most videos skip."
**Fix:** Either name what the last two minutes contain, or cut the line. Recommend: "Stay through the end — the last two minutes are who should wait, with the numbers, and that's where most market videos chicken out."

### MINOR 2 — Graphic suggestions are bland
**Fix:** The "one creative element" is the running split-screen graphic showing the price-cut percentage rising over time. Lean into THAT all the way through — make it the visual anchor every section returns to. Don't add competing visuals.

### MINOR 3 — CTA "comment 'data'" creates an unfulfilled obligation
**Fix:** Either set up an auto-reply Drive link or replace with: "If you want the spreadsheet I'm working from, the link is in the description — it auto-updates monthly."

### MINOR 4 — Doesn't establish series
**Fix:** Earn the sub by anchoring this as month 1 of a monthly cadence. Add one line at 0:35: "First of what I'm doing every month — May 14 pull this time, June around mid-month."

### MINOR 5 — One banned-word risk
**Scan:** No banned words detected. ✓ Clean on banned vocabulary.

### MINOR 6 — No anchor to where Taylor's biz pulls from
**Fix:** Add one closing line that ties the data series to Taylor's pages. "Full market dashboard at templetxhomes.net — updated monthly with the same MLS pull." This converts views to website traffic for AEO.

---

## DOMAIN CHECKS

| Check | Status | Notes |
|---|---|---|
| Identity in first 3 sentences but not first 15s | ✓ COMPLIANT (borderline) | Identity at 0:15–0:35. Tighten to ensure sentence 3 starts AT 0:15 exactly. |
| One creative element | ✓ if executed | Script names the split-screen graphic but doesn't enforce it as the sole visual. |
| Honest negatives included | ✓ 3 negatives present | Quality of negatives is good; placement of #1 is the MAJOR 2 issue. |
| Lane discipline (buyer, no investor) | ✓ COMPLIANT | No cap rates, no rental analysis, no investor pivots. |
| Banned words | ✓ CLEAN | None detected. |
| BSW specifically addressed | ✓ partial | BSW called out once in Section 4. Could be stronger throughout. |
| Military specifically addressed | ✓ partial | PCS-window addressed once. Could earn more screen time. |
| Data freshness anchored | ✓ STRONG | "May 14 pull" stated three times. |

---

## OVERALL ASSESSMENT

This is a publishable draft with revision. The data work is correct. The voice is on-brand. The lane discipline holds. The format spec is mostly met.

But three frame errors (hook landing, "back to normal" tone, rate forecast) and four content gaps (unsourced incentive, frame inversion on median price, no named neighborhoods, advice without consequence) mean a single-pass version would ship with material weaknesses.

**Recommend:** Candidate B drafts independently from the Ground Truth Pack, addressing every FATAL and MAJOR explicitly, with a different structural angle (consider opening with the neighborhood-where-inventory-is angle instead of the headline-percentage angle).

---

## END CRITIC R1
