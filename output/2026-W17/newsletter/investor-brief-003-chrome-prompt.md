# Chrome/Claude Build Prompt — The Temple TX Investor Brief Issue #3

**How to use:** Open Beehiiv → New Post → paste the HTML from `investor-brief-003.html` into the **Code editor** (not the rich-text editor) and preview. If that doesn't render cleanly, feed this whole file to Claude in Chrome and let it rebuild the layout in Beehiiv's UI.

---

## Subject Line Options (pick strongest for your audience)

- **A:** One building. Seven deals. 4.8% cap to 21.6% cap.
- **B:** Why Temple math picks old construction — and the 33% insurance gap
- **C:** Seven ways to buy 111 S 33rd (and why I'd run #3)

**Preview text:** Plus: the 250 basis point cap rate spread Texas investors should know about in 2026.

---

## Publishing Metadata

| Field | Value |
|---|---|
| **Title** | The Temple TX Investor Brief — Issue #3 |
| **Subtitle** | Seven ways to buy the same $389K building. Plus: the 250 bps cap rate spread between new and old Texas construction. |
| **Meta title** | Issue #3 — Seven Plays, One Building, and the New vs Old Construction Spread |
| **Meta description** | One $389K Temple TX building. Seven different investor strategies from 4.8% to 21.6% cap. Plus: Q1 2026 research on new construction vs older home investment returns in Texas. |
| **Tags** | investor-brief, deal-of-the-week, 111-s-33rd, bsw, new-vs-old-construction |
| **Audience** | Free (all subscribers) |
| **Send time target** | Thursday 2026-04-30, 7:00 AM CT (biweekly cadence from Issue #2 on 4/16) |

---

## Photo Placeholder to Fill Before Send

- **111 S 33rd St Hero — 10,500 SF exterior (600x400):** Pull from MLS listing photos or screen-grab from the YouTube video ([N0c9_hJOxR8](https://youtu.be/N0c9_hJOxR8)). There is only one hero image needed — the seven-plays table does the rest of the visual work.

---

## Content — HTML Source

Full HTML lives at: `claude-social-media-manager/output/2026-W17/newsletter/investor-brief-003.html`

**If pasting into Beehiiv rich-text editor,** copy the HTML and use Beehiiv's "Paste as HTML" option if available. If layout breaks, fall back to the code editor or rebuild visually from this structure:

1. **Header** — dark navy (#1e293b) bar, "The Temple TX Investor Brief" Georgia serif, emerald underline, gold "Issue #3 · April 2026" label
2. **Opening** — 2 paragraphs, "Taylor Dasch with EG Realty" entity declaration in first sentence
3. **THE BRIEFING** — H2 + 3 paragraphs on the Texas cap rate spread and concessions
4. **THE DEEP DIVE** — 5 stat callout boxes (gold left border) + "two businesses" framing + Taylor's Take callout (dark card, emerald left border) + Scars and All warning (amber)
5. **THE DEAL AUTOPSY** — 111 S 33rd header + hero photo placeholder + 7-play summary table (dark header row) + detailed write-ups for Plays 3-7 + Taylor's Verdict callout (dark card, emerald left border)
6. **THE SIGNAL** — 3 bulleted signal points
7. **ONE QUESTION** — reader reply prompt (A vs B)
8. **SIGN-OFF** — Taylor contact + unsubscribe note

---

## Critical Rules (from QUALITY-GATES.md)

- **Do NOT rewrite the content.** Format it, don't soften it.
- **Banned words:** charming, nestled, turnkey, dream home, perfect, hidden gem, vibrant, thriving. None appear in the source — keep it that way.
- **Scars and All negatives are mandatory.** Do not remove or hedge them.
- **Tables must have right-aligned numbers.**
- **Entity declaration** ("Taylor Dasch with EG Realty") is already in the first paragraph. Do not remove.
- **Unsubscribe footer** is required.
- **Photo placeholder** must stay visible until Taylor fills it with the real hero image.

---

## Post-Send Checklist (after Beehiiv confirms delivery)

1. **Blog republish** — 48-72 hours after send, republish as `/investor-brief/issue-003-seven-plays-111-s-33rd/` on templetxhomes.net with canonical tag pointing to Beehiiv URL. Apply bn- gold standard styling. Add `Article` + `FAQPage` JSON-LD (pull FAQ from "One Question" + the five deep-dive stat callouts).
2. **Registry update** — add row to `claude-social-media-manager/data/content-registry.csv`.
3. **FUB tag** — any subscriber who replies to "One Question" gets the tag `investor-brief-engaged-apr-26` in FUB.
4. **Issue #4 prep** — Start Issue #4 draft with a "Reader Responses" section pulling anonymized A/B replies from this issue.
