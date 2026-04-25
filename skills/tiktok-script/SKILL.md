# Skill: TikTok Property Tour Prep Sheet

## Triggers
"tiktok tour", "property tour tiktok", "tiktok about [address]", "film this for tiktok"

## Purpose
Generate an on-site prep sheet Taylor can pull up on his phone while walking a property with his gimbal. NOT a script — talking points, shot notes, and buyer value-adds organized by room/stop.

## Parameters

| Parameter | Required | Source |
|-----------|----------|--------|
| Property address | Yes | Taylor provides |
| Price | Yes | Taylor provides or MLS |
| Beds / Baths / SqFt / Lot | Yes | Taylor provides or MLS |
| Target persona | Yes | Taylor specifies or Claude infers from neighborhood + price point |
| Neighborhood | Yes | Taylor provides |
| Key features / upgrades | Optional | Taylor provides — if missing, Claude asks |

Valid personas (TikTok only — NO investors):
- **BSW Medical** — commute to BSW, physician loan eligibility, professional lifestyle
- **Military** — BAH affordability, proximity to Fort Hood, PCS-friendly
- **General / Relocator** — school zones, lifestyle, commute, value for money

## Execution

### Step 1 — Identify Property Parameters
Confirm all required parameters. If Taylor drops an address with no details, ask for price + beds/baths/sqft + persona before generating. If Taylor says "just use MLS" — flag that Claude cannot pull MLS directly and needs the numbers.

### Step 2 — Load Config
Read `social-media-config.json` for:
- Current hashtag tiers (broad, niche, local)
- Active DM keyword CTAs
- Brand voice rules

### Step 3 — Generate Tour Prep Sheet

Output format below. Every section is mandatory.

### Step 4 — Save Output
Save to: `output/YYYY-WXX/tiktok/[property-address-slug].md`
- Address slug format: `1234-main-st` (lowercase, hyphens, no city/state)
- Create week folder if it doesn't exist

---

## Output Template

```markdown
# TikTok Tour Prep — [Full Address]
**Date:** [YYYY-MM-DD] | **Price:** $[XXX,XXX] | **[X]bd / [X]ba / [X,XXX] sqft** | **Lot:** [X.XX] ac
**Neighborhood:** [Name] | **Persona:** [BSW Medical / Military / Relocator]

---

## HOOK (First 3 Seconds)
> [One scroll-stopping line Taylor says on camera, filmed on-site]

**Where to film:** [Specific spot — front yard, kitchen island, backyard, etc.]
**Gimbal note:** [Movement — e.g., "Low angle pushing forward through front door"]
**Why it stops the scroll:** [1-sentence explanation]

---

## TOUR STOPS

### Stop 1: [Room/Area Name]
**Gimbal:** [Movement direction, speed, transition from previous stop]
- [Talking point 1 — BUYER VALUE-ADD: why this matters financially or lifestyle-wise]
- [Talking point 2 — BUYER VALUE-ADD]
- [Talking point 3 — BUYER VALUE-ADD, optional]

### Stop 2: [Room/Area Name]
**Gimbal:** [Movement direction, speed, transition]
- [Talking point 1 — BUYER VALUE-ADD]
- [Talking point 2 — BUYER VALUE-ADD]

### Stop 3: [Room/Area Name]
**Gimbal:** [Movement direction, speed, transition]
- [Talking point 1 — BUYER VALUE-ADD]
- [Talking point 2 — BUYER VALUE-ADD]

[Continue for 5-8 stops total depending on property size]

### Final Stop: [Backyard / Best Feature / Money Shot]
**Gimbal:** [Pull-back wide shot or dramatic reveal]
- [Talking point — tie back to hook, leave them wanting more]
- [Soft CTA lead-in: tee up the DM keyword naturally]

---

## PERSONA OVERLAY — [Persona Name]

[3-5 bullet points Taylor can weave into ANY stop. These are persona-specific angles, not room-specific.]

**If BSW Medical:**
- Commute to BSW: [X] min via [route]
- Physician loan eligible: [Yes/No + why — conventional with 0% down, no PMI, etc.]
- Nearby: [relevant amenities — restaurants, grocery, daycare, gym]
- Professional lifestyle angle: [specific benefit — home office, entertaining space, etc.]

**If Military:**
- BAH at E-[X] / O-[X]: $[X,XXX]/mo covers [mortgage estimate or "mortgage + leaves $XXX"]
- Fort Hood gate: [X] min to [specific gate name]
- PCS-friendly: [resale outlook, rental demand if they PCS out]
- VA loan angle: [specific benefit — 0% down, no PMI, funding fee estimate]

**If General / Relocator:**
- School zone: [School name] — [rating or reputation]
- Commute: [X] min to [major employer/area]
- Neighborhood vibe: [1 sentence — what living here actually feels like]
- Value play: [price per sqft vs area average, what they get for the money]

---

## CAPTION + HASHTAGS

**Caption:**
[2-3 sentences. Lead with a question or bold claim. End with DM keyword CTA.]

**DM Keyword:** [KEYWORD] — e.g., "DM me '[KEYWORD]' for the full breakdown"

**Hashtags (5 max):**
- Broad (1): #realestate
- Niche (1-2): #[militaryrelocation] #[firsttimehomebuyer]
- Local (1-2): #templetx #[neighborhood]

---

## EDITING NOTES (CapCut)

- **Target length:** 30-45 seconds (under 60s hard cap)
- **Text overlays:** Price + address on first frame, bed/bath/sqft on second
- **Transitions:** [Specific suggestions — e.g., "Match cut from kitchen counter to bathroom counter"]
- **Music:** [Vibe suggestion — upbeat/chill/dramatic, NOT specific song names]
- **Captions:** Auto-generate, clean up, bold key numbers
- **Pace:** Cut dead air. If Taylor pauses >1.5s between rooms, trim it.
- **7-second rule:** Visual change every 7 seconds minimum (new room, text overlay, angle shift)

---

## QUICK-REFERENCE (Pull up on phone while filming)

| Stop | Room | Key Line |
|------|------|----------|
| 1 | [Room] | [One-liner reminder] |
| 2 | [Room] | [One-liner reminder] |
| 3 | [Room] | [One-liner reminder] |
| 4 | [Room] | [One-liner reminder] |
| 5 | [Room] | [One-liner reminder] |
| Hook | [Location] | [The scroll-stopper line] |
| CTA | [Location] | DM "[KEYWORD]" |
```

