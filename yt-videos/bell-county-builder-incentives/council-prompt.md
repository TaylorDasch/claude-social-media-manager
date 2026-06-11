# Council Prompt — Bell County Builder Incentive War Room

## The page

- URL: https://www.templetxhomes.net/bell-county-builder-incentives/
- Job: Utility + Money page (live data board + intake)
- Rail: Relocation only — NOT investor (see memory: no-new-build-portfolio-framing)
- Channel: **Living in Temple** (NOT Investing in Temple — relocator rail)
- Audience: BSW relocator, move-up buyer, military relocation
- Data: 172 cards across 7 Bell County markets (Temple, Belton, Salado, Killeen, Harker Heights, Nolanville, Troy); refreshed daily
- Page v4 deliverables added in this build:
  1. Taylor's Take weekly editorial inset
  2. Decision matrix — 3 relocator lanes × 3 questions each
  3. Amber expiring treatment (`dom >= 180 AND price_cut > 0` → ~19% of live feed)
  4. Pulse animation on the LIVE indicator
  5. Live pill degrades to "Last Verified" when feed > 48h stale

## What to produce

**Long-form (6–12 min) for Living in Temple:**

Angle: "We built a daily-refreshed builder incentive scanner for Bell County — here's what's actually negotiable in Temple, Belton, Salado, Killeen, and Harker Heights this week."

Beat structure to council:

1. **Cold open (0:00–0:15)** — open with the dollar number: "$X currently sitting on Bell County builder lots in stated incentives — and most of it does not appear on the listing." Then drop the page.
2. **Why this exists (0:15–0:45)** — most agents don't track incentives systematically; builders don't push them in MLS remarks; the average buyer leaves $15K–$40K on the table.
3. **What the scanner does (0:45–2:00)** — pulls daily MLS export, scores every active build for negotiability (incentive stacking + DOM + price-cut depth), surfaces top cards across 7 markets.
4. **The three buyer lanes (2:00–5:00)** — walk through the decision matrix on camera: BSW relocator (closing credit + physician-loan stacking), move-up buyer (price cut + aging inventory), military relocation (rate buydown + VA stacking). One actual current card per lane.
5. **The traps (5:00–7:00)** — preferred-lender requirements that compete with physician-loan terms; quietly retired "new release" reprices; VA-incompatible buydowns. Each trap gets a specific question Taylor would ask the builder rep.
6. **Taylor's Take this week (7:00–9:00)** — the on-camera version of the Take inset: Hodges Eagle Ridge as the lever, Flintrock volume vs window, Sandor Homes in Nolanville. Show the page on screen.
7. **CTA (9:00–end)** — "The board refreshes every morning. Bookmark `templetxhomes.net/bell-county-builder-incentives/`. If you want the verified incentive packet for your target market, link is in the description."

## Hooks (5 variants)

Council should produce 5 hook variants prioritizing:
- The number ($47K average across the board, or a higher specific deal)
- The negative — "Why your builder will never list these incentives"
- The contrarian — "Most of the deals on this board are NOT good — here's how to find the 19% that are"
- The authority — "I tracked every builder incentive in Bell County for 6 months. Here's what I learned."
- The lane — "If you're moving here for BSW, this is the one math equation builders don't want you to run."

## Thumbnail brief

3 concepts:
1. Taylor + a stack of three Bell County builder yard signs (Flintrock / Hodges / Sandor) + a number overlay "$47K avg"
2. Phone screenshot of the war room board on screen, with an amber-circled card and the word "WATCH" — title overlay "THE BUILDER TRAPS"
3. Split screen — left: MLS listing showing "Call for incentives"; right: the war room card showing the actual stacked deal. Text overlay: "What the listing hides."

## Shorts package (3 vertical cuts)

1. **The trap shot (30s)** — "Builders will tell you the rate buydown applies on any loan. It doesn't on VA. Here's the question you ask first." → page on screen at the matrix.
2. **The list (45s)** — "Three things to ask before you let a builder lock you into their preferred lender." → 3 cards on screen, each one a question.
3. **The dossier (30s)** — pick the actual best-scored card on the live feed when filming, walk through it on camera, end with the war room URL.

## Pinned comment

```
The Bell County Builder Incentive War Room: templetxhomes.net/bell-county-builder-incentives/?utm_source=youtube&utm_medium=description&utm_campaign=bell-county-builder-incentives

Refreshes daily. If you want the verified incentive packet for your specific target market, the intake form is at the bottom of the page — one personally reviewed reply, no drip blast.

— Taylor Dasch, EG Realty
```

## Compliance check before publishing

- No "dream home / nestled / vibrant / charming / hidden gem / welcome home" language
- No investor framing on this video (relocator rail only)
- Every dollar number used in the video must match what's actually on the page that day
- Use "agent" not "broker"
- Verify-before-offer caveat included verbally at least once

## Embed-back step

After the YouTube upload:
1. Get the video ID.
2. Add the iframe near the top of the war room page (above the AI Answer Box), per project CLAUDE.md flywheel rule.
3. Add `VideoObject` schema to the existing JSON-LD block on the page.
4. Cross-post the 3 Shorts via Postiz to TikTok + IG Reels + YT Shorts.
5. Mention the video in the next Temple Insider newsletter issue.