---

## Rules

1. **TikTok = original property tours ONLY.** Never repurpose YouTube content. Never suggest "cut this from your YouTube video." Every TikTok is filmed native on-site.

2. **Every stop MUST have a buyer value-add.** Not "nice kitchen" — WHY it matters: "Quartz counters = no sealing maintenance, saves $200/yr" or "Open to living room = you can watch kids while cooking." Financial savings or lifestyle benefit, every single bullet.

3. **Hook must be filmed on-site.** No desk intros, no green screen, no "hey guys." Taylor is standing in or in front of the property. The hook references something you can SEE.

4. **Never fully answer — leave value in the DM.** The tour shows enough to create desire. The full breakdown (comps, neighborhood data, school ratings, investment numbers) lives behind the DM keyword. Every prep sheet must have a clear DM funnel.

5. **No investor content on TikTok.** No cap rates, no cash-on-cash, no rental comps, no "great investment property" angles. Investors stay on YouTube. If the property is objectively an investment play, find the owner-occupant angle instead.

6. **Use "Fort Hood" not "Fort Cavazos."** Name reverted July 2025. This applies to all talking points, captions, and hashtags.

7. **Use "buy-and-hold investors" not "turnkey."** Unlikely to come up since no investor content on TikTok, but if referencing in any context, use the correct term.

8. **No agent speak.** Never use: dream home, white glove, turnkey, nestled, charming, stunning, boasts, perfect for, won't last long. Say what the house DOES and what it SAVES.

9. **Gimbal notes must be specific.** Not "smooth pan" — say "Slow push forward through front door, pause 2 beats on living room wide shot, then arc left toward kitchen." Taylor is reading this while holding the gimbal.

10. **Talking points are bullets, not sentences.** Taylor improvises. Give him the data point and the value-add. He'll say it in his own words. Keep bullets under 15 words.

11. **Persona overlay is separate from tour stops.** The overlay gives Taylor persona-specific facts he can drop into ANY room naturally. Don't force "mention BAH in the kitchen" — let Taylor weave it where it fits.

12. **Quick-reference table is mandatory.** This is what Taylor actually looks at on his phone between rooms. One line per stop. If he can't scan it in 5 seconds, it's too long.

## Quality Gate Checklist

Before delivering the prep sheet:
- [ ] Every tour stop has at least 2 bullet points with explicit buyer value-adds
- [ ] Hook is on-site (not desk/studio)
- [ ] No investor language (cap rate, cash flow, rental income, ROI)
- [ ] No banned agent-speak words
- [ ] DM keyword is set and CTA appears in caption
- [ ] Hashtags follow 3-tier structure (broad + niche + local), 5 max
- [ ] Gimbal notes are specific enough to follow while filming
- [ ] Quick-reference table has every stop in one scannable line
- [ ] Persona overlay has real data (commute times, BAH figures, school names)
- [ ] Total tour stops: 5-8 (not fewer, not more)
- [ ] "Fort Hood" used (never "Fort Cavazos")
